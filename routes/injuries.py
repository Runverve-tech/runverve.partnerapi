from flask import Blueprint, request, jsonify
from models.injuries import Injuries, InjuryReport
from extensions import db
from middleware.auth import token_required

bp = Blueprint('injuries', __name__)

@bp.route('/injuries', methods=['GET', 'POST'])
@token_required
def handle_injuries(current_user):
    if request.method == 'GET':
        injuries = Injuries.query.all()
        return jsonify([injury.to_dict() for injury in injuries])

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
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
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/injuries/<int:injury_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def handle_injury(current_user, injury_id):
    injury = Injuries.query.get_or_404(injury_id)

    if request.method == 'GET':
        return jsonify(injury.to_dict())

    elif request.method == 'PUT':
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            for field in ['tennis_elbow', 'muscle_strain', 'bicep_tendonitis', 'fracture', 'forearm_strain']:
                if field in data:
                    setattr(injury, field, data[field])

            db.session.commit()
            return jsonify(injury.to_dict())
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    elif request.method == 'DELETE':
        try:
            db.session.delete(injury)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

@bp.route('/injuries/report', methods=['GET', 'POST'])
@token_required
def handle_injury_reports(current_user):
    if request.method == 'GET':
        reports = InjuryReport.query.filter_by(user_sk=current_user.user_sk).all()
        return jsonify([report.to_dict() for report in reports])

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        report = InjuryReport(
            user_sk=current_user.user_sk,
            injury_id=data.get('injury_id'),
            injury_location=data.get('injury_location'),
            injury_type=data.get('injury_type')
        )
        db.session.add(report)
        db.session.commit()
        return jsonify(report.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/injuries/report/<int:report_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def handle_injury_report(current_user, report_id):
    report = InjuryReport.query.filter_by(
        report_id=report_id,
        user_sk=current_user.user_sk
    ).first_or_404()

    if request.method == 'GET':
        return jsonify(report.to_dict())

    elif request.method == 'PUT':
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            for field in ['injury_location', 'injury_type']:
                if field in data:
                    setattr(report, field, data[field])

            db.session.commit()
            return jsonify(report.to_dict())
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    elif request.method == 'DELETE':
        try:
            db.session.delete(report)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

def init_app(app):
    app.register_blueprint(bp)