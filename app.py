from flask import Flask
from flask_migrate import Migrate
from extensions import db
from config import Config
from routes import init_app as init_routes
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Set secret key for session management
    app.secret_key = Config.SECRET_KEY
    
    db.init_app(app)
    Migrate(app, db)
    
    # Import models here to ensure they're registered
    from models.user import User
    from models.preferences import UserPreferences
    from models.supplements import Supplement, SupplementPhoto, UserSupplement
    from models.hydration import HydrationLog
    from models.shoe_type import ShoeType
    from models.spark_points import SparkLedger
    from models.injuries import InjuryReport
    from models.activity import Activity
    from models.geocoding import GeocodingResult
    
    # Register blueprints
    from routes.auth import bp as auth_bp
    from routes.preferences import bp as preferences_bp
    from routes.supplements import bp as supplements_bp
    from routes.hydration import bp as hydration_bp
    from routes.geocoding import bp as geocoding_bp
    from routes.injuries import bp as injuries_bp
    from routes.activity import bp as activity_bp
    from routes.spark_points import bp as spark_points_bp  # Add this import
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(preferences_bp)
    app.register_blueprint(supplements_bp)
    app.register_blueprint(hydration_bp)
    app.register_blueprint(geocoding_bp)
    app.register_blueprint(injuries_bp)
    app.register_blueprint(activity_bp)
    app.register_blueprint(spark_points_bp)  # Add this line
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)