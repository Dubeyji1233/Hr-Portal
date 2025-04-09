from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import msal
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
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
            if password == user.get("password_hash"):  # Ideally, use hashing here
                session["user"] = {"email": user["email"], "name": user["name"], "role": user.get("role", "Static")}
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
        code, scopes=SCOPE,
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
        if conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
                if not user:
                    cursor.execute("INSERT INTO users (email, name, azure_oid) VALUES (%s, %s, %s)", (email, name, oid))
                    conn.commit()
            conn.close()

        session["user"] = {"email": email, "name": name, "role": "Employee"}  # You can change role logic later
        return redirect(url_for('home'))
    else:
        return "SSO Login failed", 401

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', user=session['user'])

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
