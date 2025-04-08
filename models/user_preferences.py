from datetime import datetime
from extensions import db
from models.supplements import Supplement
from models.user import User

user_supplement_preferences = db.Table(
    'user_supplement_preferences',
    db.Column('user_preference_id', db.Integer, db.ForeignKey('user_preferences.id'), primary_key=True),
    db.Column('supplement_id', db.Integer, db.ForeignKey('supplements.id'), primary_key=True)
)

class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_sk = db.Column(db.Integer, db.ForeignKey('users.user_sk'), nullable=False)
    shoe_type_id = db.Column(db.Integer, db.ForeignKey('shoe_type.id'))
    injuries_id = db.Column(db.Integer, db.ForeignKey('injuries.id'))
    running_surface = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='preferences')  # ✅ match 'preferences' from User model
    shoe_type = db.relationship('ShoeType', backref='user_preferences')
    injuries = db.relationship('Injuries', backref='user_preferences')
    supplements = db.relationship('Supplement', secondary=user_supplement_preferences, backref='user_preferences')

    def to_dict(self):
        return {
            'id': self.id,
            'user_sk': self.user_sk,
            'running_surface': self.running_surface,
            'shoe_type': self.shoe_type.to_dict() if self.shoe_type else None,
            'injuries': self.injuries.to_dict() if self.injuries else None,
            'supplements': [s.to_dict() for s in self.supplements] if self.supplements else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
