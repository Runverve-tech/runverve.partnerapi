from extensions import db
from datetime import datetime

class Injuries(db.Model):
    __tablename__ = 'injuries'
    
    id = db.Column(db.Integer, primary_key=True)
    tennis_elbow = db.Column(db.Boolean, default=False)
    muscle_strain = db.Column(db.Boolean, default=False)
    bicep_tendonitis = db.Column(db.Boolean, default=False)
    fracture = db.Column(db.Boolean, default=False)
    forearm_strain = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'tennis_elbow': self.tennis_elbow,
            'muscle_strain': self.muscle_strain,
            'bicep_tendonitis': self.bicep_tendonitis,
            'fracture': self.fracture,
            'forearm_strain': self.forearm_strain,
            'created_at': self.created_at
        }

class InjuryReport(db.Model):
    __tablename__ = 'injury_reports'
    __module__ = 'models.injuries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_sk = db.Column(db.Integer, db.ForeignKey('users.user_sk'), nullable=False)
    
    # Update relationship to use back_populates
    user = db.relationship('User', back_populates='injuries')
    injury_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date_reported = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # In InjuryReport
    user = db.relationship('User', backref=db.backref('injuries_rel', lazy=True, overlaps="injuries"))

    def to_dict(self):
        return {
            'id': self.id,
            'user_sk': self.user_sk,
            'injury_id': self.injury_id,
            'injury_location': self.injury_location,
            'injury_type': self.injury_type,
            'created_at': self.created_at
        }