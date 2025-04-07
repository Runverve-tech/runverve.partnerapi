from flask import jsonify, request, session
from extensions import db
from models.user import User, UserInfo
from models.preferences import UserPreferences

def create_user(username, email):
    """Create a new user"""
    try:
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created", "user_sk": new_user.user_sk}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def get_all_users():
    """Get all users"""
    try:
        users = User.query.all()
        return [{"user_sk": user.user_sk, "username": user.username, "email": user.email} for user in users], 200
    except Exception as e:
        return {"error": str(e)}, 500

def get_user_profile(user_id=None, username=None):
    """Get user profile by ID or username"""
    try:
        if user_id:
            user = UserInfo.query.get(user_id)
        elif username:
            user = UserInfo.query.filter_by(username=username).first()
        else:
            return {"message": "Please provide either 'id' or 'username'"}, 400

        if not user:
            return {"message": "User not found"}, 404

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
        return user_data, 200
    except Exception as e:
        return {"error": str(e)}, 500

def create_user_profile(data):
    """Create a new user profile"""
    try:
        if UserInfo.query.filter_by(username=data.get('username')).first():
            return {"message": "Username already exists"}, 400
        if UserInfo.query.filter_by(email_id=data.get('email_id')).first():
            return {"message": "Email already exists"}, 400

        # Validation handled by utils.validators in the route

        new_user = UserInfo(
            username=data.get('username'),
            email_id=data.get('email_id'),
            password=data.get('password'),
            gender=data.get('gender'),
            date_of_birth=data.get('date_of_birth'),
            height=float(data.get('height')),
            weight=float(data.get('weight')),
            experience_level=data.get('experience_level'),
            distance_goal=data.get('distance_goal'),
            preferences=data.get('preferences'),
            mobile_no=data.get('mobile_no')
        )

        db.session.add(new_user)
        db.session.commit()
        return {"message": "User profile created successfully"}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def update_user_profile(user_id, data):
    """Update a user profile"""
    try:
        user = UserInfo.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        # Username check
        if 'username' in data:
            existing_user = UserInfo.query.filter_by(username=data['username']).first()
            if existing_user and existing_user.id != user_id:
                return {"message": "Username already exists"}, 400
            user.username = data['username']
        
        # Update other fields (validation handled by utils.validators in the route)
        if 'password' in data:
            user.password = data['password']
        
        if 'height' in data:
            user.height = float(data['height'])
        
        if 'weight' in data:
            user.weight = float(data['weight'])

        if 'experience_level' in data:
            user.experience_level = data['experience_level']
        
        if 'distance_goal' in data:
            user.distance_goal = float(data['distance_goal'])

        if 'preferences' in data:
            user.preferences = data['preferences']
        
        if 'mobile_no' in data:
            user.mobile_no = data['mobile_no']

        db.session.commit()
        return {"message": "User profile updated successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


class UserController:
    @staticmethod
    def get_user_profile(user_sk):
        user = User.query.filter_by(user_sk=user_sk).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.to_dict()), 200

    @staticmethod
    def update_user_profile(user_sk):
        data = request.get_json()
        user = User.query.filter_by(user_sk=user_sk).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        db.session.commit()
        return jsonify(user.to_dict()), 200

    @staticmethod
    def get_user_preferences(user_sk):
        preferences = UserPreferences.query.filter_by(user_id=user_sk).first()
        if not preferences:
            return jsonify({'error': 'Preferences not found'}), 404
        return jsonify(preferences.to_dict()), 200

    @staticmethod
    def update_user_preferences(user_sk):
        data = request.get_json()
        preferences = UserPreferences.query.filter_by(user_id=user_sk).first()
        
        if not preferences:
            preferences = UserPreferences(user_id=user_sk)
            db.session.add(preferences)

        for key, value in data.items():
            if hasattr(preferences, key):
                setattr(preferences, key, value)

        db.session.commit()
        return jsonify(preferences.to_dict()), 200