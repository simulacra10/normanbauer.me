import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os



import psycopg2
from psycopg2 import sql

def create_tables():
    try:

        # Load environment variables from .env file
        load_dotenv()

        #Retrieve database credentials from environment variables
        db_host = os.getenv("DB_HOST", "localhost")  # Default to localhost if not provided
        db_name = os.getenv("DB_NAME", "flask_nb_me")  # Default to "flask_nb_me" if not provided
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_port = os.getenv("DB_PORT", "5432")  # Default to port 5432 if not provided

        # Validate that all required variables are set
        if not all([db_user, db_password]):
            raise ValueError("Missing required database credentials in the .env file.")

        # Connect to your PostgreSQL database
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        cursor = conn.cursor()

        # Create Users table
        # Create Categories table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            slug VARCHAR(100) UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Create Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            bio TEXT,
            profile_picture VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Create Posts table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            slug VARCHAR(255) UNIQUE NOT NULL,
            content TEXT NOT NULL,
            author_id INT REFERENCES users(id) ON DELETE CASCADE,
            category_id INT REFERENCES categories(id) ON DELETE SET NULL,
            tags JSONB,
            status VARCHAR(20) DEFAULT 'draft',
            published_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)


        # Commit changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()

        print("Tables created successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_tables()
