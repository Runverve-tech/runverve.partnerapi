from datetime import datetime
from extensions import db

class HydrationLog(db.Model):
    __tablename__ = 'hydration_logs'  # Changed to match the table name in error
    
    id = db.Column(db.Integer, primary_key=True)
    user_sk = db.Column(db.Integer, db.ForeignKey('users.user_sk'), nullable=False)
    water_intake = db.Column(db.Integer, nullable=False)  # Changed from quantity to water_intake
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Add relationship with User
    user = db.relationship('User', backref='hydration_logs')

    def to_dict(self):
        return {
            'id': self.id,
            'user_sk': self.user_sk,
            'water_intake': self.water_intake,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }