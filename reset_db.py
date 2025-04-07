from extensions import db
from app import create_app
from sqlalchemy import text

def reset_database():
    app = create_app()
    with app.app_context():
        # Get database connection
        connection = db.engine.connect()
        
        # Drop and recreate schema
        connection.execute(text("""
            DROP SCHEMA public CASCADE;
            CREATE SCHEMA public;
        """))
        connection.commit()
        
        # Create all tables
        db.create_all()
        print("Database reset successfully!")

if __name__ == "__main__":
    reset_database()