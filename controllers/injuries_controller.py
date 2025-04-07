from flask import jsonify, request
from models import Injuries, InjuryReport
from models.user import User
from extensions import db

class InjuriesController:
    @staticmethod
    def get_injuries(user_sk):
        injury_reports = InjuryReport.query.filter_by(user_sk=user_sk).all()
        return jsonify([report.to_dict() for report in injury_reports]), 200

    @staticmethod
    def add_injury(user_sk):
        data = request.get_json()
        if not data.get('injury_location'):
            return jsonify({'error': 'Injury location is required'}), 400
            
        injury = Injuries()
        db.session.add(injury)
        db.session.flush()
        
        injury_report = InjuryReport(
            user_sk=user_sk,
            injury_id=injury.id,
            injury_location=data['injury_location']
        )
        
        db.session.add(injury_report)
        db.session.commit()
        
        return jsonify(injury_report.to_dict()), 201

    @staticmethod
    def report_injury(data):
        """Report user injuries"""
        try:
            user_sk = data.get('user_sk')
            injuries = data.get('injuries')

            user = User.query.filter_by(user_sk=user_sk).first()
            if not user:
                return {"error": "User not found."}, 404

            response = []

            for injury_data in injuries:
                injury_id = injury_data.get('injury_id')
                injury_location = injury_data.get('injury_location')

                injury = Injuries.query.filter_by(id=injury_id).first()
                if not injury:
                    response.append({"error": f"Injury with id {injury_id} not found."})
                    continue

                injury_report = InjuryReport(
                    user_sk=user_sk,
                    injury_id=injury_id,
                    injury_location=injury_location
                )
                db.session.add(injury_report)

                response.append({
                    "injury_id": injury_id,
                    "injury_location": injury_location,
                    "injury_type": {
                        "tennis_elbow": injury.tennis_elbow,
                        "muscle_strain": injury.muscle_strain,
                        "bicep_tendonitis": injury.bicep_tendonitis,
                        "fracture": injury.fracture,
                        "forearm_strain": injury.forearm_strain
                    },
                    "status": "Injury report submitted successfully."
                })

            db.session.commit()
            return response, 200
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to save injury reports: {str(e)}"}, 500