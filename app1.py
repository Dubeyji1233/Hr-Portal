from flask import send_file,Flask, flash,render_template, request, redirect, url_for, session, flash,jsonify, Response, abort 
import pymysql
import msal
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os
import msal
import requests
from datetime import datetime
import io
import pytz
from pytz import timezone
import logging
from logging.handlers import RotatingFileHandler
from db_handler import DBLogHandler
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import ssl
import imaplib
from urllib.parse import urlparse
import pandas as pd
import cheroot.ssl.builtin

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_TYPE'] = 'filesystem'

# Azure AD Configuration
TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/getAToken"
SCOPE = ["User.Read", "Mail.Send","Calendars.ReadWrite","OnlineMeetings.ReadWrite"]
SHAREPOINT_SITE_ID = os.getenv("SHAREPOINT_SITE_ID")
EMPLOYEE_MASTER_LIST_ID = os.getenv("EMPLOYEE_MASTER_LIST_ID")
IMAP_SERVER = os.getenv("IMAP_SERVER")
IMAP_PORT = os.getenv("IMAP_PORT")

def get_otpluat_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default"
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

# DB Connection
def get_db_connection():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password=os.getenv('db_password'),
            database='hr_portal',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Database connection failed: {e}")
        return None

# MSAL setup
def build_msal_app():
    return msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY,
        client_credential=CLIENT_SECRET)



def build_auth_url():
    msal_app = build_msal_app()
    return msal_app.get_authorization_request_url(
        scopes=SCOPE,
        redirect_uri=url_for('auth_response', _external=True).replace("127.0.0.1", "localhost")
    )

# For logging all the steps
logger = logging.getLogger("AppLogger")
logger.setLevel(logging.INFO)

if not logger.handlers:
    # File handler
    file_handler = RotatingFileHandler("logs/app.log", maxBytes=1_000_000, backupCount=5)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # DB handler
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': os.getenv('db_password'),
        'database': 'hr_portal',
        'cursorclass': pymysql.cursors.DictCursor
    }

    db_handler = DBLogHandler(db_config)
    db_formatter = logging.Formatter("%(message)s")
    db_handler.setFormatter(db_formatter)
    logger.addHandler(db_handler)

# Background Schedular 
scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


# ------------------- Routes -------------------

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        logger.info(f"Login attempt for user: {email}")

        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
        conn.close()

        if user:
            # Check if the user is an SSO user (no password stored)
            if not user.get("password_hash"):
                logger.warning(f"SSO account login attempted via password by: {email}")
                flash("This account uses SSO. Please login using Azure.")
                return redirect(url_for('login'))

            # Validate password
            if password == user.get("password_hash"):
                logger.info(f"Login successful for user: {email}")
                session["user"] = {"email": user["email"], "name": user["name"], "role": user.get("role", "static")}
                return redirect(url_for('home'))
            else:
                logger.warning(f"Incorrect password for user: {email}")
                flash("Incorrect password.")
        else:
            logger.warning(f"Login failed. User not found: {email}")
            flash("User not found.")

    return render_template('login.html')

@app.route('/sso-login')
def sso_login():
    logger.info("SSO login initiated")
    return redirect(build_auth_url())

@app.route(REDIRECT_PATH)
def auth_response():
    code = request.args.get('code')
    logger.info("Received authorization code from Azure")
    msal_app = build_msal_app()
    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=SCOPE,
        redirect_uri=url_for('auth_response', _external=True).replace("127.0.0.1", "localhost")
    )

    if "access_token" in result:
        claims = result.get("id_token_claims")
        email = claims.get("preferred_username")
        name = claims.get("name")
        oid = claims.get("oid")

        if not email:
            flash("SSO Login failed: Email not found.")
            return redirect(url_for('login'))

        conn = get_db_connection()
        user_data = None

        if conn:
            with conn.cursor() as cursor:
                # Check if user exists
                cursor.execute("SELECT email, name, role FROM users WHERE email = %s", (email,))
                user_row = cursor.fetchone()

                if user_row:
                    logger.info(f"SSO user found in database: {email}")
                    # Existing user
                    user_data = {
                        "email": user_row["email"],
                        "name": user_row["name"],
                        "role": user_row["role"]
                    }
                else:
                    # New user — assign default role "HR"
                    logger.info(f"New SSO user, adding to database: {email}")
                    default_role = "requestor"
                    cursor.execute(
                        "INSERT INTO users (email, name, azure_oid, role) VALUES (%s, %s, %s, %s)",
                        (email, name, oid, default_role)
                    )
                    conn.commit()
                    user_data = {
                        "email": email,
                        "name": name,
                        "role": default_role
                    }

            conn.close()

        if user_data:
            session["user"] = user_data
            session["access_token"] = result["access_token"]
            logger.info(f"Session created for: {email}")
            return redirect(url_for('home'))
        
    logger.error("SSO Login failed: Token acquisition unsuccessful.")
    return "SSO Login failed", 401
    
    
# ------------------------------------------------------------------------------------#

#----------------------------- Ice warp login -------------------------#

def validate_icewarp_credentials(
    username,
    password,
    server=IMAP_SERVER,
    port=IMAP_PORT
):
    """Validate credentials against IceWarp IMAP server."""

    try:

        logger.info(
            f"Trying IceWarp IMAP: "
            f"server={server}, port={port}, user={username}"
        )

        context = ssl.create_default_context()

        # IceWarp server has self-signed certificate
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with imaplib.IMAP4_SSL(
            server,
            int(port),
            ssl_context=context,
            timeout=15
        ) as imap:

            imap.login(username, password)

            logger.info(
                f"IceWarp authentication successful for {username}"
            )

            return True

    except imaplib.IMAP4.error as e:

        logger.warning(
            f"IceWarp authentication failed for {username}: {e}"
        )

        return False

    except Exception as e:

        logger.exception(
            f"IceWarp connection error for {username}: {e}"
        )

        return False

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(target)
    return test_url.netloc == "" or test_url.netloc == ref_url.netloc

def get_employee_from_master(access_token, site_id, list_id, email):
    url = (
        f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/items"
        f"?$expand=fields&$filter=fields/Email eq '{email}'"
    )


    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(url, headers=headers)


    if resp.status_code != 200:
        return None

    items = resp.json().get("value", [])


    return items[0]["fields"] if items else None


@app.route("/icewarp_login", methods=["GET", "POST"])
def icewarp_login():
    """IceWarp login route"""

    if request.method == "GET":
        next_url = request.args.get("next", url_for("home"))
        return render_template("icewarp_login.html", next_url=next_url)

    # ---------------------------------------------------------
    # 1. Get login details
    # ---------------------------------------------------------
    email = request.form.get("username", "").strip().lower()
    password = request.form.get("password", "").strip()
    next_url = request.form.get("next", url_for("home"))

    logger.info(f"IceWarp login attempt for {email}")

    if not email or not password:
        flash("Please enter both email and password.", "error")
        return redirect(url_for("icewarp_login", next=next_url))

    # ---------------------------------------------------------
    # 2. Validate IceWarp credentials
    # ---------------------------------------------------------
    if not validate_icewarp_credentials(email, password):
        logger.warning(f"IceWarp authentication failed for {email}")
        flash("Invalid IceWarp username or password.", "error")
        return redirect(url_for("icewarp_login", next=next_url))

    logger.info(f"IceWarp authentication successful for {email}")

    # ---------------------------------------------------------
    # 3. Get Microsoft Graph token (for SharePoint check)
    # ---------------------------------------------------------
    try:
        access_token = get_otpluat_token()
        logger.info(f"Microsoft Graph token obtained for {email}")
    except Exception as e:
        logger.exception(f"Failed to get Microsoft Graph token for {email}: {e}")
        flash("Unable to connect to employee master. Please try again later.", "error")
        return redirect(url_for("icewarp_login", next=next_url))

    # ---------------------------------------------------------
    # 4. Check Employee Master (ONLY FOR AUTHORIZATION)
    # ---------------------------------------------------------
    site_id = SHAREPOINT_SITE_ID
    list_id = EMPLOYEE_MASTER_LIST_ID

    employee = get_employee_from_master(access_token, site_id, list_id, email)

    if not employee:
        logger.warning(f"Employee Master record not found for {email}")
        flash("Access denied. You are not authorized to use this application.", "error")
        return redirect(url_for("icewarp_login", next=next_url))

    logger.info(f"Employee Master record found for {email}")

    # ---------------------------------------------------------
    # 5. SIMPLE: Check if email exists in database
    # ---------------------------------------------------------
    conn = get_db_connection()

    if not conn:
        logger.error(f"Database connection failed for {email}")
        flash("Database connection error.", "error")
        return redirect(url_for("icewarp_login", next=next_url))

    user_data = None

    try:
        with conn.cursor() as cursor:
            # Check if user exists by email
            cursor.execute(
                """
                SELECT email, name, role
                FROM users
                WHERE LOWER(email) = LOWER(%s)
                """,
                (email,)
            )
            user_row = cursor.fetchone()

            # -------------------------------------------------
            # USER EXISTS - USE DATABASE ROLE
            # -------------------------------------------------
            if user_row:
                user_data = {
                    "email": user_row["email"].lower(),
                    "name": user_row["name"],
                    "role": user_row["role"] or "requestor"  # Use DB role, default to requestor if empty
                }
                logger.info(f"✅ User exists: {email}, Role: {user_data['role']}")

            # -------------------------------------------------
            # NEW USER - INSERT WITH REQUESTOR ROLE
            # -------------------------------------------------
            else:
                logger.info(f"New user: {email}")
                
                # Get name from SharePoint or create from email
                employee_name = employee.get("Name") or email.split("@")[0].replace(".", " ").title()
                
                # INSERT with requestor role (hardcoded as per your requirement)
                cursor.execute(
                    """
                    INSERT INTO users (email, name, role)
                    VALUES (%s, %s, %s)
                    """,
                    (email, employee_name, "requestor")
                )
                conn.commit()

                user_data = {
                    "email": email,
                    "name": employee_name,
                    "role": "requestor"
                }
                logger.info(f"✅ New user created: {email} with role: requestor")

    except Exception as e:
        logger.exception(f"Database error for {email}: {e}")
        conn.rollback()
        flash("Database error. Please contact administrator.", "error")
        return redirect(url_for("icewarp_login", next=next_url))
    finally:
        conn.close()

    # ---------------------------------------------------------
    # 6. CREATE SESSION
    # ---------------------------------------------------------
    session.clear()
    
    session["user"] = {
        "email": user_data["email"],
        "name": user_data["name"],
        "role": user_data["role"]  # Comes from database
    }
    
    session["email"] = user_data["email"]
    session["access_token"] = access_token

    logger.info(f"✅ Session created: {user_data['email']}, Role: {user_data['role']}")

    # ---------------------------------------------------------
    # 7. Redirect
    # ---------------------------------------------------------
    if next_url and is_safe_url(next_url):
        return redirect(next_url)

    return redirect(url_for("home"))
    
