from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, make_response
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
)
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
#from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# Load environment variables
load_dotenv()

# Initialize Flask app and extensions
app = Flask(__name__)
bcrypt = Bcrypt(app)

# JWT configuration
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "super-secret-key")
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "another-secret-key")
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]  # Use cookies for JWT
app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"  # Name of the access token cookie
app.config["JWT_COOKIE_SECURE"] = False  # Set to True in production with HTTPS
app.config["JWT_COOKIE_CSRF_PROTECT"] = True  # Protect against CSRF

jwt = JWTManager(app)

# Flask-Limiter setup (commented out here)
""" limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
) """

# Database connection helper
def get_db_connection():
    return connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "flask_nb_me"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432")
    )

# Helper to find user by ID
def find_user_by_id(user_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return cursor.fetchone()

# Helper to find user by email
def find_user_by_email(email):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cursor.fetchone()

# Helper for better JSON responses
def response(success, message, data=None, status=200):
    return jsonify({
        "success": success,
        "message": message,
        "data": data
    }), status

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register_view():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([username, email, password]):
            flash("All fields are required.", "error")
            return render_template('register.html')

        if find_user_by_email(email):
            flash("Email is already registered.", "error")
            return render_template('register.html')

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO users (username, email, password_hash) 
                        VALUES (%s, %s, %s)
                        """,
                        (username, email, password_hash)
                    )
                    conn.commit()
            flash("User registered successfully!", "success")
            return redirect(url_for('login_view'))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate input
        if not all([email, password]):
            flash("Email and password are required.", "error")
            return render_template('login.html')

        # Authenticate user
        user = find_user_by_email(email)
        if not user or not bcrypt.check_password_hash(user['password_hash'], password):
            flash("Invalid email or password.", "error")
            return render_template('login.html')

        # Generate JWT token
        access_token = create_access_token(identity=str(user['id']))

        # Set token as a secure HttpOnly cookie
        response = make_response(redirect(url_for('dashboard_view')))
        set_access_cookies(response, access_token)
        flash("Login successful!", "success")
        return response

    # Render login page for GET requests
    return render_template('login.html')

# Logout Route
@app.route('/logout', methods=['GET'])
def logout_view():
    response = make_response(redirect(url_for('login_view')))
    unset_jwt_cookies(response)
    flash("You have been logged out.", "success")
    return response

# Dashboard Route
@app.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard_view():
    user_id = get_jwt_identity()
    user = find_user_by_id(user_id)

    if not user:
        flash("User not found.", "error")
        return redirect(url_for('login_view'))

    return render_template('dashboard.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
