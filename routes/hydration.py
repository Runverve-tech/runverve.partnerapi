from flask import Blueprint, request, jsonify
from controllers import hydration_controller
from middleware.auth_middleware import login_required

bp = Blueprint('hydration', __name__)

@bp.route('/hydration', methods=['POST'])
@login_required
def log_hydration(current_user_sk):  # Add the parameter here
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if not data.get('quantity') or not isinstance(data.get('quantity'), int):
            return jsonify({"error": "'quantity' is required and must be an integer"}), 400
        
        # Add user_sk to the data
        data['user_sk'] = current_user_sk
            
        result, status_code = hydration_controller.log_hydration(data)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