# ------------------------------------------------------------------------------------#
@app.route('/home')
def home():
    if 'user' not in session:
        logger.warning("Unauthorized access to /home. Redirecting to login.")
        return redirect(url_for('login'))

    user_role = session['user']['role']
    default_page = 'dashboard' if user_role != 'interviewer' else None
    page = request.args.get('page', default_page)

    if user_role == 'interviewer' and page is None:
        logger.info(f"Interviewer '{session['user']['email']}' landing redirected to interview_candidates.")
        return redirect(url_for('interviewer_candidates'))

    logger.info(f"User '{session['user']['email']}' with role '{user_role}' accessed /home with page: {page}")

    if user_role == 'interviewer' and page == 'dashboard':
        logger.info(f"Redirecting interviewer '{session['user']['email']}' to interview_candidates instead of dashboard.")
        return redirect(url_for('interview_candidates'))

    allowed_pages = {
        'manager': ['dashboard', 'requisition', 'repository', 'view_requisitions'],
        'hr': ['dashboard', 'repository', 'view_requisitions', 'requisition'],
        'hr lead': ['dashboard', 'requisition', 'repository', 'view_requisitions'],
        'interviewer': ['requisition', 'repository', 'view_requisitions'],
        'requestor' : ['dashboard', 'requisition', 'repository', 'view_requisitions']
    }

    all_pages = ['dashboard', 'requisition', 'repository', 'usermanagement', 'view_requisitions']
    allowed = all_pages if user_role == 'admin' else allowed_pages.get(user_role, [])

    if page not in allowed:
        logger.warning(f"User '{session['user']['email']}' attempted to access unauthorized page: {page}")
        page = 'notallowed'

    # 👉 Prepare context
    context = {
        "user": session['user'],
        "page": page
    }

    # 👉 Load departments only for requisition page

    if page == "requisition":
        departments, customers = get_departments_and_customers(
            r"C:\PythonApplication\HR Portal\Department and Cost Centre List.xlsx"
        )
        context["departments"] = departments
        context["customers"] = customers

    return render_template('home.html', **context)

def sp_get_list_items(list_id, filter_query=None):
    """Fetch all items from a SharePoint list using your existing get_otpluat_token()."""
    # Use your existing token generator
    access_token = get_otpluat_token()

    if not access_token:
        print("ERROR: Failed to retrieve access token")
        return []

    if not list_id:
        print("ERROR: list_id not provided")
        return []

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    graph_url = (
        f"https://graph.microsoft.com/v1.0/sites/"
        f"{SHAREPOINT_SITE_ID}/lists/{list_id}/items"
    )

    if filter_query:
        graph_url += f"?$expand=fields&$filter={filter_query}&$top=5000"
    else:
        graph_url += "?$expand=fields&$top=5000"

    all_items = []

    try:
        while graph_url:
            response = requests.get(graph_url, headers=headers)

            if response.status_code != 200:
                print(f"Error response: {response.status_code} - {response.text}")
                break

            data = response.json()

            items = data.get("value", [])
            for item in items:
                field_data = item.get("fields", {})
                field_data['id'] = item.get('id')
                all_items.append(field_data)

            graph_url = data.get("@odata.nextLink")

        return all_items

    except Exception as e:
        print(f"Error fetching list items: {e}")
        return []

    
def get_departments_and_customers(file_path=r"C:\PythonApplication\HR Portal\Department and Cost Centre List.xlsx"):
    departments = []
    customers = []

    # --- 1. Fetch Departments from SharePoint (Employee Master List) ---
    try:
        dept_items = sp_get_list_items(list_id=EMPLOYEE_MASTER_LIST_ID)
        dept_set = set()

        for item in dept_items:
            # Retrieves Department field from SharePoint items
            dept_val = item.get("Department")
            if dept_val:
                dept_set.add(str(dept_val).strip())

        departments = sorted(list(dept_set))

    except Exception as e:
        print(f"Error fetching departments from SharePoint: {e}")

    # --- 2. Fetch Customers from Local Excel (Sheet 2) ---
    try:
        df_cust = pd.read_excel(file_path, sheet_name=1)
        df_cust.columns = df_cust.columns.str.strip()

        if "customers" in df_cust.columns:
            customers = df_cust["customers"].dropna().astype(str).unique().tolist()
            customers = sorted(customers)
        else:
            print("Customer Name column not found in Sheet 2")

    except Exception as e:
        print(f"Error reading Excel file for customers: {e}")

    return departments, customers

