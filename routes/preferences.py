from flask import Blueprint, request, jsonify
from models.user_preferences import UserPreferences
from extensions import db
from middleware.auth_middleware import login_required
from models.shoe_type import ShoeType
from models.injuries import Injuries
from models.supplements import Supplement

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

    # Update simple fields
    if 'running_surface' in data:
        preferences.running_surface = data['running_surface']

    # Update relationships
    if 'shoe_type_id' in data:
        preferences.shoe_type_id = data['shoe_type_id']

    if 'injuries_id' in data:
        preferences.injuries_id = data['injuries_id']

    # Update many-to-many supplements
    if 'supplements' in data:
        supplement_ids = data['supplements']
        supplements = Supplement.query.filter(Supplement.id.in_(supplement_ids)).all()
        preferences.supplements = supplements

    db.session.commit()
    return jsonify(preferences.to_dict()), 200

def init_app(app):
    app.register_blueprint(bp)
