from flask import Blueprint, request, jsonify
from models.user import User, UserInfo
from extensions import db
from utils.validators import validate_email, validate_phone_number
import re

bp = Blueprint('user', __name__)

@bp.route('/profile', methods=['GET'])
def get_user_profile():
    """Retrieve a user profile by ID or username."""
    user_id = request.args.get('id', type=int)
    username = request.args.get('username', type=str)

    if user_id:
        user = UserInfo.query.get(user_id)
    elif username:
        user = UserInfo.query.filter_by(username=username).first()
    else:
        return jsonify({"message": "Please provide either 'id' or 'username' as a query parameter."}), 400

    if not user:
        return jsonify({"message": "User not found"}), 404

    user_data = {
        "username": user.username,
        "email_id": user.email_id,
        "gender": user.gender,
        "date_of_birth": user.date_of_birth,
        "height": user.height,
        "weight": user.weight,
        "experience_level": user.experience_level,
        "distance_goal": user.distance_goal,
        "preferences": user.preferences,
        "mobile_no": user.mobile_no
    }
    return jsonify(user_data), 200

@bp.route('/profile', methods=['POST'])
def create_user_profile():
    """Create a new user profile."""
    data = request.json
    if not data:
        return jsonify({"message": "Invalid input"}), 400

    if UserInfo.query.filter_by(username=data.get('username')).first():
        return jsonify({"message": "Username already exists"}), 400
    if UserInfo.query.filter_by(email_id=data.get('email_id')).first():
        return jsonify({"message": "Email already exists"}), 400

    try:
        height = float(data.get('height')) if data.get('height') else None
        weight = float(data.get('weight')) if data.get('weight') else None
    except ValueError:
        return jsonify({"message": "Height and Weight must be numeric"}), 400

    try:
        # Create User record first with more fields
        user = User(
            username=data.get('username'),
            email=data.get('email_id'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            mobile_no=data.get('mobile_no')
        )
        db.session.add(user)
        db.session.flush()

        # Now create UserInfo record
        new_user = UserInfo(
            user_sk=user.user_sk,
            username=data.get('username'),
            email_id=data.get('email_id'),
            password=data.get('password'),  # This is now optional
            gender=data.get('gender'),
            date_of_birth=data.get('date_of_birth'),
            height=height,
            weight=weight,
            experience_level=data.get('experience_level'),
            distance_goal=data.get('distance_goal'),
            preferences=data.get('preferences'),
            mobile_no=data.get('mobile_no')
        )

        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User profile created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/profile/update', methods=['PUT'])
def update_user_profile():
    """Update a user profile by user ID."""
    user_id = request.args.get('id', type=int)
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400

    user = UserInfo.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    if not data:
        return jsonify({"message": "Invalid input"}), 400

    # Update fields if provided
    for field in ['username', 'gender', 'experience_level', 'preferences', 'mobile_no']:
        if field in data:
            setattr(user, field, data[field])

    # Handle numeric fields
    if 'height' in data:
        try:
            user.height = float(data['height'])
        except ValueError:
            return jsonify({"message": "Height must be a numeric value"}), 400

    if 'weight' in data:
        try:
            user.weight = float(data['weight'])
        except ValueError:
            return jsonify({"message": "Weight must be a numeric value"}), 400

    if 'distance_goal' in data:
        try:
            user.distance_goal = float(data['distance_goal'])
        except ValueError:
            return jsonify({"message": "Distance goal must be a numeric value"}), 400

    db.session.commit()
    return jsonify({"message": "User profile updated successfully"}), 200

def init_app(app):
    app.register_blueprint(bp, url_prefix='/users')