@app.route('/dashboard_data')
def dashboard_data():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        # 1. Department Breakdown (Active/Open Requisitions)
        cursor.execute("""
            SELECT 
                department,
                COALESCE(SUM(number_of_openings), 0) AS total_openings,
                COALESCE(SUM(openings_filled), 0) AS total_filled
            FROM requisitions
            WHERE status NOT IN ('On Hold', 'Lost from Customer')
            GROUP BY department
            ORDER BY total_openings DESC
        """)
        dept_data = cursor.fetchall()

        departments = [row['department'] or 'Unassigned' for row in dept_data]
        openings = [int(row['total_openings']) for row in dept_data]
        filled = [int(row['total_filled']) for row in dept_data]

        # 2. Recruiter Workload (Joined via requisition_assignments table)
        cursor.execute("""
            SELECT 
                COALESCE(u.name, 'Unassigned') AS recruiter_name,
                COALESCE(SUM(r.number_of_openings), 0) AS total_openings,
                COALESCE(SUM(r.openings_filled), 0) AS total_filled
            FROM requisitions r
            LEFT JOIN requisition_assignments ra ON r.id = ra.requisition_id
            LEFT JOIN users u ON ra.assigned_to_email = u.email
            WHERE r.status NOT IN ('On Hold', 'Lost from Customer')
            GROUP BY recruiter_name
            ORDER BY total_openings DESC
        """)
        recruiter_data = cursor.fetchall()

        assigned_to = [row['recruiter_name'] for row in recruiter_data]
        assigned_openings = [int(row['total_openings']) for row in recruiter_data]
        assigned_filled = [int(row['total_filled']) for row in recruiter_data]

        # 3. Overall Metrics & Strategic KPIs
        cursor.execute("""
            SELECT 
                COUNT(id) AS total_reqs,
                SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) AS open_reqs,
                SUM(CASE WHEN status = 'Closed' THEN 1 ELSE 0 END) AS closed_reqs,
                SUM(CASE WHEN status = 'On Hold' THEN 1 ELSE 0 END) AS on_hold_reqs,
                COALESCE(SUM(number_of_openings), 0) AS total_openings,
                COALESCE(SUM(openings_filled), 0) AS total_filled,
                ROUND(AVG(COALESCE(ageing, DATEDIFF(CURDATE(), created_at))), 0) AS avg_ageing_days
            FROM requisitions
            WHERE status != 'Lost from Customer'
        """)
        metrics = cursor.fetchone() or {}

        # 4. Candidate Funnel Metrics
        cursor.execute("SELECT COUNT(*) AS total_candidates FROM candidates")
        cand_res = cursor.fetchone()
        total_candidates = cand_res['total_candidates'] if cand_res else 0

        return jsonify({
            'departments': departments,
            'openings': openings,
            'filled': filled,
            'assigned_to': assigned_to,
            'assigned_openings': assigned_openings,
            'assigned_filled': assigned_filled,
            'metrics': {
                'total_openings': int(metrics.get('total_openings') or 0),
                'total_filled': int(metrics.get('total_filled') or 0),
                'open_reqs': int(metrics.get('open_reqs') or 0),
                'closed_reqs': int(metrics.get('closed_reqs') or 0),
                'on_hold_reqs': int(metrics.get('on_hold_reqs') or 0),
                'avg_ageing_days': int(metrics.get('avg_ageing_days') or 0),
                'total_candidates': int(total_candidates)
            }
        })

    except Exception as e:
        logger.error(f"Error loading dashboard data: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


# ------------------------------------------------------------------------------------#
@app.route('/submit_requisition', methods=['GET', 'POST'])
def submit_requisition():
    data = request.form
    user_email = session['user']['email']
    logger.info(f"User '{user_email}' accessing submit_requisition route.")

    if request.method == 'POST':
        data = request.form
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                
                po_value = data.get('po_value', '').strip()
                if po_value == '':
                    po_value = None
                else:
                    po_value = float(po_value)
                # Insert requisition
                cursor.execute("""
                    INSERT INTO requisitions (
                        job_title, department, number_of_openings,
                        skills_required, location, hiring_type, replacement_for,
                        budget, job_description, po_value, created_by, customer_name
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    data['job_title'], data['department'], data['number_of_openings'],
                    data['skills_required'], data['location'], data['hiring_type'], data['replacement_for'],
                    data['budget'], data['job_description'], po_value, user_email, data['customer_name']
                ))
                requisition_id = conn.insert_id()
                logger.info(f"Inserted requisition ID: {requisition_id}")

                # Insert interview hierarchy
                levels = int(data['levels'])
                for i in range(1, levels + 1):
                    level_value = f"Level-{i}"
                    cursor.execute("""
                        INSERT INTO interview_hierarchy (
                            requisition_id, level, interviewer_name, interviewer_email
                        ) VALUES (%s, %s, %s, %s)
                    """, (
                        requisition_id, level_value,
                        data[f'interviewer_name_{i}'], data[f'interviewer_email_{i}']
                    ))
                    logger.info(f"Inserted {level_value} interviewer: {data[f'interviewer_email_{i}']}")

                # Insert department utilization
                department_count = int(data.get('utilization_levels', 0))
                for i in range(1, department_count + 1):
                    dept_name = data.get(f'util_department_{i}')
                    utilization = data.get(f'util_percent_{i}')
                    if dept_name and utilization:
                        cursor.execute("""
                            INSERT INTO department_utilization (
                                requisition_id, department_name, utilization
                            ) VALUES (%s, %s, %s)
                        """, (requisition_id, dept_name, utilization))
                        logger.info(f"Added department utilization: {dept_name} - {utilization}%")

            conn.commit()
            logger.info(f"Requisition {requisition_id} committed to the database.")

            # Send email
            success, message = send_requisition_email(data)
            if success:
                logger.info(f"Requisition email sent successfully for ID: {requisition_id}")
                flash('Requisition submitted and email sent successfully!')
            else:
                logger.warning(f"Email failed for requisition ID {requisition_id}: {message}")
                flash(f'Requisition submitted, but email failed: {message}')

        except Exception as e:
            logger.error(f"Error submitting requisition: {e}")
            conn.rollback()
            flash('An error occurred while submitting the requisition.')
        finally:
            conn.close()

        return redirect(url_for('home', page='requisition'))

    # GET request → render form with departments
    return render_template('requisition.html')

# ------------------------------------------------------------------------------------#
def send_requisition_email(requisition_data):
    access_token = session.get("access_token")
    user = session.get("user")

    if not access_token or not user:
        logger.error("Attempted to send email without authentication.")
        return False, "User not authenticated."

    # Connect to DB to get HR Leads and Admins
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT email FROM users WHERE role IN ('hr lead', 'admin', 'manager') AND is_active = 1")
            recipients = [row['email'] for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Failed to fetch HR Lead/Admin emails: {e}")
        return False, "Failed to fetch HR Lead/Admin emails."
    finally:
        conn.close()

    # Add the creator of the requisition if not already in the list
    if requisition_data.get('created_by') and requisition_data['created_by'] not in recipients:
        recipients.append(requisition_data['created_by'])

    if not recipients:
        logger.warning("No recipients found for requisition email.")
        return False, "No recipients found."

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    email_body = f"""
Hi Team,

A new requisition has been submitted by {user['name']}.

Job Title: {requisition_data['job_title']}
Department: {requisition_data['department']}
No. of Openings: {requisition_data['number_of_openings']}
Skills Required: {requisition_data['skills_required']}
Location: {requisition_data['location']}
Budget: {requisition_data['budget']}
Type: {requisition_data['hiring_type']}

Please revert back within 1 day if any missing information.

Regards,
{user['name']}
"""

    # Prepare recipients in Microsoft Graph format
    to_recipients = [{"emailAddress": {"address": email}} for email in recipients]

    message = {
        "message": {
            "subject": "New Hiring Requisition Submitted",
            "body": {
                "contentType": "Text",
                "content": email_body
            },
            "toRecipients": to_recipients
        },
        "saveToSentItems": "true"
    }

    response = requests.post(
        'https://graph.microsoft.com/v1.0/me/sendMail',
        headers=headers,
        json=message
    )

    if response.status_code == 202:
        logger.info(f"Email sent successfully to: {', '.join(recipients)}")
        return True, "Mail sent"
    else:
        logger.error(f"Failed to send email: {response.text}")
        return False, f"Failed to send mail: {response.text}"

# ------------------------------------------------------------------------------------#
# @app.route('/assign_requisition', methods=['GET', 'POST'])
# def assign_requisition():
#
#     if 'user' not in session or session['user']['role'] not in ['hr lead', 'admin']:
#         return redirect(url_for('home'))
#
#     user = session.get('user')
#     conn = get_db_connection()
#     requisitions = []
#     hr_users = []
#     success_message = None
#
#     try:
#         with conn.cursor() as cursor:
#
#             cursor.execute("""
#                 SELECT r.id, r.job_title, r.department, u.name AS created_by
#                 FROM requisitions r
#                 JOIN users u ON r.created_by = u.email
#                 WHERE r.assigned_to IS NULL
#                 ORDER BY r.created_at DESC
#             """)
#             requisitions = cursor.fetchall()
#
#
#             cursor.execute("SELECT id, name, email FROM users WHERE role = 'hr'")
#             hr_users = cursor.fetchall()
#
#
#             # Handle form submission (POST)
#             if request.method == 'POST':
#                 requisition_id = request.form['requisition_id']
#                 assigned_to = request.form['assigned_to']
#
#                 # Update the requisition assignment
#                 cursor.execute("""
#                     UPDATE requisitions
#                     SET assigned_to = %s
#                     WHERE id = %s
#                 """, (assigned_to, requisition_id))
#                 conn.commit()
#
#                 flash("Requisition successfully assigned!", "success")
#                 # Redirect to the same page to refresh and update the dropdown
#                 return redirect(url_for('assign_requisition'))
#
#     except Exception as e:
#         print("Error:", str(e))
#
#     finally:
#         conn.close()
#
#     return render_template('assign_requisition.html', requisitions=requisitions, hr_users=hr_users,  user=user)
# ------------------------------------------------------------------------------------#

@app.route('/view_requisitions')
def view_requisitions():
    if 'user' not in session:
        logging.warning("Unauthorized access to /view_requisitions")
        return redirect(url_for('home'))

    user = session['user']
    logging.info(f"User {user['email']} accessing /view_requisitions")
    conn = get_db_connection()
    requisitions = []

    try:
        with conn.cursor() as cursor:
            # 🔁 Update status column based on current openings_filled vs number_of_openings
            cursor.execute("""
                UPDATE requisitions
                SET status = CASE
                    WHEN openings_filled = number_of_openings THEN 'Closed'
                    ELSE 'Open'
                END,
                closed_at = CASE
                    WHEN openings_filled = number_of_openings AND closed_at IS NULL THEN CURRENT_TIMESTAMP
                    ELSE closed_at
                END
                WHERE status NOT IN ('On Hold', 'Lost from Customer');
            """)
            conn.commit()
            logging.info("Requisition statuses updated based on openings_filled")

            # 2) Freeze ageing for newly closed requisitions
            cursor.execute("""
                UPDATE requisitions
                SET ageing = DATEDIFF(CURDATE(), created_at)
                WHERE status = 'Closed' AND ageing IS NULL;
            """)
            conn.commit()
            logging.info("Ageing frozen for closed requisitions")

            # 3) Fetch requisitions
            if user['role'] in ['admin', 'manager','hr lead']:
                logging.info(f"{user['email']} fetching all requisitions (Role: {user['role']})")
                cursor.execute("""
                    SELECT 
                        r.*,
                        u1.name AS created_by_name,
                        GROUP_CONCAT(DISTINCT u2.name) AS assigned_to_names,
                        GROUP_CONCAT(DISTINCT ra.assigned_to_email) AS assigned_to_emails,
                        COALESCE(r.ageing, DATEDIFF(CURDATE(), r.created_at)) AS ageing
                    FROM requisitions r
                    LEFT JOIN users u1 ON r.created_by = u1.email
                    LEFT JOIN requisition_assignments ra ON ra.requisition_id = r.id
                    LEFT JOIN users u2 ON ra.assigned_to_email = u2.email
                    GROUP BY r.id
                    ORDER BY r.created_at;
                """)
            else:
                logging.info(f"{user['email']} fetching assigned requisitions")
                cursor.execute("""
                    SELECT 
                        r.*,
                        u1.name AS created_by_name,
                        GROUP_CONCAT(DISTINCT u2.name) AS assigned_to_names,
                        GROUP_CONCAT(DISTINCT ra.assigned_to_email) AS assigned_to_emails,
                        COALESCE(r.ageing, DATEDIFF(CURDATE(), r.created_at)) AS ageing
                    FROM requisitions r
                    LEFT JOIN users u1 ON r.created_by = u1.email
                    LEFT JOIN requisition_assignments ra ON ra.requisition_id = r.id
                    LEFT JOIN users u2 ON ra.assigned_to_email = u2.email
                    WHERE ra.assigned_to_email = %s
                    GROUP BY r.id
                    ORDER BY r.created_at;
                """, (user['email'],))
            requisitions = cursor.fetchall()

    except Exception as e:
        logging.error(f"Error in view_requisitions: {e}")
        flash("Something went wrong fetching requisitions", "danger")
    finally:
        conn.close()

    return render_template('view_requisitions.html', requisitions=requisitions, user=user)


# ------------------------------------------------------------------------------------#


@app.route('/requisition/<int:requisition_id>', methods=['GET', 'POST'])
def view_requisition_details(requisition_id):
    if 'user' not in session:
        logging.warning("Unauthorized access to requisition details")
        return redirect(url_for('home'))

    user = session['user']
    logging.info(f"{user['email']} accessing requisition ID {requisition_id}")
    conn = get_db_connection()

    requisition = None
    hr_users = []
    assigned_users = []
    assigned_user_emails = []
    utilization_data = []
    interview_hierarchy = []

    try:
        with conn.cursor() as cursor:

            cursor.execute("SELECT * FROM requisitions WHERE id = %s", (requisition_id,))
            requisition = cursor.fetchone()
            logging.debug(f"Raw requisition data: {requisition}")
            

            # Fetch requisition with creator/assignee info
            cursor.execute("""
                SELECT r.*, u1.name AS created_by_name, u2.name AS assigned_to_name
                FROM requisitions r
                LEFT JOIN users u1 ON r.created_by = u1.email
                LEFT JOIN users u2 ON r.assigned_to = u2.email
                WHERE r.id = %s
            """, (requisition_id,))
            requisition = cursor.fetchone()

            if not requisition:
                conn.close()  # explicitly close connection here since finally block might not be reached due to return
                flash("Requisition not found", "warning")
                return redirect(url_for('view_requisitions'))


            # Fetch list of assigned HRs from requisition_assignments table
            cursor.execute("""
                SELECT u.name, u.email
                FROM requisition_assignments ra
                JOIN users u ON ra.assigned_to_email = u.email
                WHERE ra.requisition_id = %s
            """, (requisition_id,))
            assigned_users = cursor.fetchall()
            assigned_user_emails = [u['email'] for u in assigned_users]

            # Fetch all HR users for assignment
            if user['role'] in ['admin', 'hr lead']:
                cursor.execute("SELECT name, email FROM users WHERE role = 'hr'")
                hr_users = cursor.fetchall()

            # Handle assignment form submission
            if request.method == 'POST' and user['role'] in ['admin', 'hr lead']:
                selected_emails = request.form.getlist('assigned_to')

                # Remove existing assignments
                cursor.execute("DELETE FROM requisition_assignments WHERE requisition_id = %s", (requisition_id,))

                # Insert new assignments
                for email in selected_emails:
                    cursor.execute("""
                        INSERT INTO requisition_assignments (requisition_id, assigned_to_email,  assigned_by_email)
                        VALUES (%s, %s, %s)
                    """, (requisition_id, email, user['email']))

                    logging.info(f"{user['email']} assigned requisition ID {requisition_id} to {email}")

                conn.commit()
                flash("Requisition successfully assigned to selected HRs!", "success")

                if selected_emails:
                    send_assignment_email(requisition, selected_emails, user['name'])

                return redirect(url_for('view_requisition_details', requisition_id=requisition_id))

            # Fetch department utilization
            cursor.execute("""
                SELECT department_name, utilization
                FROM department_utilization
                WHERE requisition_id = %s
            """, (requisition_id,))
            utilization_data = cursor.fetchall()

            # Fetch interview hierarchy
            cursor.execute("""
                SELECT level, interviewer_name, interviewer_email
                FROM interview_hierarchy
                WHERE requisition_id = %s
                ORDER BY level ASC
            """, (requisition_id,))
            interview_hierarchy = cursor.fetchall()

    except Exception as e:
        logging.error(f"Error fetching requisition details: {e}")
        flash("Error loading requisition details", "danger")
    finally:
        conn.close()

    return render_template(
        'requisition_details.html',
        requisition=requisition,
        hr_users=hr_users,
        user=user,
        utilization_data=utilization_data,
        interview_hierarchy=interview_hierarchy,
        assigned_users=assigned_users,
        assigned_user_emails=assigned_user_emails
    )

def send_assignment_email(requisition_data, assigned_emails, assigned_by_name):
    access_token = session.get("access_token")
    if not access_token:
        logger.error("Attempted to send email without authentication.")
        return False, "User not authenticated."

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    email_body = f"""
Hi HR Team,

You have been assigned a new requisition by {assigned_by_name}.

Job Title: {requisition_data['job_title']}
Department: {requisition_data['department']}
No. of Openings: {requisition_data['number_of_openings']}
Skills Required: {requisition_data['skills_required']}
Location: {requisition_data['location']}
Budget: {requisition_data['budget']}
Type: {requisition_data['hiring_type']}

Please take the necessary action.

Regards,
{assigned_by_name}
"""

    # Prepare recipients for Microsoft Graph
    to_recipients = [{"emailAddress": {"address": email}} for email in assigned_emails]

    message = {
        "message": {
            "subject": "New Requisition Assigned",
            "body": {
                "contentType": "Text",
                "content": email_body
            },
            "toRecipients": to_recipients
        },
        "saveToSentItems": "true"
    }

    response = requests.post(
        'https://graph.microsoft.com/v1.0/me/sendMail',
        headers=headers,
        json=message
    )

    if response.status_code == 202:
        logger.info(f"Assignment email sent successfully to: {', '.join(assigned_emails)}")
        return True, "Mail sent"
    else:
        logger.error(f"Failed to send email: {response.text}")
        return False, f"Failed to send mail: {response.text}"


@app.route('/requisition/<int:requisition_id>/edit', methods=['GET', 'POST'])
def edit_requisition(requisition_id):
    user = session.get('user')
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            if request.method == 'POST':
                form = request.form
                manual_status = form.get("status")

                allowed_manual_statuses = ['On Hold', 'Lost from Customer']
                if manual_status not in allowed_manual_statuses:
                    # Preserve original status if manual_status is empty or invalid
                    cursor.execute("SELECT status FROM requisitions WHERE id = %s", (requisition_id,))
                    current_req = cursor.fetchone()
                    manual_status = current_req['status'] if current_req else 'Pending'

                # --- Update requisition table ---
                cursor.execute("""
                    UPDATE requisitions SET
                        job_title = %s, department = %s, number_of_openings = %s,
                        skills_required = %s, location = %s, hiring_type = %s,
                        budget = %s, job_description = %s, customer_name = %s, status = %s
                    WHERE id = %s
                """, (
                    form['job_title'], form['department'], form['number_of_openings'],
                    form['skills_required'], form['location'], form['hiring_type'],
                    form['budget'], form['job_description'], form['customer_name'], manual_status, requisition_id
                ))

                # --- Department Utilization Incremental Update ---
                cursor.execute(
                    "SELECT id, department_name, utilization FROM department_utilization WHERE requisition_id = %s",
                    (requisition_id,))
                existing_utilization = cursor.fetchall()

                # Convert existing numbers to string for strict key comparison with string form inputs
                existing_util_map = {(row['department_name'], str(row['utilization'])): row['id'] for row in
                                     existing_utilization}
                submitted_utils = set()

                count_util = int(form.get('utilization_count', 0))
                for i in range(1, count_util + 1):
                    dept = form.get(f'department_name_{i}')
                    util = form.get(f'utilization_{i}')
                    if dept and util:
                        key = (dept, str(util))
                        submitted_utils.add(key)

                        if key not in existing_util_map:
                            # New record to insert
                            cursor.execute("""
                                INSERT INTO department_utilization (requisition_id, department_name, utilization)
                                VALUES (%s, %s, %s)
                            """, (requisition_id, dept, util))

                # Delete removed ones
                for key, record_id in existing_util_map.items():
                    if key not in submitted_utils:
                        cursor.execute("DELETE FROM department_utilization WHERE id = %s", (record_id,))

                # --- Interview Hierarchy Incremental Update ---
                cursor.execute(
                    "SELECT id, level, interviewer_name, interviewer_email FROM interview_hierarchy WHERE requisition_id = %s",
                    (requisition_id,))
                existing_hierarchy = cursor.fetchall()

                existing_hierarchy_map = {(row['level'], row['interviewer_name'], row['interviewer_email']): row['id']
                                          for row in existing_hierarchy}
                submitted_hierarchy = set()

                count_hierarchy = int(form.get('hierarchy_count', 0))
                for i in range(1, count_hierarchy + 1):
                    name = form.get(f'interviewer_name_{i}')
                    email = form.get(f'interviewer_email_{i}')
                    if name and email:
                        level_label = f"Level-{i}"  # store as Level-1, Level-2
                        key = (level_label, name, email)
                        submitted_hierarchy.add(key)

                        if key not in existing_hierarchy_map:
                            cursor.execute("""
                                INSERT INTO interview_hierarchy (requisition_id, level, interviewer_name, interviewer_email)
                                VALUES (%s, %s, %s, %s)
                            """, (requisition_id, level_label, name, email))

                # Delete removed ones
                for key, record_id in existing_hierarchy_map.items():
                    if key not in submitted_hierarchy:
                        cursor.execute("DELETE FROM interview_hierarchy WHERE id = %s", (record_id,))

                conn.commit()
                flash("Requisition updated successfully!", "success")
                return redirect(url_for('view_requisitions'))

            # --- GET request - load data to edit ---
            cursor.execute("SELECT * FROM requisitions WHERE id = %s", (requisition_id,))
            requisition = cursor.fetchone()

            cursor.execute("SELECT * FROM department_utilization WHERE requisition_id = %s", (requisition_id,))
            department_utilization = cursor.fetchall()

            # fetch hierarchy sorted numerically by level number
            cursor.execute("""
                SELECT * FROM interview_hierarchy 
                WHERE requisition_id = %s 
                ORDER BY CAST(SUBSTRING_INDEX(level, '-', -1) AS UNSIGNED) ASC
            """, (requisition_id,))
            interview_hierarchy = cursor.fetchall()

            # Fetch existing options for dropdowns & datalist
            cursor.execute(
                "SELECT DISTINCT department_name FROM department_utilization WHERE department_name IS NOT NULL AND department_name != ''")
            departments_db = [row['department_name'] for row in cursor.fetchall()]

            # Fallback default list if database list is small
            default_departments = ["Engineering", "HR", "Sales", "Marketing", "Finance", "Operations", "IT"]
            departments = list(set(departments_db + default_departments))
            departments.sort()

            cursor.execute(
                "SELECT DISTINCT customer_name FROM requisitions WHERE customer_name IS NOT NULL AND customer_name != ''")
            customers = [row['customer_name'] for row in cursor.fetchall()]

    except Exception as e:
        logger.error(f"Error in edit_requisition: {e}")
        flash("Something went wrong while editing the requisition.", "danger")
        return redirect(url_for('home'))
    finally:
        conn.close()

    return render_template("edit_requisition.html",
                           requisition=requisition,
                           department_utilization=department_utilization,
                           interview_hierarchy=interview_hierarchy,
                           departments=departments,
                           customers=customers,
                           user=user)



# Helper function to check TAT breach
def check_tat_breach(requisition):
    created_at = requisition.get("created_at")
    comments_updated_at = requisition.get("comments_updated_at")

    if not created_at or not comments_updated_at:
        return False  # Cannot check

    # Convert to datetime if strings
    if isinstance(created_at, str):
        created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
    if isinstance(comments_updated_at, str):
        comments_updated_at = datetime.strptime(comments_updated_at, "%Y-%m-%d %H:%M:%S")

    time_diff = comments_updated_at - created_at
    return time_diff > timedelta(days=1)

@app.route('/update_comments/<int:requisition_id>', methods=['POST'])
def update_comments(requisition_id):
    from datetime import datetime

    comments = request.form.get('comments')
    user = session.get("user")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Update comments and timestamp
        cursor.execute("""
            UPDATE requisitions 
            SET comments = %s, comments_updated_at = %s 
            WHERE id = %s
        """, (comments, datetime.now(), requisition_id))
        conn.commit()

        logger.info(f"Comments updated for requisition ID {requisition_id} by user {user['email'] if user else 'Unknown'}. Comment: {comments}")

        # Fetch updated requisition data
        cursor.execute("SELECT * FROM requisitions WHERE id = %s", (requisition_id,))
        requisition = cursor.fetchone()

        # Check for TAT breach
        if requisition and check_tat_breach(requisition):
            logger.warning(f"TAT breached for requisition ID {requisition_id} by {requisition.get('assigned_to')}")

    except Exception as e:
        logger.error(f"Error updating comments for requisition ID {requisition_id}: {str(e)}")
        flash("An error occurred while updating comments.", "danger")
        conn.rollback()
        return redirect(url_for('edit_requisition', requisition_id=requisition_id))

    finally:
        conn.close()

    # Send email to the 'created_by' user
    success, msg = send_comment_update_email(requisition)

    if success:
        logger.info(f"Comment update email sent successfully to {requisition['created_by']} for requisition ID {requisition_id}")
    else:
        logger.error(f"Failed to send comment update email for requisition ID {requisition_id}: {msg}")

    flash("Comments updated successfully." + (" Email sent." if success else " " + msg), "success" if success else "danger")
    return redirect(url_for('edit_requisition', requisition_id=requisition_id))



def send_comment_update_email(requisition_data):
    access_token = session.get("access_token")
    user = session.get("user")

    if not access_token or not user:
        logger.error("Attempted to send comment update email without authentication.")
        return False, "User not authenticated."

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    email_body = f"""
Hi {requisition_data['created_by']},

Your requisition for the position "{requisition_data['job_title']}" has been updated with the following comment:

------------------------------------------------------
{requisition_data['comments']}
------------------------------------------------------

Updated by: {user['name']} ({user['email']})

Regards,
HR System
"""

    message = {
        "message": {
            "subject": f"Comment Added to Requisition - {requisition_data['job_title']}",
            "body": {
                "contentType": "Text",
                "content": email_body
            },
            "toRecipients": [
                {"emailAddress": {"address": requisition_data['created_by']}}
            ]
        },
        "saveToSentItems": "true"
    }

    response = requests.post(
        'https://graph.microsoft.com/v1.0/me/sendMail',
        headers=headers,
        json=message
    )

    if response.status_code == 202:
        logger.info(f"Comment update email sent to {requisition_data['created_by']}")
        return True, "Email sent successfully"
    else:
        logger.error(f"Failed to send comment update email: {response.text}")
        return False, f"Failed to send email: {response.text}"




# ------------------------------------------------------------------------------------#
@app.route('/user_management')
def user_management():
    print("Session contents:", session)
    user = session.get('user')
    logging.info(f"{user['email']} accessing user management")
    print(user)
    email = session['user']['email']
    print ("Email", email)
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            db_users = cursor.fetchall()
            logging.info(f"Fetched {len(db_users)} users for management view")
    finally:
        connection.close()
    return render_template('user_management.html', users=db_users,user=user)

# Route: Update role
@app.route('/update-role/<int:user_id>', methods=['POST'])
def update_role(user_id):
    new_role = request.form.get('role')

    if not new_role:
        logging.warning(f"Attempt to update role for user {user_id} with invalid role")
        flash("Invalid role selected.", "danger")
        return redirect(url_for('user_management'))

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
        connection.commit()
        logging.info(f"User ID {user_id} role updated to {new_role}")
        flash("Role updated successfully.", "success")
    finally:
        connection.close()

    return redirect(url_for('user_management'))

# ------------------------------------------------------------------------------------#

def get_requisitions(email, role):
    logging.info(f"Fetching requisitions for {email} (Role: {role})")
    connection = get_db_connection()
    with connection.cursor() as cursor:
        if role in ['admin', 'hr lead','manager']:
            cursor.execute("""
                SELECT r.id, r.job_title, r.department, r.customer_name, 
                       r.number_of_openings, r.openings_filled
                FROM requisitions r
                ORDER BY r.created_at DESC
            """)
        else:
            cursor.execute("""
                SELECT r.id, r.job_title, r.department, r.customer_name, 
                       r.number_of_openings, r.openings_filled
                FROM requisitions r
                JOIN requisition_assignments ra ON r.id = ra.requisition_id
                WHERE ra.assigned_to_email = %s
                ORDER BY r.created_at DESC
            """, (email,))
        
        requisitions = cursor.fetchall()
        logging.info(f"Found {len(requisitions)} requisitions")
    
    connection.close()
    return requisitions



@app.route('/submit_candidate', methods=['GET', 'POST'])
def submit_candidate():
    logging.info("Accessed /submit_candidate route")

    if 'user' not in session:
        logging.warning("Unauthorized access attempt to submit_candidate")
        return redirect(url_for('home'))

    user_id = session['user']['email']
    user = session['user']['role']
    requisitions = get_requisitions(user_id, user)

    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            skills = request.form['skills']
            requisition_id = request.form['requisition_id']
            years = int(request.form.get('total_exp_years', 0))
            months = int(request.form.get('total_exp_months', 0))
            total_exp = years * 12 + months  # store total experience in months
            current_loc = request.form['current_loc']
            current_ctc = request.form['current_ctc']
            exp_ctc = request.form['exp_ctc']
            source = request.form['source']
            designation = request.form['designation']
            notice_period = request.form['notice_period']
            reason_for_change = request.form['reason_for_change']
            holding_other_offer = request.form['holding_other_offer']

            if source == "Other":
                source = request.form.get("other_source")

            if 'resume' not in request.files:
                return jsonify({"status": "error", "message": "Resume is required"}), 400

            resume_file = request.files['resume']
            resume_blob = resume_file.read()

            allowed_ids = [str(r['id']) for r in requisitions]
            if requisition_id not in allowed_ids:
                return jsonify({"status": "error", "message": "Unauthorized requisition access"}), 403

            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO candidates (
                        name, email, phone, skills, requisition_id, resume, submitted_by,
                        total_exp, current_loc, current_ctc, exp_ctc, source,
                        designation, notice_period, reason_for_change, holding_other_offer
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    name, email, phone, skills, requisition_id, resume_blob, user_id,
                    total_exp, current_loc, current_ctc, exp_ctc, source,
                    designation, notice_period, reason_for_change, holding_other_offer
                ))
                connection.commit()
            connection.close()

            logging.info(f"Candidate {name} submitted successfully by {user_id}")
            return jsonify({"status": "success"}), 200

        except Exception as e:
            logging.exception("Error while submitting candidate")
            return jsonify({"status": "error", "message": str(e)}), 500

    return render_template('submit_candidate.html', requisitions=requisitions, user=session['user'])

@app.route('/update_candidate/<int:id>', methods=['POST'])
def update_candidate(id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Collect form data
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            skills = request.form['skills']
            years = int(request.form.get('total_exp_years', 0))
            months = int(request.form.get('total_exp_months', 0))
            total_exp = years * 12 + months  # store total experience in months
            current_loc = request.form['current_loc']
            current_ctc = request.form['current_ctc']
            exp_ctc = request.form['exp_ctc']
            designation = request.form['designation']
            notice_period = request.form['notice_period']
            reason_for_change = request.form['reason_for_change']
            holding_other_offer = request.form['holding_other_offer']
            source = request.form['source']
            if source == "Other":
                source = request.form.get("other_source")

            resume_blob = None
            if 'resume' in request.files and request.files['resume'].filename:
                resume_file = request.files['resume']
                resume_blob = resume_file.read()

            # Build update query
            query = """
                UPDATE candidates 
                SET name=%s, email=%s, phone=%s, skills=%s, total_exp=%s,
                    current_loc=%s, current_ctc=%s, exp_ctc=%s, designation=%s,
                    notice_period=%s, reason_for_change=%s, holding_other_offer=%s,
                    source=%s
                    {resume_clause}
                WHERE id=%s
            """
            # If resume uploaded, include it in query
            if resume_blob:
                resume_clause = ", resume=%s"
                params = (name, email, phone, skills, total_exp, current_loc, current_ctc, exp_ctc,
                          designation, notice_period, reason_for_change, holding_other_offer,
                          source, resume_blob, id)
            else:
                resume_clause = ""
                query = query.format(resume_clause="")
                params = (name, email, phone, skills, total_exp, current_loc, current_ctc, exp_ctc,
                          designation, notice_period, reason_for_change, holding_other_offer,
                          source, id)
                conn.commit()
            
            cursor.execute(query.format(resume_clause=resume_clause), params)
            conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    except Exception as e:
        logging.exception("Error updating candidate")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/check_candidate', methods=['POST'])
def check_candidate():
    name = request.json.get("name")
    email = request.json.get("email")
    phone = request.json.get("phone")

    if not (name or email or phone):
        return jsonify({"status": "error", "message": "At least one of name, email, or phone is required"}), 400

    try:
        conn = get_db_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT id, name, email, phone, skills, designation 
                FROM candidates 
                WHERE name = %s OR email = %s OR phone = %s
            """, (name, email, phone))
            candidate = cursor.fetchone()
        conn.close()

        if candidate:
            return jsonify({"status": "found", "candidate": candidate}), 200
        else:
            return jsonify({"status": "not_found"}), 200

    except Exception as e:
        logging.exception("Error while checking candidate")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/get_candidate/<int:id>', methods=['GET'])
def get_candidate(id):
    try:
        conn = get_db_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT id, name, email, phone, skills, total_exp, current_loc, 
                       current_ctc, exp_ctc, designation, notice_period, 
                       reason_for_change, holding_other_offer, source 
                FROM candidates WHERE id = %s
            """, (id,))
            candidate = cursor.fetchone()
        conn.close()

        if candidate:
            return jsonify({"status": "success", "candidate": candidate})
        else:
            return jsonify({"status": "error", "message": "Candidate not found"}), 404
    except Exception as e:
        logging.exception("Error fetching candidate")
        return jsonify({"status": "error", "message": str(e)}), 500



# ------------------------------------------------------------------------------------#
@app.route('/view_candidates')
def view_candidates():
    logging.info("Accessed /view_candidates route")

    if 'user' not in session:
        logging.warning("Unauthorized access attempt to view_candidates")
        return redirect(url_for('home'))

    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            user_role = session['user']['role']
            user_email = session['user']['email']
            logging.info(f"{user_email} ({user_role}) is viewing candidates")

            base_query = """
                SELECT 
                    c.id, c.name, c.email, c.phone, u.name AS shortlisted_by, c.shortlisted_on,
                    c.submitted_by, c.is_shortlisted, c.selection_status,
                    r.job_title AS requisition_title,
                    c.offer_letter IS NOT NULL AS offer_exists,
                    (
                        SELECT COUNT(*) 
                        FROM interview_hierarchy ih 
                        WHERE ih.requisition_id = c.requisition_id
                    ) AS total_levels,
                    (
                        SELECT COUNT(*) 
                        FROM ratings ra 
                        WHERE ra.candidate_id = c.id AND ra.status IN ('selected', 'rejected')
                    ) AS completed_levels,
                    (
                        SELECT COUNT(*) 
                        FROM ratings ra 
                        WHERE ra.candidate_id = c.id AND ra.status = 'rejected'
                    ) AS rejected_levels
                FROM candidates c
                JOIN requisitions r ON c.requisition_id = r.id
                LEFT JOIN users u ON c.shortlisted_by = u.id
                {where_clause}
            """


            if user_role  in ['hr','requestor']:
                where_clause = "WHERE c.submitted_by = %s"
                cursor.execute(base_query.format(where_clause=where_clause), (user_email,))
            else:
                where_clause = ""
                cursor.execute(base_query.format(where_clause=where_clause))

            candidates = cursor.fetchall()
            logging.info(f"Retrieved {len(candidates)} candidates")

    except Exception as e:
        logging.exception("Error while fetching candidates:")
        return "Error loading candidates", 500
    finally:
        conn.close()

    return render_template('view_candidates.html', candidates=candidates, user=session['user'])



@app.route('/update_selection_status/<int:candidate_id>', methods=['POST'])
def update_selection_status(candidate_id):
    logging.info(f"Accessed update_selection_status for candidate ID: {candidate_id}")

    data = request.get_json()
    new_status = data.get('selection_status')

    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # Fetch current candidate info
            cursor.execute("""
                SELECT c.selection_status, c.requisition_id, r.job_title, r.department,
                       r.number_of_openings, r.openings_filled, r.created_by
                FROM candidates c
                JOIN requisitions r ON c.requisition_id = r.id
                WHERE c.id = %s
            """, (candidate_id,))
            candidate = cursor.fetchone()

            if not candidate:
                logging.warning(f"No candidate found with ID {candidate_id}")
                return jsonify({'success': False, 'message': 'Candidate not found'})

            current_status = candidate['selection_status']
            requisition_id = candidate['requisition_id']

            # Update only if status is changing
            if current_status != new_status:

                # 🔥 Track timestamp for Did Not Join in candidates table
                if new_status == 'Did Not Join':
                    cursor.execute("""
                        UPDATE candidates 
                        SET selection_status = %s, did_not_join_date = NOW()
                        WHERE id = %s
                    """, (new_status, candidate_id))
                    logging.info(f"Candidate {candidate_id} marked as Did Not Join at {datetime.now()}")
                else:
                    # Normal status update without timestamp
                    cursor.execute(
                        "UPDATE candidates SET selection_status = %s WHERE id = %s",
                        (new_status, candidate_id)
                    )

                # Handle openings_filled changes
                if new_status == 'Selected' and current_status != 'Selected':
                    # Candidate newly selected → increment
                    cursor.execute("""
                        UPDATE requisitions
                        SET openings_filled = openings_filled + 1
                        WHERE id = %s AND openings_filled < number_of_openings
                    """, (requisition_id,))
                    logging.info(f"Incremented openings_filled for requisition {requisition_id}")

                elif current_status == 'Selected' and new_status != 'Selected':
                    # 🔥 Candidate backed out → decrement, reopen, and track reopened date
                    cursor.execute("""
                        UPDATE requisitions
                        SET openings_filled = openings_filled - 1,
                            status = 'Open',
                            closed_at = NULL,
                            reopened_at = NOW()
                        WHERE id = %s AND openings_filled > 0
                    """, (requisition_id,))
                    logging.info(f"Requisition {requisition_id} reopened at {datetime.now()}")

                conn.commit()

                # Fetch updated requisition info
                cursor.execute("""
                    SELECT number_of_openings, openings_filled, created_by, job_title, department
                    FROM requisitions
                    WHERE id = %s
                """, (requisition_id,))
                requisition = cursor.fetchone()

                # Send email notification
                cursor.execute("SELECT email FROM users WHERE role IN ('hr lead', 'admin')")
                recipients = [row['email'] for row in cursor.fetchall()]

                if requisition['created_by'] not in recipients:
                    recipients.append(requisition['created_by'])

                # Prepare email content
                if new_status == 'Selected':
                    status_msg = f"Candidate SELECTED for '{requisition['job_title']}'. {requisition['openings_filled']} out of {requisition['number_of_openings']} positions filled."
                elif current_status == 'Selected' and new_status != 'Selected':
                    if new_status == 'Did Not Join':
                        status_msg = f"⚠️ Candidate DID NOT JOIN after selection for '{requisition['job_title']}'. Position is now OPEN again. {requisition['openings_filled']} out of {requisition['number_of_openings']} positions currently filled."
                    else:
                        status_msg = f"Candidate selection REVERSED (now {new_status}) for '{requisition['job_title']}'. {requisition['openings_filled']} out of {requisition['number_of_openings']} positions now filled. Requisition REOPENED."
                else:
                    status_msg = f"Candidate status changed to {new_status}"

                email_body = f"""
Hi Team,

Candidate status updated from '{current_status}' to '{new_status}'.

{status_msg}

Regards,
HR Portal System
"""

                # Send email via Microsoft Graph
                access_token = session.get("access_token")
                if access_token and recipients:
                    headers = {
                        'Authorization': f'Bearer {access_token}',
                        'Content-Type': 'application/json'
                    }
                    to_recipients = [{"emailAddress": {"address": email}} for email in recipients]

                    message = {
                        "message": {
                            "subject": f"Candidate Selection Update - {requisition['job_title']}",
                            "body": {
                                "contentType": "Text",
                                "content": email_body
                            },
                            "toRecipients": to_recipients
                        },
                        "saveToSentItems": "true"
                    }

                    response = requests.post(
                        'https://graph.microsoft.com/v1.0/me/sendMail',
                        headers=headers,
                        json=message
                    )
                    if response.status_code == 202:
                        logging.info(f"Selection update email sent to: {', '.join(recipients)}")
                    else:
                        logging.error(f"Failed to send selection email: {response.text}")

            else:
                conn.commit()

            logging.info(f"Updated candidate {candidate_id} status from '{current_status}' to '{new_status}'")
            return jsonify({'success': True})

    except Exception as e:
        conn.rollback()
        logging.exception(f"Failed to update selection status for candidate {candidate_id}")
        return jsonify({'success': False, 'message': 'Database error'})

    finally:
        conn.close()



@app.route('/interviewer_candidates')
def interviewer_candidates():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']
    email = user['email']
    role = user['role']

    if role != 'interviewer':
        return "Access Denied", 403

    query = """
        SELECT c.*, r.job_title AS requisition_title
        FROM candidates c
        JOIN interview_schedule i ON c.id = i.candidate_id
        JOIN requisitions r ON c.requisition_id = r.id
        WHERE i.interviewer_email = %s
        ORDER BY i.interview_datetime
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (email,))
    candidates = cursor.fetchall()
    cursor.close()

    return render_template('interviewer_candidates.html', candidates=candidates, user=user)



@app.route('/update_onboarding/<int:candidate_id>', methods=['POST'])
def update_onboarding(candidate_id):
    user = session.get('user')
    access_token = session.get("access_token")

    final_ctc             = request.form.get('final_ctc')
    planned_joining_date  = request.form.get('planned_joining_date')
    offer_file            = request.files.get('offer_letter')
    offer_letter_date     = datetime.now() if offer_file and offer_file.filename else None

    logger.info(f"{user['email']} is updating onboarding for candidate {candidate_id}")

    conn = get_db_connection()
    candidate_name, requisition_id, recipients = None, None, []
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 🔹 Get candidate info + requisition_id
            cursor.execute("SELECT id, name, requisition_id FROM candidates WHERE id = %s", (candidate_id,))
            candidate = cursor.fetchone()
            if not candidate:
                return jsonify(success=False, error="Candidate not found")

            candidate_name = candidate["name"]
            requisition_id = candidate["requisition_id"]

            # 🔹 Update candidate onboarding fields
            if offer_file and offer_file.filename:
                offer_blob = offer_file.read()
                cursor.execute("""
                    UPDATE candidates
                    SET final_ctc = %s,
                        planned_joining_date = %s,
                        offer_letter = %s,
                        offer_letter_date = %s
                    WHERE id = %s
                """, (
                    final_ctc or None,
                    planned_joining_date or None,
                    offer_blob,
                    offer_letter_date,
                    candidate_id
                ))
            else:
                cursor.execute("""
                    UPDATE candidates
                    SET final_ctc = %s,
                        planned_joining_date = %s,
                        offer_letter_date = %s
                    WHERE id = %s
                """, (
                    final_ctc or None,
                    planned_joining_date or None,
                    offer_letter_date,
                    candidate_id
                ))

            conn.commit()

            # 🔹 Fetch HR Lead (from users table), assigned_to_email, assigned_by_email
            cursor.execute("""
                SELECT DISTINCT u.email
                FROM users u
                WHERE u.role = 'hr lead'
                UNION
                SELECT ra.assigned_to_email
                FROM requisition_assignments ra
                WHERE ra.requisition_id = %s
                UNION
                SELECT ra.assigned_by_email
                FROM requisition_assignments ra
                WHERE ra.requisition_id = %s
            """, (requisition_id, requisition_id))
            recipients = [row['email'] for row in cursor.fetchall() if row.get("email")]

    except Exception as e:
        logger.error(f"Error updating onboarding for candidate {candidate_id}: {e}", exc_info=True)
        return jsonify(success=False, error=str(e))
    finally:
        conn.close()

    # 🔹 Send Email using Microsoft Graph
    if recipients and candidate_name and access_token:
        email_body = f"""
Hello Team,

The onboarding details for candidate {candidate_name} (Requisition ID: {requisition_id}) have been updated.

Final CTC: {final_ctc or 'N/A'}
Planned Joining Date: {planned_joining_date or 'N/A'}

Updated by: {user['email']}
"""

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        to_recipients = [{"emailAddress": {"address": email}} for email in recipients]

        message = {
            "message": {
                "subject": f"Onboarding Update - {candidate_name}",
                "body": {
                    "contentType": "Text",
                    "content": email_body
                },
                "toRecipients": to_recipients
            },
            "saveToSentItems": "true"
        }

        response = requests.post(
            'https://graph.microsoft.com/v1.0/me/sendMail',
            headers=headers,
            json=message
        )

        if response.status_code == 202:
            logger.info(f"Onboarding email sent successfully to: {', '.join(recipients)}")
        else:
            logger.error(f"Failed to send onboarding email: {response.text}")

    return jsonify(success=True)



@app.route('/update_actual_joining/<int:candidate_id>', methods=['POST'])
def update_actual_joining(candidate_id):
    data = request.get_json()
    actual_joining_date = data.get('actual_joining_date')

    logger.info(f"Updating actual joining date for candidate ID: {candidate_id} to {actual_joining_date}")
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE candidates
                SET actual_joining_date = %s
                WHERE id = %s
            """, (actual_joining_date or None, candidate_id))
        conn.commit()
        return jsonify(success=True)
    except Exception as e:
        logger.error(f"Error updating actual joining date: {e}", exc_info=True)
        return jsonify(success=False, error=str(e))
    finally:
        conn.close()



