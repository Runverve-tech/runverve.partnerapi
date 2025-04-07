from flask import Blueprint, request, jsonify, current_app, redirect, url_for
from models.user import User
from extensions import db
import jwt
from datetime import datetime, timedelta
import secrets
from config import Config
from google.oauth2 import id_token
from google.auth.transport import requests

bp = Blueprint('auth', __name__)

@bp.route('/auth/google', methods=['POST'])
def google_auth():
    data = request.get_json()
    token = data.get('token')
    
    try:
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            Config.GOOGLE_CLIENT_ID
        )

        # Get user info from token
        email = idinfo['email']
        name = idinfo.get('name', email.split('@')[0])
        
        # Find or create user
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                email=email,
                username=name,
                is_google_user=True
            )
            db.session.add(user)
            db.session.commit()
        
        # Generate JWT token
        token = jwt.encode({
            'user_sk': user.user_sk,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, current_app.config['SECRET_KEY'])
        
        return jsonify({
            'token': token,
            'user': {
                'user_sk': user.user_sk,
                'username': user.username,
                'email': user.email
            }
        })
        
    except ValueError:
        return jsonify({'error': 'Invalid token'}), 401

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400
        
    user = User.query.filter_by(username=data['username']).first()
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
        
    if not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = jwt.encode({
        'user_sk': user.user_sk,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, current_app.config['SECRET_KEY'])

    return jsonify({
        'token': token,
        'user': {
            'user_sk': user.user_sk,
            'username': user.username,
            'email': user.email
        }
    })

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if username already exists
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'error': 'Username already exists'}), 400
        
    # Check if email already exists
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    try:
        user = User()
        user.username = data.get('username')
        user.email = data.get('email')
        user.set_password(data.get('password'))
        
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/request-password-reset', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
        
    user = User.query.filter_by(email=email).first()
    if not user:
        # For security, don't reveal if email exists
        return jsonify({'message': 'If the email exists, a reset link will be sent'}), 200
    
    # Generate reset token
    reset_token = secrets.token_urlsafe(32)
    user.reset_token = reset_token
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
    
    db.session.commit()
    
    # TODO: Send email with reset link
    # For development, return token directly
    return jsonify({
        'message': 'Password reset email sent',
        'token': reset_token  # Remove this in production
    }), 200

@bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')
    
    if not token or not new_password:
        return jsonify({'error': 'Token and new password are required'}), 400
    
    user = User.query.filter_by(reset_token=token).first()
    if not user or not user.reset_token_expires or user.reset_token_expires < datetime.utcnow():
        return jsonify({'error': 'Invalid or expired reset token'}), 400
    
    user.set_password(new_password)
    user.reset_token = None
    user.reset_token_expires = None
    
    db.session.commit()
    
    return jsonify({'message': 'Password successfully reset'}), 200

def init_app(app):
    """Initialize auth routes with the Flask app"""
    app.register_blueprint(bp)  # Removed url_prefix to make routes directly accessible