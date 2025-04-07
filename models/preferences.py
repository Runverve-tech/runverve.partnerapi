from datetime import datetime
from extensions import db
from models.supplements import Supplement

class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'
    __module__ = 'models.preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_sk = db.Column(db.Integer, db.ForeignKey('users.user_sk'), nullable=False)
    
    # Update relationship to use back_populates
    # Keep only one of these relationships (remove the other)
    user = db.relationship('User', back_populates='preferences')
    
    # Remove this duplicate relationship
    # user = db.relationship('models.user.User', backref='preferences_rel', lazy=True, uselist=False)
    supplements_id = db.Column(db.Integer, db.ForeignKey('supplements.id'))
    shoe_type = db.Column(db.String(50), nullable=True)
    running_surface = db.Column(db.String(50), nullable=True)
    preferred_distance = db.Column(db.Float, nullable=True)
    preferred_pace = db.Column(db.String(20), nullable=True)
    training_frequency = db.Column(db.Integer, nullable=True)
    weather_preference = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('models.user.User', backref='preferences_rel', lazy=True, uselist=False)
    supplements = db.relationship('Supplement', backref='user_preferences')

    def to_dict(self):
        return {
            'id': self.id,
            'user_sk': self.user_sk,  # Changed from user_id to user_sk
            'shoe_type': self.shoe_type,
            'running_surface': self.running_surface,
            'preferred_distance': self.preferred_distance,
            'preferred_pace': self.preferred_pace,
            'training_frequency': self.training_frequency,
            'weather_preference': self.weather_preference,
            'supplements': self.supplements.to_dict() if self.supplements else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Association table for many-to-many relationship
user_supplement_preferences = db.Table('user_supplement_preferences',
    db.Column('user_preference_id', db.Integer, db.ForeignKey('user_preferences.id'), primary_key=True),
    db.Column('supplement_id', db.Integer, db.ForeignKey('supplements.id'), primary_key=True)
)