@app.route('/view_offer/<int:candidate_id>')
def view_offer(candidate_id):
    logger.info(f"View offer letter requested for candidate ID: {candidate_id}")
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT offer_letter FROM candidates WHERE id = %s", (candidate_id,))
            row = cursor.fetchone()
    finally:
        conn.close()

    if row and row['offer_letter']:
        file_data = row['offer_letter']
        file_stream = io.BytesIO(file_data)

        header = file_data[:8]
        if header.startswith(b'%PDF'):
            mime_type = 'application/pdf'
            filename = 'offer_letter.pdf'
        elif header.startswith(b'PK'):
            mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            filename = 'offer_letter.docx'
        elif header.startswith(b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'):
            mime_type = 'application/msword'
            filename = 'offer_letter.doc'
        else:
            logger.error(f"Unsupported file format for candidate ID: {candidate_id}")
            abort(400, description="Unsupported file format")

        logger.info(f"Serving offer letter for candidate ID: {candidate_id} as {filename}")
        return send_file(
            file_stream,
            mimetype=mime_type,
            download_name=filename,
            as_attachment=False
        )

    logger.warning(f"Offer letter not found for candidate ID: {candidate_id}")
    flash("Offer letter not found.")
    return "Offer letter not found", 404


@app.route('/download_resume/<int:candidate_id>')
def download_resume(candidate_id):
    logger.info(f"Downloading resume for candidate ID: {candidate_id}")
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT name, resume FROM candidates WHERE id = %s", (candidate_id,))
            result = cursor.fetchone()

            if result and result['resume']:
                logger.info(f"Resume found for candidate: {result['name']}")
                return send_file(
                    io.BytesIO(result['resume']),
                    download_name=f"{result['name']}_Resume.pdf",
                    as_attachment=True
                )
            else:
                logger.warning(f"No resume found for candidate ID: {candidate_id}")
                return "No resume found for this candidate.", 404
    finally:
        conn.close()


@app.route('/shortlist_candidate/<int:candidate_id>', methods=['POST'])
def shortlist_candidate(candidate_id):
    if 'user' not in session:
        logger.warning("Unauthorized access attempt to shortlist.")
        return redirect(url_for('home'))

    user = session['user']
    email = user['email']
    name = user['name']
    now = datetime.now()
    logger.info(f"User {name} ({email}) attempting to shortlist candidate ID: {candidate_id}")

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    if not result:
        logger.error(f"User {email} not found in database.")
        cursor.close()
        connection.close()
        return jsonify({'success': False, 'error': 'User not found'})

    user_id = result['id']
    logger.info(f"Shortlisting candidate {candidate_id} by user ID {user_id}")

    query = """
        UPDATE candidates
        SET is_shortlisted = TRUE,
            shortlisted_by = %s,
            shortlisted_on = %s
        WHERE id = %s
    """
    cursor.execute(query, (user_id, now, candidate_id))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({
        'success': True,
        'shortlisted_by': name,
        'shortlisted_on': now.strftime('%Y-%m-%d %H:%M')
    })


@app.route('/candidate/<int:id>')
def candidate_detail(id):
    if 'user' not in session:
        logger.warning("Unauthorized attempt to view candidate detail.")
        return redirect(url_for('home'))

    logger.info(f"Candidate detail page requested for ID: {id}")
    user = session['user']
    conn = get_db_connection()

    candidate = None
    ratings_by_level = {}
    next_pending_level = None

    try:
        with conn.cursor() as cursor:
            # Get candidate + requisition info
            cursor.execute("""
                SELECT c.*, r.job_title, r.department
                FROM candidates c
                LEFT JOIN requisitions r ON c.requisition_id = r.id
                WHERE c.id = %s
            """, (id,))
            candidate = cursor.fetchone()

            if not candidate:
                logger.warning(f"Candidate ID {id} not found.")
                flash("Candidate not found", "warning")
                return redirect(url_for('view_candidates'))

            logger.info(f"Candidate found: {candidate['name']}")
            requisition_id = candidate['requisition_id']

            # Get interviewers and their rating (if exists)
            cursor.execute("""
                SELECT ih.id AS interviewer_id, ih.level, ih.interviewer_name, ih.interviewer_email,
                    COALESCE(rt.status, 'pending') AS status, rt.id AS rating_id,
                    rt.communication_skills, rt.technical_skills, rt.learning_ability,
                    rt.problem_solving, rt.cultural_fitment, rt.remarks, rt.status
                    FROM interview_hierarchy ih
                LEFT JOIN ratings rt 
                ON rt.interviewer_id = ih.id AND rt.candidate_id = %s
                WHERE ih.requisition_id = %s
                ORDER BY ih.level ASC
            """, (id, requisition_id))

            interviews = cursor.fetchall()

            for row in interviews:
                level = row['level']
                ratings_by_level[level] = row
                if next_pending_level is None and row['status'] == 'pending':
                    next_pending_level = level

    except Exception as e:
        print("Error:", e)
        logger.exception(f"Error loading candidate detail for ID: {id}")
        flash("Something went wrong.", "danger")
    finally:
        conn.close()

    return render_template('candidate_details.html',
                           candidate=candidate,
                           ratings_by_level=ratings_by_level,
                           next_pending_level=next_pending_level,
                           user=user)

@app.route('/update_offer_status/<int:candidate_id>', methods=['POST'])
def update_offer_status(candidate_id):
    user = session.get('user')
    if not user:
        return jsonify(success=False, message="Unauthorized"), 401

    data = request.json
    new_offer_status = data.get('offer_status')

    if new_offer_status not in ['Accepted', 'Backed Out', None]: # Include None for initially not set
        return jsonify(success=False, message="Invalid offer status provided."), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE candidates
                SET offer_status = %s
                WHERE id = %s
            """, (new_offer_status, candidate_id))
            conn.commit()
            logging.info(f"Candidate {candidate_id} offer status updated to {new_offer_status} by {user['email']}.")
            return jsonify(success=True, message="Offer status updated successfully.")

    except Exception as e:
        conn.rollback()
        logging.exception(f"Error updating offer status for candidate ID {candidate_id}:")
        return jsonify(success=False, message=f"Error updating offer status: {e}"), 500
    finally:
        conn.close()



@app.route('/submit_rating/<int:candidate_id>/<level>', methods=['POST'])
def submit_rating(candidate_id, level):
    user = session.get('user')
    access_token = get_otpluat_token()

    try:
        level_num = int(str(level).replace("Level-", ""))
    except ValueError:
        flash("Invalid level format.", "danger")
        return redirect(url_for('candidate_detail', id=candidate_id))

    logger.info(f"{user['email']} is submitting rating for candidate {candidate_id} at level {level_num}")

    remarks = request.form.get('remarks')
    action = request.form.get('action')  # 'selected', 'rejected', or 'on_hold'

    # Extract ratings
    communication_skills = request.form.get('communication_skills')
    technical_skills = request.form.get('technical_skills')
    learning_ability = request.form.get('learning_ability')
    problem_solving = request.form.get('problem_solving')
    cultural_fitment = request.form.get('cultural_fitment')

    conn = get_db_connection()
    candidate_name = None
    recipients = []

    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # Fetch interviewer and requisition
            cursor.execute("""
                SELECT ih.id AS interviewer_id, ih.requisition_id, c.name AS candidate_name
                FROM interview_hierarchy ih
                JOIN candidates c ON ih.requisition_id = c.requisition_id
                WHERE c.id = %s AND ih.level = %s
            """, (candidate_id, level))
            result = cursor.fetchone()

            if not result:
                flash("Interview hierarchy not found.", "danger")
                return redirect(url_for('candidate_detail', id=candidate_id))

            interviewer_id = result['interviewer_id']
            requisition_id = result['requisition_id']
            candidate_name = result['candidate_name']

            # 🔑 Check if rating already exists
            cursor.execute("""
                SELECT id, status FROM ratings
                WHERE candidate_id = %s AND interviewer_id = %s
            """, (candidate_id, interviewer_id))
            existing_rating = cursor.fetchone()

            if existing_rating:
                if existing_rating['status'] == "on_hold" and action in ("selected", "rejected"):
                    # ✅ Update only status (don’t overwrite ratings)
                    cursor.execute("""
                        UPDATE ratings
                        SET status = %s, remarks = %s
                        WHERE id = %s
                    """, (action, remarks, existing_rating['id']))
                else:
                    # Prevent duplicate insert if already finalised
                    flash("This candidate already has a final decision.", "warning")
                    return redirect(url_for('candidate_detail', id=candidate_id))
            else:
                # ✅ Insert new rating
                cursor.execute("""
                    INSERT INTO ratings (
                        candidate_id, requisition_id, interviewer_id,
                        communication_skills, technical_skills, learning_ability,
                        problem_solving, cultural_fitment,
                        remarks, status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    candidate_id, requisition_id, interviewer_id,
                    communication_skills, technical_skills, learning_ability,
                    problem_solving, cultural_fitment,
                    remarks, action
                ))

            # Always mark interview as completed
            cursor.execute("""
                UPDATE interview_schedule
                SET status = 'completed'
                WHERE candidate_id = %s AND level = %s
            """, (candidate_id, level_num))

            conn.commit()

            # Fetch recipients for email
            cursor.execute("""
                SELECT DISTINCT u.email
                FROM users u
                WHERE u.role = 'hr lead'
                UNION
                SELECT ra.assigned_to_email
                FROM requisition_assignments ra
                WHERE ra.requisition_id = %s
                UNION
                SELECT ra.assigned_by_email
                FROM requisition_assignments ra
                WHERE ra.requisition_id = %s
            """, (requisition_id, requisition_id))
            recipients = [row['email'] for row in cursor.fetchall()]

    except Exception as e:
        logger.exception(f"Submit rating error for candidate {candidate_id}, level {level}")
        flash("Error submitting rating.", "danger")
        return redirect(url_for('candidate_detail', id=candidate_id))
    finally:
        conn.close()

    # ✅ Send email only when final decision is made
    if action in ("selected", "rejected") and recipients and candidate_name and access_token:
        email_body = f"""
Hello Team,

The interview for {candidate_name} at {level} has been completed.

Result: {action.title()}

Remarks: {remarks or 'N/A'}

Submitted by: {user['email']}
"""
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        to_recipients = [{"emailAddress": {"address": email}} for email in recipients]

        message = {
            "message": {
                "subject": f"Interview {level} Completed - {candidate_name}",
                "body": {"contentType": "Text", "content": email_body},
                "toRecipients": to_recipients
            },
            "saveToSentItems": "true"
        }

        response = requests.post(
            'https://graph.microsoft.com/v1.0/users/otpluat@orientindia.net/sendMail',
            headers=headers,
            json=message
        )

        if response.status_code == 202:
            logger.info(f"Email sent successfully to: {', '.join(recipients)}")
        else:
            logger.error(f"Failed to send email: {response.text}")

    flash(f"Rating submitted as '{action.title()}'.", "success")
    return redirect(url_for('candidate_detail', id=candidate_id))







# ------------------------------------------------------------------------------------#
@app.route('/schedule_interview/<int:candidate_id>', methods=['GET', 'POST'])
def schedule_interview(candidate_id):
    if 'user' not in session:
        logger.warning("Unauthorized access to schedule interview.")
        return redirect(url_for('home'))

    logger.info(f"Loading schedule page for candidate ID: {candidate_id}")
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute("""
        SELECT level, interview_datetime, interview_type, status FROM interview_schedule
        WHERE candidate_id = %s
    """, (candidate_id,))
    
    scheduled_interviews = {}
    for row in cursor.fetchall():
        level_val = row['level']
        if isinstance(level_val, str) and level_val.startswith("Level-"):
            level_val = int(level_val.replace("Level-", ""))
        else:
            level_val = int(level_val)
        scheduled_interviews[level_val] = {
            'interview_datetime': row['interview_datetime'],
            'status': row['status'],
            'interview_type': row.get('interview_type', '')
        }

    if request.method == 'POST':
        level_str = request.form['level']
        level = int(level_str.replace("Level-", "")) if level_str.startswith("Level-") else int(level_str)

        interview_datetime_str = request.form['interview_datetime']
        interview_datetime = datetime.strptime(interview_datetime_str, '%Y-%m-%dT%H:%M')
        interview_type = request.form.get('interview_type')
        
        # ✅ FIX: Compare DATE only. This allows all of TODAY'S entries to send emails.
        ist = pytz.timezone('Asia/Kolkata')
        current_time_ist = datetime.now(ist).replace(tzinfo=None)
     
        is_backdated = interview_datetime < current_time_ist

        if level > 1:
            previous = scheduled_interviews.get(level - 1)
            if not previous or previous['status'] != 'completed':
                flash(f"You must complete Level {level - 1} before scheduling Level {level}.", "danger")
                return redirect(request.url)

        cursor.execute("""
            SELECT ih.*, c.email as candidate_email, c.name as candidate_name, c.requisition_id
            FROM interview_hierarchy ih
            JOIN candidates c ON ih.requisition_id = c.requisition_id
            WHERE c.id = %s AND (ih.level = %s OR ih.level = %s)
        """, (candidate_id, level, f"Level-{level}"))
        result = cursor.fetchone()

        if not result:
            flash('Invalid level or candidate', 'danger')
            return redirect(request.url)

        # 1. Save or Update the record first
        cursor.execute("""
            INSERT INTO interview_schedule (
                candidate_id, requisition_id, level, interview_datetime, 
                interviewer_name, interviewer_email, status, interview_type
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                interview_datetime = VALUES(interview_datetime), 
                interview_type = VALUES(interview_type)
        """, (candidate_id, result['requisition_id'], level, interview_datetime_str, 
              result['interviewer_name'], result['interviewer_email'], 'pending', interview_type))
        connection.commit()

        # 2. Only trigger external APIs if NOT backdated (Now allowing all of today)
        if not is_backdated:
            access_token = session.get('access_token')
            if access_token:
                try:
                    event_id = send_teams_invite(
                        interviewer_email=result['interviewer_email'],
                        candidate_email=result['candidate_email'],
                        start_time=interview_datetime,
                        duration_minutes=30,
                        subject=f"Interview for {result['candidate_name']} - Level {level}",
                        location="Microsoft Teams" if interview_type == "Virtual" else "Office",
                        description="Scheduled interview. Please be on time.",
                        access_token=access_token
                    )

                    if event_id:
                        cursor.execute("""
                            UPDATE interview_schedule
                            SET teams_event_id = %s
                            WHERE candidate_id = %s AND level = %s
                        """, (event_id, candidate_id, level))
                        connection.commit()
                        logger.info(f"Teams Event ID {event_id} saved successfully.")
                    else:
                        logger.warning("send_teams_invite returned None. Check Graph API permissions.")

                except Exception as e:
                    logger.exception("Error during Teams invite process")
                    flash("Interview saved, but calendar invite failed.", "warning")

                # Reminder Job
                try:
                    reminder_time = interview_datetime + timedelta(minutes=5)
                    scheduler.add_job(
                        func=send_interview_feedback_reminder,
                        trigger='date',
                        run_date=reminder_time,
                        args=[candidate_id, level, access_token],
                        id=f"reminder_{candidate_id}_{level}",
                        replace_existing=True
                    )
                except Exception as e:
                    logger.error(f"Reminder scheduling failed: {e}")
            else:
                logger.error("No access_token in session. Cannot send invite.")
                flash("Session expired. Please log in again to send invites.", "danger")
        else:
            logger.info(f"Entry for {interview_datetime_str} is backdated. Skipping Teams invite.")

        flash(f"Interview for Level {level} scheduled successfully.", "success")
        return redirect(url_for('schedule_interview', candidate_id=candidate_id))

    return render_template('schedule_interview.html', candidate_id=candidate_id, 
                           hierarchy=get_hierarchy(candidate_id), scheduled=scheduled_interviews, user=session['user'])


