from flask import Blueprint, request, jsonify
from controllers import hydration_controller
from middleware.auth_middleware import login_required
from datetime import datetime

bp = Blueprint('hydration', __name__)

@bp.route('/hydration', methods=['POST'])
@login_required
def log_hydration(current_user_sk):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if not data.get('quantity') or not isinstance(data.get('quantity'), int):
            return jsonify({"error": "'quantity' is required and must be an integer"}), 400
        
        data['user_sk'] = current_user_sk
            
        result, status_code = hydration_controller.log_hydration(data)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/hydration', methods=['GET'])
@login_required
def get_hydration_logs(current_user_sk):
    try:
        date = request.args.get('date')
        if date:
            try:
                date = datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        
        result, status_code = hydration_controller.get_hydration_logs(current_user_sk, date)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/hydration/<int:log_id>', methods=['PUT'])
@login_required
def update_hydration_log(current_user_sk, log_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if 'quantity' in data and (not isinstance(data['quantity'], int) or data['quantity'] <= 0):
            return jsonify({"error": "Quantity must be a positive integer"}), 400
        
        data['user_sk'] = current_user_sk
        data['log_id'] = log_id
        
        result, status_code = hydration_controller.update_hydration_log(data)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/hydration/<int:log_id>', methods=['DELETE'])
@login_required
def delete_hydration_log(current_user_sk, log_id):
    try:
        result, status_code = hydration_controller.delete_hydration_log(current_user_sk, log_id)
        return jsonify(result) if status_code != 204 else ('', 204)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/hydration/summary', methods=['GET'])
@login_required
def get_hydration_summary(current_user_sk):
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}), 400
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}), 400
        
        result, status_code = hydration_controller.get_hydration_summary(
            current_user_sk, 
            start_date, 
            end_date
        )
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

