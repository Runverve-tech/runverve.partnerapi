from flask import jsonify, request
from models.activity import Activity
from extensions import db

class ActivityController:
    """Controller for activity-related operations"""
    
    @staticmethod
    def get_activities():
        """Get all activities"""
        activities = Activity.query.all()
        return jsonify([activity.to_dict() for activity in activities]), 200  # Fixed: activity -> activities
    
    @staticmethod
    def get_activity(activity_id):
        """Get a specific activity by ID"""
        activity = Activity.query.get_or_404(activity_id)
        return jsonify(activity.to_dict()), 200
    
    @staticmethod
    def create_activity():
        """Create a new activity"""
        data = request.get_json()
        
        # Create new activity
        new_activity = Activity(**data)
        
        db.session.add(new_activity)
        db.session.commit()
        
        return jsonify(new_activity.to_dict()), 201
    
    @staticmethod
    def update_activity(activity_id):
        """Update an existing activity"""
        activity = Activity.query.get_or_404(activity_id)
        data = request.get_json()
        
        # Update fields
        for key, value in data.items():
            if hasattr(activity, key):
                setattr(activity, key, value)
        
        db.session.commit()
        return jsonify(activity.to_dict()), 200
    
    @staticmethod
    def delete_activity(activity_id):
        """Delete an activity"""
        activity = Activity.query.get_or_404(activity_id)
        db.session.delete(activity)
        db.session.commit()
        return jsonify({'message': 'Activity deleted successfully'}), 200