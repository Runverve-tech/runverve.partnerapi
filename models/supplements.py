from extensions import db
from datetime import datetime

class Supplement(db.Model):
    __tablename__ = 'supplements'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    # Add relationship to photos
    photos = db.relationship('SupplementPhoto', backref='supplement_rel', lazy=True)

class SupplementPhoto(db.Model):
    __tablename__ = 'supplement_photos'
    __module__ = 'models.supplements'
    
    id = db.Column(db.Integer, primary_key=True)
    supplement_id = db.Column(db.Integer, db.ForeignKey('supplements.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    photo_data = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserSupplement(db.Model):
    __tablename__ = 'user_supplements'
    __module__ = 'models.supplements'

    id = db.Column(db.Integer, primary_key=True)
    user_sk = db.Column(db.Integer, db.ForeignKey('users.user_sk'), nullable=False)
    supplement_id = db.Column(db.Integer, db.ForeignKey('supplements.id'), nullable=False)
    dosage = db.Column(db.String(50))
    frequency = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Define relationships with correct model names
    user = db.relationship('models.user.User', backref='user_supplements_rel', lazy=True)
    supplement = db.relationship('Supplement', backref='user_supplements_rel', lazy=True)