def get_hierarchy(candidate_id):
    logging.info(f"Fetching hierarchy for candidate ID: {candidate_id}")
    cursor = get_db_connection().cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT requisition_id FROM candidates WHERE id = %s", (candidate_id,))
    req = cursor.fetchone()

    cursor.execute("SELECT * FROM interview_hierarchy WHERE requisition_id = %s ORDER BY level", (req['requisition_id'],))
    hierarchy = cursor.fetchall()

    # ✅ Normalize hierarchy levels (store both int and display string)
    for row in hierarchy:
        if isinstance(row['level'], str) and row['level'].startswith("Level-"):
            row['level'] = int(row['level'].replace("Level-", ""))
        else:
            row['level'] = int(row['level'])
        row['level_display'] = f"Level-{row['level']}"

    return hierarchy



def send_teams_invite(interviewer_email, candidate_email, start_time, duration_minutes, subject, location, description, access_token):
    logging.info(f"Sending Teams invite to {interviewer_email} and {candidate_email} for {start_time}")
    
    # ✅ FIX: Instead of localizing to UTC, localize to IST (Asia/Kolkata)
    local_tz = pytz.timezone("Asia/Kolkata")
    if start_time.tzinfo is None:
        start_time = local_tz.localize(start_time)
    else:
        start_time = start_time.astimezone(local_tz)

    end_time = start_time + timedelta(minutes=duration_minutes)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    event_payload = {
        "subject": subject,
        "body": {
            "contentType": "HTML",
            "content": description
        },
        "start": {
            # Format: 2023-11-10T14:30:00
            "dateTime": start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "timeZone": "Asia/Kolkata"
        },
        "end": {
            "dateTime": end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "timeZone": "Asia/Kolkata"
        },
        "location": {
            "displayName": location
        },
        "attendees": [
            {
                "emailAddress": {
                    "address": candidate_email,
                    "name": "Candidate"
                },
                "type": "required"
            },
            {
                "emailAddress": {
                    "address": interviewer_email,
                    "name": "Interviewer"
                },
                "type": "required"
            }
        ],
        "isOnlineMeeting": True,
        "onlineMeetingProvider": "teamsForBusiness"
    }

    response = requests.post(
        "https://graph.microsoft.com/v1.0/me/events",
        headers=headers,
        json=event_payload
    )

    if response.status_code >= 400:
        logging.error(f"Failed to send Teams invite: {response.status_code} - {response.text}")
        # Return None so the main route knows the invite failed
        return None 

    event = response.json()
    logging.info(f"Teams invite sent successfully. Event ID: {event.get('id')}")
    return event.get('id')

