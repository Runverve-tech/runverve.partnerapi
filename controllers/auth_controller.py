from flask import jsonify, request, session
from extensions import db
from models.user import User, UserToken
from werkzeug.security import generate_password_hash, check_password_hash

class AuthController:
    @staticmethod
    def exchange_token(code):
        """Exchange authorization code for tokens"""
        # This would integrate with your API client
        # token_data = api.exchange_token(code)
        
        # For demonstration purposes:
        token_data = None
        return {"message": "Token exchange functionality not yet implemented"}, 501

    @staticmethod
    def store_user_session(user_sk):
        """Store user session data"""
        session['user_sk'] = user_sk
        return {"message": "Session stored successfully"}, 200

    @staticmethod
    def check_user_logged_in():
        """Check if user is logged in"""
        if 'user_sk' not in session:
            return False
        return True

    @staticmethod
    def register():
        data = request.get_json()
        if not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({'error': 'Missing required fields'}), 400
            
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'User registered successfully'}), 201

    @staticmethod
    def login():
        data = request.get_json()
        if not all(k in data for k in ['username', 'password']):
            return jsonify({'error': 'Missing required fields'}), 400
            
        user = User.query.filter_by(username=data['username']).first()
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
            
        session['user_sk'] = user.user_sk
        return jsonify({'message': 'Login successful', 'user_sk': user.user_sk}), 200