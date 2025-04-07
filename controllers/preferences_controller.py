from flask import jsonify, request
from extensions import db
from models.preferences import UserPreferences

class PreferencesController:
    @staticmethod
    def get_preferences(user_id):
        preferences = UserPreferences.query.filter_by(user_id=user_id).first()
        if not preferences:
            return jsonify({'error': 'Preferences not found'}), 404
        return jsonify(preferences.to_dict()), 200

    @staticmethod
    def update_preferences(user_id):
        data = request.get_json()
        preferences = UserPreferences.query.filter_by(user_id=user_id).first()
        
        if not preferences:
            preferences = UserPreferences(user_id=user_id)
            db.session.add(preferences)

        for key, value in data.items():
            if hasattr(preferences, key):
                setattr(preferences, key, value)

        try:
            db.session.commit()
            return jsonify(preferences.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500