from flask import jsonify, request
from extensions import db
from models.preferences import UserPreferences
from models.supplements import Supplement

class PreferencesController:
    @staticmethod
    def get_preferences(user_sk):
        preferences = UserPreferences.query.filter_by(user_sk=user_sk).first()
        if not preferences:
            return jsonify({'error': 'Preferences not found'}), 404
        return jsonify(preferences.to_dict()), 200

    @staticmethod
    def update_preferences(user_sk):
        data = request.get_json()
        preferences = UserPreferences.query.filter_by(user_sk=user_sk).first()

        if not preferences:
            preferences = UserPreferences(user_sk=user_sk)
            db.session.add(preferences)

        # Simple field
        if 'running_surface' in data:
            preferences.running_surface = data['running_surface']

        # FK relationships
        if 'shoe_type_id' in data:
            preferences.shoe_type_id = data['shoe_type_id']
        if 'injuries_id' in data:
            preferences.injuries_id = data['injuries_id']

        # Many-to-many relationship (supplements)
        if 'supplements' in data:
            supplement_ids = data['supplements']
            supplements = Supplement.query.filter(Supplement.id.in_(supplement_ids)).all()
            preferences.supplements = supplements

        try:
            db.session.commit()
            return jsonify(preferences.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
