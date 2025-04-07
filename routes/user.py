from flask import Blueprint, request, jsonify
from controllers import user_controller
from middleware.auth_middleware import login_required
from utils.validators import validate_email, validate_password, validate_phone_number
from controllers.user_controller import UserController

bp = Blueprint('user', __name__)

@bp.route('/profile/<int:user_sk>', methods=['GET'])
def get_profile(user_sk):
    return UserController.get_user_profile(user_sk)

@bp.route('/profile/<int:user_sk>', methods=['PUT'])
def update_profile(user_sk):
    return UserController.update_user_profile(user_sk)

@bp.route('/preferences/<int:user_sk>', methods=['GET'])
def get_preferences(user_sk):
    return UserController.get_user_preferences(user_sk)

@bp.route('/preferences/<int:user_sk>', methods=['PUT'])
def update_preferences(user_sk):
    return UserController.update_user_preferences(user_sk)

@bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid input"}), 400
    return user_controller.create_user(data.get('username'), data.get('email'))

@bp.route('/', methods=['GET'])
def get_users():
    result, status_code = user_controller.get_all_users()
    return jsonify(result), status_code

@bp.route('/profile', methods=['GET'])
def get_user():
    user_id = request.args.get('id', type=int)
    username = request.args.get('username', type=str)
    result, status_code = user_controller.get_user_profile(user_id, username)
    return jsonify(result), status_code

@bp.route('/profile', methods=['POST'])
def create_user_profile():
    data = request.json
    if not data:
        return jsonify({"message": "Invalid input"}), 400

    if not validate_email(data.get('email_id')):
        return jsonify({"message": "Invalid email format"}), 400
        
    if not validate_password(data.get('password')):
        return jsonify({"message": "Password must be at least 8 characters long, include a number, an uppercase letter, and a special character"}), 400
        
    if data.get('mobile_no') and not validate_phone_number(data.get('mobile_no')):
        return jsonify({"message": "Mobile number must be a 10-digit numeric value"}), 400
        
    result, status_code = user_controller.create_user_profile(data)
    return jsonify(result), status_code

@bp.route('/profile/update', methods=['PUT'])
def update_user_profile():
    user_id = request.args.get('id', type=int)
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400
        
    data = request.json
    if not data:
        return jsonify({"message": "Invalid input"}), 400
        
    if 'password' in data and not validate_password(data['password']):
        return jsonify({"message": "Password must be at least 8 characters long, include a number, an uppercase letter, and a special character"}), 400
        
    if 'mobile_no' in data and not validate_phone_number(data['mobile_no']):
        return jsonify({"message": "Mobile number must be a 10-digit numeric value"}), 400
        
    result, status_code = user_controller.update_user_profile(user_id, data)
    return jsonify(result), status_code

def init_app(app):
    app.register_blueprint(bp, url_prefix='/users')