from datetime import datetime, date
from extensions import db

class Activity(db.Model):
    __tablename__ = 'activities'
    __module__ = 'models.activity'
    
    activity_id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey('users.user_sk'), nullable=False)
    name = db.Column(db.String(255))
    distance = db.Column(db.Float, default=0.0)
    moving_time = db.Column(db.Integer, default=0)
    elapsed_time = db.Column(db.Integer, default=0)
    total_elevation_gain = db.Column(db.Float, default=0.0)
    type = db.Column(db.String(50))
    start_date = db.Column(db.DateTime, default=date.today)
    description = db.Column(db.Text)
    calories = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Update relationship with unique backref
    user = db.relationship('models.user.User', backref='activities_rel', lazy=True)

    def to_dict(self):
        return {
            'activity_id': self.activity_id,
            'athlete_id': self.athlete_id,
            'name': self.name,
            'distance': self.distance,
            'moving_time': self.moving_time,
            'elapsed_time': self.elapsed_time,
            'total_elevation_gain': self.total_elevation_gain,
            'type': self.type,
            'start_date': self.start_date,
            'description': self.description,
            'calories': self.calories,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }