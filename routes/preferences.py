from flask import Blueprint, request, jsonify, g
from models.preferences import UserPreferences
from extensions import db
from middleware.auth_middleware import login_required

bp = Blueprint('preferences', __name__)

@bp.route('/user/preferences', methods=['GET', 'POST'])
@login_required
def handle_user_preferences(current_user_sk):
    if request.method == 'GET':
        preferences = UserPreferences.query.filter_by(user_sk=current_user_sk).first()
        if preferences:
            return jsonify(preferences.to_dict())
        return jsonify({}), 404

    data = request.get_json()
    preferences = UserPreferences.query.filter_by(user_sk=current_user_sk).first()
    
    if not preferences:
        preferences = UserPreferences(user_sk=current_user_sk)
        db.session.add(preferences)
    
    # Update preferences
    for key in ['shoe_type', 'running_surface', 'preferred_distance', 
                'preferred_pace', 'training_frequency', 'weather_preference']:
        if key in data:
            setattr(preferences, key, data[key])
    
    db.session.commit()
    return jsonify(preferences.to_dict()), 200

def init_app(app):
    app.register_blueprint(bp)