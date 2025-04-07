from extensions import db
from datetime import datetime

class Photo(db.Model):
    __tablename__ = 'photos'
    __module__ = 'models.photos'
    
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_sk = db.Column(db.Integer, db.ForeignKey('users.user_sk'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    photo_data = db.Column(db.LargeBinary, nullable=False)
    
    user = db.relationship('models.user.User', backref='photos_rel', lazy=True)

class SupplementPhoto(db.Model):
    """User uploaded supplement photos"""
    __tablename__ = 'supplement_photos'
    __module__ = 'models.photos'
    
    pic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_sk = db.Column(db.Integer, db.ForeignKey('users.user_sk'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    supplement_type = db.Column(db.String(100), nullable=False)
    photo_data = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Add relationship with unique backref
    user = db.relationship('models.user.User', backref='supplement_photos_rel', lazy=True)