
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
from apscheduler.schedulers.background import BackgroundScheduler
import atexit


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
SCOPE = ["User.Read", "Mail.Send","Calendars.ReadWrite"," OnlineMeetings.ReadWrite"]

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

os.makedirs("logs", exist_ok=True)

# For logging all the steps
logger = logging.getLogger("AppLogger")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = RotatingFileHandler("logs/app.log", maxBytes=1_000_000, backupCount=5)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

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
                    default_role = "admin"
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
@app.route('/home')
def home():
    if 'user' not in session:
        logger.warning("Unauthorized access to /home. Redirecting to login.")
        return redirect(url_for('login'))

    page = request.args.get('page', 'dashboard')
    user_role = session['user']['role']
    logger.info(f"User '{session['user']['email']}' with role '{user_role}' accessed /home with page: {page}")

    allowed_pages = {
        'manager': ['dashboard', 'requisition', 'repository', 'view_requisitions'],
        'hr': ['dashboard', 'repository', 'view_requisitions'],
        'hr lead': ['dashboard', 'repository', 'view_requisitions']
    }

    all_pages = ['dashboard', 'requisition', 'repository', 'usermanagement', 'view_requisitions']
    allowed = all_pages if user_role == 'admin' else allowed_pages.get(user_role, [])

    if page not in allowed:
        logger.warning(f"User '{session['user']['email']}' attempted to access unauthorized page: {page}")
        page = 'notallowed'

    return render_template(
        'home.html',
        user=session['user'],
        page=page
    )

@app.route('/dashboard_data')
def dashboard_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Step 1: Get all unique departments
    cursor.execute("SELECT DISTINCT department FROM requisitions")
    departments_result = cursor.fetchall()
    departments = [row['department'] for row in departments_result]

    openings = []
    filled = []

    # Step 2: For each department, get totals
    for dept in departments:
        cursor.execute("""
            SELECT 
                COALESCE(SUM(number_of_openings), 0) AS total_openings,
                COALESCE(SUM(openings_filled), 0) AS total_filled
            FROM requisitions
            WHERE department = %s
        """, (dept,))
        result = cursor.fetchone()
        openings.append(result['total_openings'])
        filled.append(result['total_filled'])

    # Chart 2: Assigned To-wise
    cursor.execute("""
        SELECT assigned_to,
               COALESCE(SUM(number_of_openings), 0) AS total_openings,
               COALESCE(SUM(openings_filled), 0) AS total_filled
        FROM requisitions
        GROUP BY assigned_to
    """)
    assigned_data = cursor.fetchall()
    assigned_to = [row['assigned_to'] for row in assigned_data]
    assigned_openings = [row['total_openings'] for row in assigned_data]
    assigned_filled = [row['total_filled'] for row in assigned_data]

    conn.close()

    return jsonify({
        'departments': departments,
        'openings': openings,
        'filled': filled,
        'assigned_to': assigned_to,
        'assigned_openings': assigned_openings,
        'assigned_filled': assigned_filled
    })

