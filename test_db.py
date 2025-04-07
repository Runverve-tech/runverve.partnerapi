from extensions import db
from app import create_app
from sqlalchemy import text

def test_connection():
    app = create_app()
    with app.app_context():
        try:
            # Test the connection
            result = db.session.execute(text('SELECT 1'))
            print("Database connection successful!")
            
            # Show current tables
            result = db.session.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            print("\nCurrent tables in database:")
            for row in result:
                print(f"- {row[0]}")
                
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            db.session.close()

if __name__ == "__main__":
    test_connection()