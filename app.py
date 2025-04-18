
from flask import send_file,Flask, flash,render_template, request, redirect, url_for, session, flash,jsonify
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
            return redirect(url_for('home'))

    return "SSO Login failed", 401
# ------------------------------------------------------------------------------------#
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))

    page = request.args.get('page', 'dashboard')
    user_role = session['user']['role']

    allowed_pages = {
        'manager': ['dashboard', 'requisition', 'repository', 'view_requisitions'],
        'hr': ['dashboard', 'repository', 'view_requisitions'],
        'hr lead': ['dashboard', 'repository', 'view_requisitions','assign_requisition' ]
    }

    all_pages = ['dashboard', 'requisition', 'repository', 'usermanagement', 'view_requisitions','assign_requisition']
    allowed = all_pages if user_role == 'admin' else allowed_pages.get(user_role, [])

    if page not in allowed:
        page = 'notallowed'

    return render_template(
        'home.html',
        user=session['user'],
        page=page
    )
# ------------------------------------------------------------------------------------#
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
        # ✅ Email Notification to HR
        success, message = send_requisition_email(data)
        if success:
            flash('Requisition submitted and email sent successfully!')
        else:
            flash(f'Requisition submitted, but email failed: {message}')

    except Exception as e:
        print(e)
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
        return True, "Mail sent"
    else:
        return False, f"Failed to send mail: {response.text}"
