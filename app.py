from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import msal
from datetime import timedelta
from dotenv import load_dotenv
import os

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
SCOPE = ["User.Read"]

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

        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
        conn.close()

        if user:
            # Check if the user is an SSO user (no password stored)
            if not user.get("password_hash"):
                flash("This account uses SSO. Please login using Azure.")
                return redirect(url_for('login'))

            # Validate password
            if password == user.get("password_hash"):
                session["user"] = {"email": user["email"], "name": user["name"], "role": user.get("role", "static")}
                return redirect(url_for('home'))
            else:
                flash("Incorrect password.")
        else:
            flash("User not found.")

    return render_template('login.html')

@app.route('/sso-login')
def sso_login():
    return redirect(build_auth_url())

@app.route(REDIRECT_PATH)
def auth_response():
    code = request.args.get('code')
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
                    # Existing user
                    user_data = {
                        "email": user_row["email"],
                        "name": user_row["name"],
                        "role": user_row["role"]
                    }
                else:
                    # New user — assign default role "HR"
                    default_role = "hr"
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
            return redirect(url_for('home'))

    return "SSO Login failed", 401

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))

    page = request.args.get('page', 'dashboard')
    user_role = session['user']['role']

    allowed_pages = {
        'manager': ['dashboard', 'requisition', 'repository', 'view_requisitions'],
        'hr': ['dashboard', 'repository', 'view_requisitions'],
    }

    all_pages = ['dashboard', 'requisition', 'repository', 'usermanagement', 'view_requisitions']
    allowed = all_pages if user_role == 'admin' else allowed_pages.get(user_role, [])

    if page not in allowed:
        page = 'notallowed'

    # Requisition data only when viewing that page
    requisitions = []
    if page == 'view_requisitions':
        connection = get_db_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM requisitions ORDER BY created_at DESC")
                requisitions = cursor.fetchall()
            connection.close()

    return render_template(
        'home.html',
        user=session['user'],
        page=page,
        requisitions=requisitions
    )

@app.route('/submit_requisition', methods=['POST'])
def submit_requisition():
    data = request.form
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Insert into requisitions
            cursor.execute("""
                INSERT INTO requisitions (
                    job_title, department, number_of_openings,
                    skills_required, location, hiring_type,
                    budget,job_description, created_by
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data['job_title'], data['department'], data['number_of_openings'],
                data['skills_required'], data['location'], data['hiring_type'],
                data['budget'],data['job_description'], session['user']['email']
            ))
            requisition_id = conn.insert_id()

            # Insert Interview Hierarchy
            levels = int(data['levels'])
            for i in range(1, levels + 1):
                cursor.execute("""
                    INSERT INTO interview_hierarchy (
                        requisition_id, level, interviewer_name, interviewer_email
                    ) VALUES (%s, %s, %s, %s)
                """, (
                    requisition_id, i, data[f'interviewer_name_{i}'], data[f'interviewer_email_{i}']
                ))
        conn.commit()
        flash('Requisition submitted successfully!')
    except Exception as e:
        print(e)
        conn.rollback()
        flash('An error occurred while submitting the requisition.')
    finally:
        conn.close()
    return redirect(url_for('home', page='requisition'))





@app.route('/logout')
def logout():
    user = session.get("user")
    session.clear()

    if user and user.get("role") == "Static":
        # Redirect static user to your local login/home page
        return redirect(url_for('login'))  # or url_for('home') if you want them to land on home
    else:
        # Redirect SSO user to Microsoft's logout
        return redirect(
            "https://login.microsoftonline.com/common/oauth2/v2.0/logout"
            f"?post_logout_redirect_uri={url_for('login', _external=True)}"
        )

if __name__ == '__main__':
    app.run(debug=True, port=5005)
