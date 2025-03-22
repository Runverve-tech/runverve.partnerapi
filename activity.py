from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime
import datetime as dt
import os
from dotenv import load_dotenv
import facebook as fb

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

app.secret_key = os.getenv('SERVER_SECRET_KEY')


# Load database URI directly from the environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
# Disable modification tracking overhead
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Define the User model


class User(db.Model):
    __tablename__ = 'users'
    user_sk = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Define the Activity model

class Activity(db.Model):
    __tablename__ = 'activity'
    activity_id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey('users.user_sk'), nullable=False)
    name = db.Column(db.String(255))
    distance = db.Column(db.Float, default=0.0)
    moving_time = db.Column(db.Integer, default=0)
    elapsed_time = db.Column(db.Integer, default=0)
    total_elevation_gain = db.Column(db.Float, default=0.0)
    type = db.Column(db.String(50), db.Enum('run', 'walk', 'hike', 'swim', 'ride', name='type_enum'))
    start_date = db.Column(db.DateTime, default=dt.date.today())
    description = db.Column(db.Text)
    calories = db.Column(db.Float, default=0.0)
    
# Routes to interact with users


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"user_sk": user.user_sk, "username": user.username, "email": user.email} for user in users])


@app.before_request
def create_tables():
    db.create_all()

# Start of the activities part.

@app.route("/activity", methods=["GET"])
def get_activities():
    
    try:
       activities = Activity.query.all()
    except:
       return jsonify({"error": "Internal server error."}), 500
    
    return jsonify([{
        
        "activity_id": activity.activity_id,
        "athlete_id": activity.athlete_id,
        "name": activity.name,
        "distance": activity.distance,
        "moving_time": activity.moving_time,
        "elapsed_time": activity.elapsed_time,
        "total_elevation_gain": activity.total_elevation_gain,
        "type": activity.type,
        "start_date": activity.start_date,
        "description": activity.description,
        "calories": activity.calories
        
    } for activity in activities])
    
@app.route("/activity/athletes/<athlete_id>", methods=["GET"])
def get_activities_by_athlete(athlete_id):
    
    try:
       id_exists = User.query.get(athlete_id)
    except:
       return jsonify({"error": "Internal server error."}), 500
    
    if not id_exists:
        return jsonify({"error": "Invalid athlete ID"}), 400
    
    activities = Activity.query.filter_by(athlete_id=athlete_id)
    
    return jsonify([{
        
        "activity_id": activity.activity_id,
        "athlete_id": activity.athlete_id,
        "name": activity.name,
        "distance": activity.distance,
        "moving_time": activity.moving_time,
        "elapsed_time": activity.elapsed_time,
        "total_elevation_gain": activity.total_elevation_gain,
        "type": activity.type,
        "start_date": activity.start_date,
        "description": activity.description,
        "calories": activity.calories
        
    } for activity in activities])
    
@app.route("/activity/<activity_id>", methods=["GET"])
def get_activity_by_id(activity_id):
    

    try:
       activity = Activity.query.filter_by(activity_id=activity_id).first()
    except:
       return jsonify({"error": "Internal server error."}), 500
    
    
    if not activity:
        return jsonify({"error": "Activity not found."}), 404
    
    return jsonify({
        
        "activity_id": activity.activity_id,
        "athlete_id": activity.athlete_id,
        "name": activity.name,
        "distance": activity.distance,
        "moving_time": activity.moving_time,
        "elapsed_time": activity.elapsed_time,
        "total_elevation_gain": activity.total_elevation_gain,
        "type": activity.type,
        "start_date": activity.start_date,
        "description": activity.description,
        "calories": activity.calories
        
    })
    
    
@app.route("/activity/<athlete_id>", methods=["POST"])
def create_activity(athlete_id):
    '''
    Required JSON
    
    {
        "name": <activity_name>,
        "type": <type_of_the_activity>, # (--> it can be: 'run', 'walk', 'hike', 'swim' or 'ride')
        "description": <description_of_the_activity>,
    }
    '''
    
    try:
        id_exists = db.session.query(User).filter_by(user_sk=athlete_id).first()
    
    except:
        return jsonify({"error": "Internal server error."}), 500
        
    
    
    if not id_exists:
        return jsonify({"error": "Invalid athlete ID"}), 400
    
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid input. JSON data is required."}), 400
    
    activity_types =  ['run', 'walk', 'hike', 'swim', 'ride']
    
    if data['type'] not in activity_types:
        return jsonify({"error": "Invalid activity type."}), 400
    
    required_fields = [ "name", "type", "description" ]
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    
    new_activity = Activity(name=data["name"], type=data["type"], description=data["description"], athlete_id=athlete_id)
    db.session.add(new_activity)
    db.session.commit()
    return jsonify({"message": "New activity named '"+data["name"]+"' created successfully.", "activity_id": new_activity.activity_id}), 201

@app.route("/activity/<activity_id>", methods=["DELETE"])
def delete_activity(activity_id):
    
    try:
       activity = Activity.query.filter_by(activity_id=activity_id).first()
    except:
       return jsonify({"error": "Internal server error."}), 500
    
    
    if not activity:
        return jsonify({"error": "Activity not found."}), 404
    
    db.session.delete(activity)
    db.session.commit()
    
    return jsonify({"message": "Activity deleted successfully."}), 200

# End of the activities part.


if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 8000))  # Railway provides a PORT env variable
    app.run(host="0.0.0.0", port=PORT)
