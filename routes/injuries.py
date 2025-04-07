from flask import Blueprint, request, jsonify
from models.injuries import Injuries, InjuryReport
from extensions import db
from middleware.auth import token_required

bp = Blueprint('injuries', __name__)

@bp.route('/injuries', methods=['POST'])
@token_required
def create_injury(current_user):  # Added current_user parameter
    data = request.get_json()
    injury = Injuries(
        tennis_elbow=data.get('tennis_elbow', False),
        muscle_strain=data.get('muscle_strain', False),
        bicep_tendonitis=data.get('bicep_tendonitis', False),
        fracture=data.get('fracture', False),
        forearm_strain=data.get('forearm_strain', False)
    )
    db.session.add(injury)
    db.session.commit()
    return jsonify(injury.to_dict()), 201

@bp.route('/injuries/report', methods=['POST'])
@token_required
def create_injury_report(current_user):  # Added current_user parameter
    data = request.get_json()
    report = InjuryReport(
        user_sk=data.get('user_sk'),
        injury_id=data.get('injury_id'),
        injury_location=data.get('injury_location'),
        injury_type=data.get('injury_type')
    )
    db.session.add(report)
    db.session.commit()
    return jsonify(report.to_dict()), 201

def init_app(app):
    app.register_blueprint(bp)