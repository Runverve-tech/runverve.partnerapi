from flask import Blueprint, request, jsonify
from models.user_preferences import UserPreferences
from extensions import db
from middleware.auth_middleware import login_required
from models.shoe_type import ShoeType
from models.injuries import Injuries
from models.supplements import Supplement

bp = Blueprint('preferences', __name__)

@bp.route('/user/preferences', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def handle_user_preferences(current_user_sk):
    if request.method == 'GET':
        try:
            preferences = UserPreferences.query.filter_by(user_sk=current_user_sk).first()
            if preferences:
                return jsonify(preferences.to_dict())
            return jsonify({"message": "No preferences found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            preferences = UserPreferences.query.filter_by(user_sk=current_user_sk).first()
            if preferences:
                return jsonify({"error": "Preferences already exist. Use PUT to update"}), 409

            preferences = UserPreferences(user_sk=current_user_sk)
            update_preferences(preferences, data)
            db.session.add(preferences)
            db.session.commit()
            return jsonify(preferences.to_dict()), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    elif request.method == 'PUT':
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            preferences = UserPreferences.query.filter_by(user_sk=current_user_sk).first()
            if not preferences:
                return jsonify({"error": "Preferences not found"}), 404

            update_preferences(preferences, data)
            db.session.commit()
            return jsonify(preferences.to_dict())

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    elif request.method == 'DELETE':
        try:
            preferences = UserPreferences.query.filter_by(user_sk=current_user_sk).first()
            if not preferences:
                return jsonify({"error": "Preferences not found"}), 404

            db.session.delete(preferences)
            db.session.commit()
            return '', 204

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

def update_preferences(preferences, data):
    # Update simple fields
    if 'running_surface' in data:
        if not isinstance(data['running_surface'], str):
            raise ValueError("running_surface must be a string")
        preferences.running_surface = data['running_surface']

    # Update relationships with validation
    if 'shoe_type_id' in data:
        shoe_type = ShoeType.query.get(data['shoe_type_id'])
        if not shoe_type:
            raise ValueError(f"Shoe type with ID {data['shoe_type_id']} not found")
        preferences.shoe_type_id = data['shoe_type_id']

    if 'injuries_id' in data:
        injury = Injuries.query.get(data['injuries_id'])
        if not injury:
            raise ValueError(f"Injury with ID {data['injuries_id']} not found")
        preferences.injuries_id = data['injuries_id']

    # Update many-to-many supplements with validation
    if 'supplements' in data:
        if not isinstance(data['supplements'], list):
            raise ValueError("supplements must be a list of IDs")
        supplements = Supplement.query.filter(Supplement.id.in_(data['supplements'])).all()
        if len(supplements) != len(data['supplements']):
            raise ValueError("One or more supplement IDs are invalid")
        preferences.supplements = supplements

@bp.route('/user/preferences/supplements', methods=['GET'])
@login_required
def get_user_supplements(current_user_sk):
    try:
        preferences = UserPreferences.query.filter_by(user_sk=current_user_sk).first()
        if not preferences:
            return jsonify({"message": "No preferences found"}), 404
        
        supplements = [supplement.to_dict() for supplement in preferences.supplements]
        return jsonify(supplements)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def init_app(app):
    app.register_blueprint(bp)
