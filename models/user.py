from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    __module__ = 'models.user'
    
    user_sk = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)
    # Update relationships to use back_populates
    preferences = db.relationship('UserPreferences', back_populates='user', uselist=False)
    injuries = db.relationship('InjuryReport', back_populates='user')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'user_sk': self.user_sk,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'preferences': self.preferences.to_dict() if self.preferences else None
        }

class UserToken(db.Model):
    __tablename__ = 'user_token'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_sk = db.Column(db.Integer, db.ForeignKey('users.user_sk'))
    platform = db.Column(db.String(100), nullable=False)
    access_token = db.Column(db.String(255), nullable=False)
    access_token_secret = db.Column(db.String(255), nullable=False)
    refresh_token = db.Column(db.String(255))

class UserInfo(db.Model):
    __tablename__ = 'user_info'
    __module__ = 'models.user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_sk = db.Column(db.Integer, db.ForeignKey('users.user_sk'), nullable=False)  # Added foreign key
    username = db.Column(db.String(50), unique=True, nullable=False)
    email_id = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    height = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    experience_level = db.Column(db.String(50), nullable=True)
    distance_goal = db.Column(db.Float, nullable=True)
    preferences = db.Column(db.Text, nullable=True)
    mobile_no = db.Column(db.String(15), nullable=True)



class Photo(db.Model):
    __tablename__ = 'photos'
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_sk = db.Column(db.Integer, db.ForeignKey('users.user_sk'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    photo_data = db.Column(db.LargeBinary, nullable=False)