# ------------------------------------------------------------------------------------#
@app.route('/assign_requisition', methods=['GET', 'POST'])
def assign_requisition():

    if 'user' not in session or session['user']['role'] not in ['hr lead', 'admin']:
        return redirect(url_for('home'))

    user = session.get('user')
    conn = get_db_connection()
    requisitions = []
    hr_users = []
    success_message = None

    try:
        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT r.id, r.job_title, r.department, u.name AS created_by
                FROM requisitions r
                JOIN users u ON r.created_by = u.email
                WHERE r.assigned_to IS NULL
                ORDER BY r.created_at DESC
            """)
            requisitions = cursor.fetchall()


            cursor.execute("SELECT id, name, email FROM users WHERE role = 'hr'")
            hr_users = cursor.fetchall()


            # Handle form submission (POST)
            if request.method == 'POST':
                requisition_id = request.form['requisition_id']
                assigned_to = request.form['assigned_to']

                # Update the requisition assignment
                cursor.execute("""
                    UPDATE requisitions
                    SET assigned_to = %s
                    WHERE id = %s
                """, (assigned_to, requisition_id))
                conn.commit()

                flash("Requisition successfully assigned!", "success")
                # Redirect to the same page to refresh and update the dropdown
                return redirect(url_for('assign_requisition'))

    except Exception as e:
        print("Error:", str(e))

    finally:
        conn.close()

    return render_template('assign_requisition.html', requisitions=requisitions, hr_users=hr_users,  user=user)
# ------------------------------------------------------------------------------------#

@app.route('/view_requisitions')
def view_requisitions():
    if 'user' not in session:
        return redirect(url_for('home'))

    user = session['user']
    conn = get_db_connection()
    requisitions = []

    try:
        with conn.cursor() as cursor:
            if user['role'] in ['admin', 'hr lead']:
                # Admins and HR Leads see all requisitions
                cursor.execute("""
                    SELECT r.id, r.job_title, r.department, r.created_at, r.created_by,
                           r.assigned_to, u1.name AS created_by_name, u2.name AS assigned_to_name
                    FROM requisitions r
                    LEFT JOIN users u1 ON r.created_by = u1.email
                    LEFT JOIN users u2 ON r.assigned_to = u2.email
                    ORDER BY r.created_at DESC
                """)
            else:
                # HR sees only their own assigned requisitions
                cursor.execute("""
                    SELECT r.id, r.job_title, r.department, r.created_at,r.created_by,
                           r.assigned_to, u1.name AS created_by_name, u2.name AS assigned_to_name
                    FROM requisitions r
                    LEFT JOIN users u1 ON r.created_by = u1.email
                    LEFT JOIN users u2 ON r.assigned_to = u2.email
                    WHERE r.assigned_to = %s
                    ORDER BY r.created_at DESC
                """, (user['email'],))

            requisitions = cursor.fetchall()

    except Exception as e:
        print("Error in view_requisitions:", e)
        flash("Something went wrong fetching requisitions", "danger")
    finally:
        conn.close()

    return render_template('view_requisitions.html', requisitions=requisitions, user=user )

# ------------------------------------------------------------------------------------#
@app.route('/user_management')
def user_management():
    print("Session contents:", session)
    user = session.get('user')
    print(user)
    email = session['user']['email']
    print ("Email", email)
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            db_users = cursor.fetchall()
    finally:
        connection.close()
    return render_template('user_management.html', users=db_users,user=user)

# Route: Update role
@app.route('/update-role/<int:user_id>', methods=['POST'])
def update_role(user_id):
    new_role = request.form.get('role')

    if not new_role:
        flash("Invalid role selected.", "danger")
        return redirect(url_for('user_management'))

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE users SET role = %s WHERE id = %s"
            cursor.execute(sql, (new_role, user_id))
        connection.commit()
        flash("Role updated successfully.", "success")
    finally:
        connection.close()

    return redirect(url_for('user_management'))

# ------------------------------------------------------------------------------------#

def get_requisitions(email, user):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        if user in ['admin', 'hr lead']:
            cursor.execute("SELECT * FROM requisitions")
        else:
            cursor.execute("SELECT * FROM requisitions WHERE assigned_to = %s", (email,))
        requisitions = cursor.fetchall()
    connection.close()
    return requisitions


@app.route('/submit_candidate', methods=['GET', 'POST'])
def submit_candidate():
    print("Session contents:", session)
    if 'user' not in session:
        return redirect(url_for('home'))


    user_id = session['user']['email']
    user = session['user']['role']
    requisitions = get_requisitions(user_id, user)

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        skills = request.form['skills']
        requisition_id = request.form['requisition_id']
        resume_file = request.files['resume']

        allowed_ids = [str(r['id']) for r in requisitions]
        if requisition_id not in allowed_ids:
            return "Unauthorized access to requisition", 403

        resume_blob = resume_file.read()

        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO candidates (name, email, phone, skills, requisition_id, resume, submitted_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, email, phone, skills, requisition_id, resume_blob, user_id))
            connection.commit()
        connection.close()

        return "Candidate submitted successfully!"

    return render_template('submit_candidate.html', requisitions=requisitions, user = session['user'])

# ------------------------------------------------------------------------------------#
@app.route('/view_candidates')
def view_candidates():
    if 'user' not in session:
        return redirect(url_for('home'))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if session['user']['role'] == 'hr':
                query = """
                    SELECT c.*, r.job_title AS requisition_title
                    FROM candidates c
                    JOIN requisitions r ON c.requisition_id = r.id
                    WHERE c.submitted_by = %s
                """
                cursor.execute(query, (session['user']['email'],))
            else:
                query = """
                    SELECT c.*, r.job_title AS requisition_title
                    FROM candidates c
                    JOIN requisitions r ON c.requisition_id = r.id
                """
                cursor.execute(query)

            candidates = cursor.fetchall()
    finally:
        conn.close()

    return render_template('view_candidates.html', candidates=candidates, user = session['user'])


@app.route('/download_resume/<int:candidate_id>')
def download_resume(candidate_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT name, resume FROM candidates WHERE id = %s", (candidate_id,))
            result = cursor.fetchone()

            if result and result['resume']:
                return send_file(
                    io.BytesIO(result['resume']),
                    download_name=f"{result['name']}_Resume.pdf",
                    as_attachment=True
                )
            else:
                return "No resume found for this candidate.", 404
    finally:
        conn.close()

@app.route('/shortlist_candidate/<int:candidate_id>', methods=['POST'])
def shortlist_candidate(candidate_id):
    if 'user' not in session:
        return redirect(url_for('home'))

    user = session['user']
    email = user['email']
    name = user['name']
    now = datetime.now()

    connection = get_db_connection()
    cursor = connection.cursor()

    # Step 1: Get the user ID based on the email from the session
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    if not result:
        cursor.close()
        connection.close()
        return jsonify({'success': False, 'error': 'User not found'})

    user_id = result['id']

    # Step 2: Update candidate as shortlisted
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

# ------------------------------------------------------------------------------------#
@app.route('/schedule_interview/<int:candidate_id>', methods=['GET', 'POST'])
def schedule_interview(candidate_id):
    if 'user' not in session:
        return redirect(url_for('home'))

    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Fetch scheduled interviews with status
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

        # 🧠 Check if previous level is completed (except for level 1)
        if level > 1:
            previous = scheduled_interviews.get(level - 1)
            if not previous or previous['status'] != 'completed':
                flash(f"You must complete Level {level - 1} before scheduling Level {level}.", "danger")
                return redirect(request.url)

        # Fetch interviewer info from hierarchy
        cursor.execute("""
            SELECT ih.*, c.email as candidate_email, c.name as candidate_name
            FROM interview_hierarchy ih
            JOIN candidates c ON ih.requisition_id = c.requisition_id
            WHERE c.id = %s AND ih.level = %s
        """, (candidate_id, level))
        result = cursor.fetchone()

        if not result:
            flash('Invalid level or candidate', 'danger')
            return redirect(request.url)

        # Insert or update interview_schedule
        cursor.execute("""
            INSERT INTO interview_schedule (candidate_id, level, interview_datetime, interviewer_name, interviewer_email, status)
            VALUES (%s, %s, %s, %s, %s, 'pending')
            ON DUPLICATE KEY UPDATE interview_datetime = VALUES(interview_datetime)
        """, (candidate_id, level, interview_datetime_str, result['interviewer_name'], result['interviewer_email']))
        connection.commit()

        # Teams Invite
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
        except Exception as e:
            print("Error sending invite:", e)
            flash("Interview scheduled, but failed to send Teams invite.", "warning")

        flash(f"Interview for Level {level} scheduled successfully.", "success")
        return redirect(url_for('schedule_interview', candidate_id=candidate_id))

    # GET request
    return render_template(
        'schedule_interview.html',
        candidate_id=candidate_id,
        hierarchy=get_hierarchy(candidate_id),
        scheduled=scheduled_interviews,
        user=session['user']
    )




def get_hierarchy(candidate_id):
    cursor = get_db_connection().cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT requisition_id FROM candidates WHERE id = %s", (candidate_id,))
    req = cursor.fetchone()
    cursor.execute("SELECT * FROM interview_hierarchy WHERE requisition_id = %s ORDER BY level", (req['requisition_id'],))
    return cursor.fetchall()

def send_teams_invite(interviewer_email, candidate_email, start_time, duration_minutes, subject, location, description, access_token):
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
        f"https://graph.microsoft.com/v1.0/users/{interviewer_email}/events",
        headers=headers,
        json=event_payload
    )

    if response.status_code >= 400:
        raise Exception(f"Failed to send Teams invite: {response.status_code} {response.text}")

    return response.json()
@app.route('/edit_schedule/<int:candidate_id>/<int:level>', methods=['GET', 'POST'])
def edit_schedule(candidate_id, level):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        new_time = request.form['interview_datetime']
        cursor.execute("""
            UPDATE interview_schedule
            SET interview_datetime = %s
            WHERE candidate_id = %s AND level = %s
        """, (new_time, candidate_id, level))
        conn.commit()

        # Optionally: Re-send updated invite
        cursor.execute("SELECT interviewer_email FROM interview_schedule WHERE candidate_id = %s AND level = %s", (candidate_id, level))
        email = cursor.fetchone()['interviewer_email']
        send_teams_invite(email, new_time, candidate_id)  # Re-send invite with updated time

        return redirect(url_for('schedule_interview', candidate_id=candidate_id))

    cursor.execute("SELECT * FROM interview_schedule WHERE candidate_id = %s AND level = %s", (candidate_id, level))
    schedule = cursor.fetchone()
    return render_template('edit_schedule.html', schedule=schedule)

# ------------------------------------------------------------------------------------#
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

@app.route('/mark_completed/<int:candidate_id>/<int:level>', methods=['GET'])
def mark_completed(candidate_id, level):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE interview_schedule
        SET status = 'completed'
        WHERE candidate_id = %s AND level = %s
    """, (candidate_id, level))
    connection.commit()
    flash(f'Level {level} marked as completed!', 'success')
    return redirect(url_for('schedule_interview', candidate_id=candidate_id))


if __name__ == '__main__':
    app.run(debug=True, port=5005)


