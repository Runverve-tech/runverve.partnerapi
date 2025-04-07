from flask import jsonify, request
from models import Supplement
from extensions import db

class SupplementsController:
    @staticmethod
    def get_supplements(user_sk):
        supplements = Supplement.query.filter_by(user_sk=user_sk).all()
        return jsonify([supplement.to_dict() for supplement in supplements]), 200

    @staticmethod
    def add_supplement(user_sk):
        data = request.get_json()
        
        required_fields = ['name', 'dosage', 'frequency']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
            
        supplement = Supplement(
            user_sk=user_sk,
            name=data['name'],
            dosage=data['dosage'],
            frequency=data['frequency']
        )
        
        db.session.add(supplement)
        db.session.commit()
        
        return jsonify(supplement.to_dict()), 201