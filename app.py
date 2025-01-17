from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app and extensions
app = Flask(__name__)
bcrypt = Bcrypt(app)

# JWT configuration
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "super-secret-key")
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "another-secret-key")  # For flash messages
jwt = JWTManager(app)

# Database connection helper
def get_db_connection():
    return connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "flask_nb_me"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432")
    )

# Helper to find user by email
def find_user_by_email(email):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cursor.fetchone()

# Register View (HTML)
@app.route('/register', methods=['GET', 'POST'])
def register_view():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate input
        if not all([username, email, password]):
            flash("All fields are required.", "error")
            return render_template('register.html')

        # Check if user exists
        if find_user_by_email(email):
            flash("Email is already registered.", "error")
            return render_template('register.html')

        # Hash password and create user
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

# Login View (HTML)
@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate input
        if not all([email, password]):
            flash("Email and password are required.", "error")
            return render_template('login.html')

        # Find user
        user = find_user_by_email(email)
        if not user or not bcrypt.check_password_hash(user['password_hash'], password):
            flash("Invalid email or password.", "error")
            return render_template('login.html')

        # Generate JWT token
        access_token = create_access_token(identity=user['id'])
        flash("Login successful!", "success")
        return render_template('protected.html', access_token=access_token)

    return render_template('login.html')

# Protected View (HTML)
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected_view():
    user_id = get_jwt_identity()
    return render_template('protected.html', user_id=user_id)

if __name__ == '__main__':
    app.run(debug=True)