def delete_teams_event(event_id, access_token):
    url = f"https://graph.microsoft.com/v1.0/users/otpluat@orientindia.net/events/{event_id}"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.delete(url, headers=headers)
    if response.status_code in (204, 200):
        logging.info(f"Deleted previous Teams event {event_id}")
    else:
        logging.warning(f"Failed to delete event {event_id}: {response.status_code} {response.text}")


@app.route('/edit_schedule/<int:candidate_id>/<int:level>', methods=['GET', 'POST'])
def edit_schedule(candidate_id, level):
    logging.info(f"Accessed edit_schedule for candidate {candidate_id}, level {level}")
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        if request.method == 'POST':
            new_time_str = request.form['interview_datetime']
            new_time = datetime.strptime(new_time_str, '%Y-%m-%dT%H:%M')
            interview_type = request.form['interview_type']   

            # ✅ 1. IST Backdated Check
            ist = pytz.timezone('Asia/Kolkata')
            current_time_ist = datetime.now(ist).replace(tzinfo=None)
            is_backdated = new_time < current_time_ist

            cursor.execute("""
                SELECT i.interviewer_email, c.email AS candidate_email, i.teams_event_id
                FROM interview_schedule i
                JOIN candidates c ON i.candidate_id = c.id
                WHERE i.candidate_id = %s AND i.level = %s
            """, (candidate_id, level))
            result = cursor.fetchone()

            access_token = session.get('access_token')
            event_id = result['teams_event_id'] if result else None

            if result:
                # ✅ 2. Only handle Teams integration if NOT backdated
                if not is_backdated:
                    # Delete old event if it exists
                    if result['teams_event_id']:
                        try:
                            delete_teams_event(result['teams_event_id'], access_token)
                        except Exception as e:
                            logging.error(f"Failed to delete old event: {e}")

                    # Create new Teams event
                    event_id = send_teams_invite(
                        interviewer_email=result['interviewer_email'],
                        candidate_email=result['candidate_email'],
                        start_time=new_time,
                        duration_minutes=30,
                        subject=f"Interview - Level {level} (Updated)",
                        location="Microsoft Teams" if interview_type == "Virtual" else "Office",
                        description="This interview schedule has been updated. Please check the new timing.",
                        access_token=access_token
                    )
                else:
                    # If it IS backdated, we don't create a new event. 
                    # We might want to keep the old event_id or null it out.
                    # Usually, for backdated entries, we set the event_id to None.
                    event_id = None
                    logging.info("Edit is backdated. Skipping Teams invite creation.")

                # ✅ 3. Update schedule (Database always gets updated)
                cursor.execute("""
                    UPDATE interview_schedule
                    SET interview_datetime = %s, interview_type = %s, teams_event_id = %s
                    WHERE candidate_id = %s AND level = %s
                """, (new_time, interview_type, event_id, candidate_id, level))
                conn.commit()

            flash("Interview schedule updated successfully.", "success")
            return redirect(url_for('schedule_interview', candidate_id=candidate_id))

        # GET request
        cursor.execute("SELECT * FROM interview_schedule WHERE candidate_id = %s AND level = %s", (candidate_id, level))
        schedule = cursor.fetchone()
        return render_template('edit_schedule.html', schedule=schedule)

    finally:
        cursor.close()
        conn.close()

