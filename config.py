import os
from dotenv import load_dotenv
import os
from datetime import timedelta
from datetime import datetime

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Update database URI to use Neon PostgreSQL
    # Ensure SSL mode for Neon
    database_url = os.environ.get('DATABASE_URL')
    if database_url and 'sslmode' not in database_url:
        database_url += '?sslmode=require'
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    # File upload settings
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max file size 16MB
    
    # API credentials
    CLIENT_ID = os.getenv('CLIENT_ID', 'CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET', 'CLIENT_SECRET')
    REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:5000/exchange_token')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '<your api key>')
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'your-google-client-id')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', 'your-google-client-secret')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