# ------------------------------------------------------------------------------------#
@app.route('/submit_requisition', methods=['POST'])
def submit_requisition():
    data = request.form
    user_email = session['user']['email']
    logger.info(f"User '{user_email}' is submitting a requisition.")

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Insert requisition
            cursor.execute("""
                INSERT INTO requisitions (
                    job_title, department, number_of_openings,
                    skills_required, location, hiring_type,
                    budget, job_description, created_by
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data['job_title'], data['department'], data['number_of_openings'],
                data['skills_required'], data['location'], data['hiring_type'],
                data['budget'], data['job_description'], user_email
            ))
            requisition_id = conn.insert_id()
            logger.info(f"Inserted requisition ID: {requisition_id}")

            # Insert interview hierarchy
            levels = int(data['levels'])
            for i in range(1, levels + 1):
                cursor.execute("""
                    INSERT INTO interview_hierarchy (
                        requisition_id, level, interviewer_name, interviewer_email
                    ) VALUES (%s, %s, %s, %s)
                """, (
                    requisition_id, i, data[f'interviewer_name_{i}'], data[f'interviewer_email_{i}']
                ))
                logger.info(f"Inserted level {i} interviewer: {data[f'interviewer_email_{i}']}")

        conn.commit()
        logger.info(f"Requisition {requisition_id} committed to the database.")

        # Email
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

# ------------------------------------------------------------------------------------#
def send_requisition_email(requisition_data):
    access_token = session.get("access_token")
    user = session.get("user")

    if not access_token or not user:
        logger.error("Attempted to send email without authentication.")
        return False, "User not authenticated."

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    email_body = f"""
Hi HR Team,

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

    message = {
        "message": {
            "subject": "New Hiring Requisition Submitted",
            "body": {
                "contentType": "Text",
                "content": email_body
            },
            "toRecipients": [
                {"emailAddress": {"address": "virajhumbre@orientindia.net"}}
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
        logger.info(f"Email sent successfully to HR for requisition by {user['email']}")
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
                END
            """)
            conn.commit()
            logging.info("Requisition statuses updated based on openings_filled")

            # Fetch requisitions
            if user['role'] in ['admin', 'hr lead']:
                logging.info(f"{user['email']} fetching all requisitions (Role: {user['role']})")
                cursor.execute("""
                    SELECT r.*, u1.name AS created_by_name, u2.name AS assigned_to_name
                    FROM requisitions r
                    LEFT JOIN users u1 ON r.created_by = u1.email
                    LEFT JOIN users u2 ON r.assigned_to = u2.email
                    ORDER BY r.created_at DESC
                """)
            else:
                logging.info(f"{user['email']} fetching assigned requisitions")
                cursor.execute("""
                    SELECT r.id, r.job_title, r.department, r.created_at, r.created_by,
                           r.assigned_to, r.status, u1.name AS created_by_name, u2.name AS assigned_to_name
                    FROM requisitions r
                    LEFT JOIN users u1 ON r.created_by = u1.email
                    LEFT JOIN users u2 ON r.assigned_to = u2.email
                    WHERE r.assigned_to = %s
                    ORDER BY r.created_at DESC
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

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT r.*, u1.name AS created_by_name, u2.name AS assigned_to_name
                FROM requisitions r
                LEFT JOIN users u1 ON r.created_by = u1.email
                LEFT JOIN users u2 ON r.assigned_to = u2.email
                WHERE r.id = %s
            """, (requisition_id,))
            requisition = cursor.fetchone()

            if not requisition:
                logging.warning(f"Requisition {requisition_id} not found.")
                flash("Requisition not found", "warning")
                return redirect(url_for('view_requisitions'))

            if user['role'] in ['admin', 'hr lead']:
                logging.info(f"{user['email']} fetching HR users for assignment")
                cursor.execute("SELECT name, email FROM users WHERE role = 'hr'")
                hr_users = cursor.fetchall()

            if request.method == 'POST' and user['role'] in ['admin', 'hr lead']:
                assigned_to = request.form['assigned_to']
                cursor.execute("""
                    UPDATE requisitions
                    SET assigned_to = %s
                    WHERE id = %s
                """, (assigned_to, requisition_id))
                conn.commit()
                logging.info(f"Requisition {requisition_id} assigned to {assigned_to} by {user['email']}")
                flash("Requisition successfully assigned!", "success")
                return redirect(url_for('view_requisition_details', requisition_id=requisition_id))

    except Exception as e:
        logging.error(f"Error fetching requisition details: {e}")
        flash("Error loading requisition details", "danger")
    finally:
        conn.close()

    return render_template('requisition_details.html', requisition=requisition, hr_users=hr_users, user=user)

@app.route('/requisition/<int:requisition_id>/edit', methods=['GET', 'POST'])
def edit_requisition(requisition_id):
    user = session.get('user')
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            if request.method == 'POST':
                form = request.form
                cursor.execute("""
                    UPDATE requisitions SET
                        job_title = %s, department = %s, number_of_openings = %s,
                        skills_required = %s, location = %s, hiring_type = %s,
                        budget = %s, job_description = %s
                    WHERE id = %s
                """, (
                    form['job_title'], form['department'], form['number_of_openings'],
                    form['skills_required'], form['location'], form['hiring_type'],
                    form['budget'], form['job_description'], requisition_id
                ))
                conn.commit()
                flash("Requisition updated successfully!", "success")
                return redirect(url_for('view_requisition', requisition_id=requisition_id))

            # GET request – fetch requisition
            cursor.execute("SELECT * FROM requisitions WHERE id = %s", (requisition_id,))
            requisition = cursor.fetchone()
    except Exception as e:
        logger.error(f"Error in edit_requisition: {e}")
        flash("Something went wrong while editing the requisition.", "danger")
        return redirect(url_for('home'))
    finally:
        conn.close()

    return render_template("edit_requisition.html", requisition=requisition, user=user)

@app.route('/update_comments/<int:requisition_id>', methods=['POST'])
def update_comments(requisition_id):
    comments = request.form.get('comments')
    user = session.get("user")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Update comments
        cursor.execute("UPDATE requisitions SET comments = %s WHERE id = %s", (comments, requisition_id))
        conn.commit()

        logger.info(f"Comments updated for requisition ID {requisition_id} by user {user['email'] if user else 'Unknown'}. Comment: {comments}")

        # Fetch updated requisition data
        cursor.execute("SELECT * FROM requisitions WHERE id = %s", (requisition_id,))
        requisition = cursor.fetchone()

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

def get_requisitions(email, user):
    logging.info(f"Fetching requisitions for {email} (Role: {user})")
    connection = get_db_connection()
    with connection.cursor() as cursor:
        if user in ['admin', 'hr lead']:
            cursor.execute("SELECT * FROM requisitions")
        else:
            cursor.execute("SELECT * FROM requisitions WHERE assigned_to = %s", (email,))
        requisitions = cursor.fetchall()
        logging.info(f"Found {len(requisitions)} requisitions")
    connection.close()
    return requisitions


@app.route('/submit_candidate', methods=['GET', 'POST'])
def submit_candidate():
    logging.info("Accessed /submit_candidate route")
    logging.debug(f"Session contents: {session}")
    print("Session contents:", session)
    if 'user' not in session:
        logging.warning("Unauthorized access attempt to submit_candidate")
        return redirect(url_for('home'))


    user_id = session['user']['email']
    user = session['user']['role']
    requisitions = get_requisitions(user_id, user)


    if request.method == 'POST':
        logging.info(f"Candidate submission attempt by user: {user_id}")

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        skills = request.form['skills']
        requisition_id = request.form['requisition_id']
        resume_file = request.files['resume']
        total_exp = request.form['total_exp']
        current_loc = request.form['current_loc']
        current_ctc = request.form['current_ctc']
        exp_ctc = request.form['exp_ctc']
        source = request.form['source']
        
        allowed_ids = [str(r['id']) for r in requisitions]
        if requisition_id not in allowed_ids:
            logging.error(f"Unauthorized requisition access attempt by {user_id} for requisition_id {requisition_id}")
            return "Unauthorized access to requisition", 403

        resume_blob = resume_file.read()

        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO candidates (name, email, phone, skills, requisition_id, resume, submitted_by, total_exp,
                           current_loc, current_ctc, exp_ctc, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, email, phone, skills, requisition_id, resume_blob, user_id, total_exp, current_loc, current_ctc,
                  exp_ctc, source))
            connection.commit()
        connection.close()
        logging.info(f"Candidate {name} submitted successfully by {user_id}")
        return 'success'  # This will trigger the modal on success

    return render_template('submit_candidate.html', requisitions=requisitions, user = session['user'])

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

            if user_role == 'hr':
                query = """
                    SELECT c.*, r.job_title AS requisition_title,
                    c.offer_letter IS NOT NULL AS offer_exists
                    FROM candidates c
                    JOIN requisitions r ON c.requisition_id = r.id
                    WHERE c.submitted_by = %s
                """
                cursor.execute(query, (user_email,))
            else:
                query = """
                    SELECT c.*, r.job_title AS requisition_title,
                    c.offer_letter IS NOT NULL AS offer_exists
                    FROM candidates c
                    JOIN requisitions r ON c.requisition_id = r.id
                """
                cursor.execute(query)

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
        with conn.cursor() as cursor:
            # Get current selection_status and requisition_id of candidate
            cursor.execute("SELECT selection_status, requisition_id FROM candidates WHERE id = %s", (candidate_id,))
            result = cursor.fetchone()

            if not result:
                logging.warning(f"No candidate found with ID {candidate_id}")
                return jsonify({'success': False, 'message': 'Candidate not found'})

            current_status = result['selection_status']
            requisition_id = result['requisition_id']

            # Update selection_status only if it's changing
            if current_status != new_status:
                cursor.execute(
                    "UPDATE candidates SET selection_status = %s WHERE id = %s",
                    (new_status, candidate_id)
                )

                # Only increment openings_filled if changing from non-Selected to Selected
                if new_status == 'selected' and current_status != 'selected':
                    cursor.execute("""
                        UPDATE requisitions
                        SET openings_filled = openings_filled + 1
                        WHERE id = %s AND openings_filled < number_of_openings
                    """, (requisition_id,))

            conn.commit()
            logging.info(f"Updated candidate {candidate_id} status from '{current_status}' to '{new_status}'")
            return jsonify({'success': True})

    except Exception as e:
        conn.rollback()
        logging.exception(f"Failed to update selection status for candidate {candidate_id}")
        return jsonify({'success': False, 'message': 'Database error'})
    finally:
        conn.close()



@app.route('/update_onboarding/<int:candidate_id>', methods=['POST'])
def update_onboarding(candidate_id):
    final_ctc             = request.form.get('final_ctc')
    planned_joining_date  = request.form.get('planned_joining_date')
    actual_joining_date   = request.form.get('actual_joining_date')
    offer_file            = request.files.get('offer_letter')

    logger.info(f"Updating onboarding info for candidate ID: {candidate_id}")

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if offer_file and offer_file.filename:
                offer_blob = offer_file.read()
                if offer_blob:
                    logger.info(f"Offer letter uploaded for candidate ID: {candidate_id}")
                    cursor.execute("""
                        UPDATE candidates
                        SET final_ctc = %s,
                            planned_joining_date = %s,
                            actual_joining_date = %s,
                            offer_letter = %s
                        WHERE id = %s
                    """, (
                        final_ctc or None,
                        planned_joining_date or None,
                        actual_joining_date or None,
                        offer_blob,
                        candidate_id
                    ))
                else:
                    logger.warning(f"Empty file submitted for offer letter - candidate ID: {candidate_id}")
                    cursor.execute("""
                        UPDATE candidates
                        SET final_ctc = %s,
                            planned_joining_date = %s,
                            actual_joining_date = %s
                        WHERE id = %s
                    """, (
                        final_ctc or None,
                        planned_joining_date or None,
                        actual_joining_date or None,
                        candidate_id
                    ))
            else:
                logger.info(f"No offer letter uploaded for candidate ID: {candidate_id}")
                cursor.execute("""
                    UPDATE candidates
                    SET final_ctc = %s,
                        planned_joining_date = %s,
                        actual_joining_date = %s
                    WHERE id = %s
                """, (
                    final_ctc or None,
                    planned_joining_date or None,
                    actual_joining_date or None,
                    candidate_id
                ))

        conn.commit()
        logger.info(f"Successfully updated candidate ID: {candidate_id}")
        return jsonify(success=True)

    except Exception as e:
        logger.error(f"Error updating onboarding for candidate ID {candidate_id}: {e}", exc_info=True)
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



@app.route('/submit_rating/<int:candidate_id>/<int:level>', methods=['POST'])
def submit_rating(candidate_id, level):
    user = session.get('user')
    logger.info(f"{user['email']} is submitting rating for candidate {candidate_id} at level {level}")
    remarks = request.form.get('remarks')
    
    # Extract rating values from the form
    communication_skills = request.form.get('communication_skills')
    technical_skills = request.form.get('technical_skills')
    learning_ability = request.form.get('learning_ability')
    problem_solving = request.form.get('problem_solving')
    cultural_fitment = request.form.get('cultural_fitment')

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Find interviewer and requisition ID
            cursor.execute("""
                SELECT ih.id AS interviewer_id, ih.requisition_id
                FROM interview_hierarchy ih
                JOIN candidates c ON ih.requisition_id = c.requisition_id
                WHERE c.id = %s AND ih.level = %s
            """, (candidate_id, level))
            result = cursor.fetchone()

            if result:
                interviewer_id = result['interviewer_id']
                requisition_id = result['requisition_id']

                # Insert into ratings table
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
                    remarks, 'submitted'
                ))
                conn.commit()
                logger.info(f"Rating submitted successfully for candidate {candidate_id}, level {level}")

        flash("Rating submitted successfully.", "success")
    except Exception as e:
        logger.exception(f"Submit rating error for candidate {candidate_id}, level {level}")
        print("Submit rating error:", e)
        flash("Error submitting rating.", "danger")
    finally:
        conn.close()

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
        SELECT level, interview_datetime, status FROM interview_schedule
        WHERE candidate_id = %s
    """, (candidate_id,))
    scheduled_interviews = {
        row['level']: {
            'interview_datetime': row['interview_datetime'],
            'status': row['status']
        } for row in cursor.fetchall()
    }

    if request.method == 'POST':
        level = int(request.form['level'])
        interview_datetime_str = request.form['interview_datetime']
        interview_datetime = datetime.strptime(interview_datetime_str, '%Y-%m-%dT%H:%M')

        logger.info(f"Scheduling interview: candidate {candidate_id}, level {level}, datetime {interview_datetime_str}")

        if level > 1:
            previous = scheduled_interviews.get(level - 1)
            if not previous or previous['status'] != 'completed':
                logger.warning(f"Cannot schedule Level {level} without completing Level {level - 1}")
                flash(f"You must complete Level {level - 1} before scheduling Level {level}.", "danger")
                return redirect(request.url)

        cursor.execute("""
            SELECT ih.*, c.email as candidate_email, c.name as candidate_name
            FROM interview_hierarchy ih
            JOIN candidates c ON ih.requisition_id = c.requisition_id
            WHERE c.id = %s AND ih.level = %s
        """, (candidate_id, level))
        result = cursor.fetchone()

        if not result:
            logger.error(f"No interviewer found for candidate {candidate_id}, level {level}")
            flash('Invalid level or candidate', 'danger')
            return redirect(request.url)

        cursor.execute("""
            INSERT INTO interview_schedule (candidate_id, level, interview_datetime, interviewer_name, interviewer_email, status)
            VALUES (%s, %s, %s, %s, %s, 'pending')
            ON DUPLICATE KEY UPDATE interview_datetime = VALUES(interview_datetime)
        """, (candidate_id, level, interview_datetime_str, result['interviewer_name'], result['interviewer_email']))
        connection.commit()

        access_token = session.get('access_token')
        try:
            send_teams_invite(
                interviewer_email=result['interviewer_email'],
                candidate_email=result['candidate_email'],
                start_time=interview_datetime,
                duration_minutes=30,
                subject=f"Interview for Candidate {result['candidate_name']} - Level {level}",
                location="Microsoft Teams Meeting",
                description="This is a scheduled interview. Please be on time.",
                access_token=access_token
            )
            logger.info(f"Teams invite sent to {result['interviewer_email']} and {result['candidate_email']}")
        except Exception as e:
            logger.exception("Error sending Teams invite")
            flash("Interview scheduled, but failed to send Teams invite.", "warning")

        # ✅ Schedule one-time reminder exactly 5 mins after interview start
        reminder_time = interview_datetime + timedelta(minutes=5)
        job_id = f"reminder_{candidate_id}_{level}"

        try:
            scheduler.add_job(
                func=send_interview_feedback_reminder,
                trigger='date',
                run_date=reminder_time,
                args=[candidate_id, level, access_token],
                id=job_id,
                replace_existing=True
            )
            logger.info(f"Scheduled reminder job {job_id} at {reminder_time}")
        except Exception as e:
            logger.error(f"Failed to schedule reminder job {job_id}: {e}")

        flash(f"Interview for Level {level} scheduled successfully.", "success")
        return redirect(url_for('schedule_interview', candidate_id=candidate_id))

    return render_template(
        'schedule_interview.html',
        candidate_id=candidate_id,
        hierarchy=get_hierarchy(candidate_id),
        scheduled=scheduled_interviews,
        user=session['user']
    )

def get_hierarchy(candidate_id):
    logging.info(f"Fetching hierarchy for candidate ID: {candidate_id}")
    cursor = get_db_connection().cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT requisition_id FROM candidates WHERE id = %s", (candidate_id,))
    req = cursor.fetchone()
    cursor.execute("SELECT * FROM interview_hierarchy WHERE requisition_id = %s ORDER BY level", (req['requisition_id'],))
    return cursor.fetchall()

def send_teams_invite(interviewer_email, candidate_email, start_time, duration_minutes, subject, location, description, access_token):
    logging.info(f"Sending Teams invite to {interviewer_email} and {candidate_email} for {start_time}")
    # Ensure timezone-aware datetime (UTC)
    if start_time.tzinfo is None:
        start_time = pytz.utc.localize(start_time)

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
        f"https://graph.microsoft.com/v1.0/users/otpluat@orientindia.net/events",
        headers=headers,
        json=event_payload
    )

    if response.status_code >= 400:
        logging.error(f"Failed to send Teams invite: {response.status_code} - {response.text}")
        raise Exception(f"Failed to send Teams invite: {response.status_code} {response.text}")

    logging.info("Teams invite sent successfully.")
    return response.json()

@app.route('/edit_schedule/<int:candidate_id>/<int:level>', methods=['GET', 'POST'])
def edit_schedule(candidate_id, level):
    logging.info(f"Accessed edit_schedule for candidate {candidate_id}, level {level}")
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        new_time_str = request.form['interview_datetime']
        new_time = datetime.strptime(new_time_str, '%Y-%m-%dT%H:%M')  # Adjust format if needed
        logging.info(f"Updating interview time to {new_time} for candidate {candidate_id}, level {level}")

        cursor.execute("""
            UPDATE interview_schedule
            SET interview_datetime = %s
            WHERE candidate_id = %s AND level = %s
        """, (new_time, candidate_id, level))
        conn.commit()

        # Fetch required details
        cursor.execute("""
            SELECT i.interviewer_email, c.email AS candidate_email
            FROM interview_schedule i
            JOIN candidates c ON i.candidate_id = c.id
            WHERE i.candidate_id = %s AND i.level = %s
        """, (candidate_id, level))
        result = cursor.fetchone()

        access_token = session.get('access_token')
        if result:
            interviewer_email = result['interviewer_email']
            candidate_email = result['candidate_email']
            duration_minutes = 30
            subject = f"Interview - Level {level}"
            location = "Microsoft Teams"
            description = "This is an automated interview invitation. Please be prepared on time."
            access_token = access_token  # Replace with your function to get a valid token

            logging.info(f"Sending updated invite to {interviewer_email} and {candidate_email}")

            send_teams_invite(
                interviewer_email,
                candidate_email,
                new_time,
                duration_minutes,
                subject,
                location,
                description,
                access_token
            )

        return redirect(url_for('schedule_interview', candidate_id=candidate_id))

    # GET method
    cursor.execute("SELECT * FROM interview_schedule WHERE candidate_id = %s AND level = %s", (candidate_id, level))
    schedule = cursor.fetchone()
    return render_template('edit_schedule.html', schedule=schedule)


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
    app.run(debug=True, port=5005)