# ------------------------------------------------------------------------------------#
@app.route('/logout')
def logout():
    user = session.get("user")
    logging.info(f"User {user} logged out")
    session.clear()

    if user and user.get("role") == "Static":
        logging.info("Redirecting static user to login page.")
        # Redirect static user to your local login/home page
        return redirect(url_for('login'))  # or url_for('home') if you want them to land on home
    else:
        # Redirect SSO user to Microsoft's logout
        logging.info("Redirecting SSO user to Microsoft logout.")
        return redirect(
            "https://login.microsoftonline.com/common/oauth2/v2.0/logout"
            f"?post_logout_redirect_uri={url_for('login', _external=True)}"
        )

@app.route('/mark_completed/<int:candidate_id>/<int:level>', methods=['GET'])
def mark_completed(candidate_id, level):
    logging.info(f"Marking interview as completed for candidate {candidate_id}, level {level}")
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE interview_schedule
        SET status = 'completed'
        WHERE candidate_id = %s AND level = %s
    """, (candidate_id, level))
    connection.commit()
    flash(f'Level {level} marked as completed!', 'success')
    logging.info("Interview marked as completed and flash message triggered.")
    return redirect(url_for('schedule_interview', candidate_id=candidate_id))

@app.route('/view_repository')
def view_repository():
    logging.info("Accessed /view_repository route")

    if 'user' not in session:
        logging.warning("Unauthorized access attempt to view_repository")
        return redirect(url_for('home'))

    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            user_role = session['user']['role']
            user_email = session['user']['email']
            logging.info(f"{user_email} ({user_role}) is viewing the job profile repository")

            if user_role == 'hr':
                query = """
                    SELECT *, 
                    (total_exp + TIMESTAMPDIFF(YEAR, date, CURDATE())) AS dynamic_exp
                    FROM job_profile
                    WHERE source = %s
                """
                cursor.execute(query, (user_email,))
            else:
                query = """
                    SELECT *, 
                    (total_exp + TIMESTAMPDIFF(YEAR, date, CURDATE())) AS dynamic_exp
                    FROM job_profile
                """
                cursor.execute(query)

            profiles = cursor.fetchall()
            logging.info(f"Retrieved {len(profiles)} job profiles from repository")
    except Exception as e:
        logging.exception("Error while fetching job profiles:")
        return "Error loading job profiles", 500
    finally:
        conn.close()

    return render_template('view_repository.html', profiles=profiles, user=session['user'])


@app.route('/submit_job_profile', methods=['POST'])
def submit_job_profile():
    if 'user' not in session:
        flash("Please log in to submit a profile.")
        return redirect(url_for('login'))

    data = request.form
    file = request.files['cv']
    user_email = session['user']['email']
    logger.info(f"User '{user_email}' is submitting a job profile.")

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO job_profile (
                    date, name, email_id, contact_number, total_exp,
                    current_loc, skills, current_ctc, exp_ctc, source, cv
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data['date'], data['name'], data['email_id'], data['contact_number'],
                data['total_exp'], data['current_loc'], data['skills'],
                data['current_ctc'], data['exp_ctc'], data['source'],
                file.read() if file else None
            ))
        conn.commit()
        logger.info("Job profile submitted successfully.")
        flash("Profile submitted successfully!")
    except Exception as e:
        logger.exception("Error submitting job profile:")
        conn.rollback()
        flash("An error occurred while submitting the profile.")
    finally:
        conn.close()

    return redirect(url_for('view_repository'))

@app.route('/download_cv/<int:profile_id>')
def download_cv(profile_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch the CV data from the database
            sql = "SELECT cv FROM job_profile WHERE profile_id = %s"
            cursor.execute(sql, (profile_id,))
            profile = cursor.fetchone()
    finally:
        connection.close()

    if profile and profile['cv']:
        # CV is stored as a binary object in the database
        cv_data = profile['cv']
        
        # Check for PDF and DOC file types based on file signature (magic bytes)
        if cv_data.startswith(b'%PDF'):
            mime_type = 'application/pdf'
            filename = 'resume.pdf'
        elif cv_data[:2] == b'\xd0\xcf':  # DOC files start with 0xD0 0xCF (MS Word 97-2003 format)
            mime_type = 'application/msword'
            filename = 'resume.doc'
        elif cv_data[:4] == b'PK\x03\x04':  # DOCX files start with 0x50 0x4B 0x03 0x04 (MS Word 2007+ format)
            mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            filename = 'resume.docx'
        else:
            abort(400, description="Unsupported file type")

        # Send the file without download (open in a new tab)
        return send_file(io.BytesIO(cv_data), mimetype=mime_type, download_name=filename, as_attachment=False)
    
    flash('CV not found.')
    return redirect(url_for('view_repository', profile_id=profile_id))

def send_joining_reminder():
    conn = get_db_connection()
    today_plus_7 = (datetime.today() + timedelta(days=7)).date()

    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT c.name AS candidate_name, c.planned_joining_date, r.job_title,
                       u1.email AS created_by_email, u2.email AS assigned_to_email
                FROM candidates c
                JOIN requisitions r ON c.requisition_id = r.id
                LEFT JOIN users u1 ON r.created_by = u1.email
                LEFT JOIN users u2 ON r.assigned_to = u2.email
                WHERE c.planned_joining_date = %s
            """, (today_plus_7,))
            candidates = cursor.fetchall()

            for c in candidates:
                for recipient in [c['created_by_email'], c['assigned_to_email']]:
                    if recipient:
                        _send_email_to_user(
                            recipient,
                            subject="Upcoming Candidate Joining Reminder",
                            body=f"""
Hi,

This is a reminder that candidate {c['candidate_name']} is expected to join for the position of {c['job_title']} on {c['planned_joining_date']}.

Please ensure all arrangements are in place.

Regards,
HR Team
                            """
                        )

    except Exception as e:
        logger.error(f"Error sending joining reminders: {e}")
    finally:
        conn.close()


def _send_email_to_user(email, subject, body, access_token):
    if not access_token:
        logger.error("Access token not provided.")
        return

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    message = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [
                {"emailAddress": {"address": email}}
            ]
        },
        "saveToSentItems": "true"
    }

    response = requests.post(
        'https://graph.microsoft.com/v1.0/users/otpluat@orientindia.net/sendMail',
        headers=headers,
        json=message
    )

    if response.status_code == 202:
        logger.info(f"Reminder email sent to {email}")
    else:
        logger.error(f"Failed to send reminder email to {email}: {response.text}")



 #------ TAT for interviewer to submit the ratings -------#

def send_interview_feedback_reminder(candidate_id, level, access_token):
    logger.info("Reminder triggered for candidate ID %s, level %s at %s", candidate_id, level, datetime.now())

    india_tz = timezone('Asia/Kolkata')
    now = datetime.now(india_tz)

    conn = get_db_connection()
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT i.id, i.candidate_id, i.interviewer_email, i.interviewer_name,
                   i.interview_datetime, c.name AS candidate_name, r.job_title
            FROM interview_schedule i
            JOIN candidates c ON i.candidate_id = c.id
            JOIN requisitions r ON c.requisition_id = r.id
            WHERE i.candidate_id = %s AND i.level = %s AND i.status = 'completed'
        """, (candidate_id, level))

        interview = cursor.fetchone()
        if interview and interview['interviewer_email']:
            _send_email_to_user(
                email=interview['interviewer_email'],
                subject="Interview Feedback Reminder",
                body=f"""
Hi {interview['interviewer_name']},

This is a gentle reminder to submit your feedback for the interview you conducted with candidate **{interview['candidate_name']}** for the position of **{interview['job_title']}** on **{interview['interview_datetime'].strftime('%Y-%m-%d %H:%M')}**.

Please log in to the system and submit your feedback. Please ignore if already submitted.

Regards,  
HR Team
                """,
                access_token=access_token
            )
            logger.info("Reminder sent to %s", interview['interviewer_email'])
        else:
            logger.info("No reminder sent. Interview not marked as completed or email missing.")
    except Exception as e:
        logger.error("Error sending interview feedback reminder: %s", e)
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='192.168.4.53', port=443, debug=True, ssl_context= (r'C:\PythonApplication\Intranet\certificate.pem',r'C:\PythonApplication\Intranet\privatekey.key'))

