from flask import jsonify, request, session
from extensions import db
from models.user import User, UserInfo
from models.user_preferences import UserPreferences

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

class UserController:
    @staticmethod
    def create_user_profile(data):
        try:
            # Create new user profile
            user = User(
                email=data.get('email_id'),
                username=data.get('username'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                mobile_no=data.get('mobile_no')
            )
            
            db.session.add(user)
            db.session.commit()
            
            return {
                "message": "User profile created successfully",
                "user": {
                    "user_sk": user.user_sk,
                    "email": user.email,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "mobile_no": user.mobile_no
                }
            }, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

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