from extensions import db
from datetime import datetime

class SparkLedger(db.Model):
    __tablename__ = 'spark_ledger'
    __module__ = 'models.spark_points'
    
    id = db.Column(db.Integer, primary_key=True)
    user_sk = db.Column(db.Integer, db.ForeignKey('users.user_sk'), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Define relationship with unique backref
    user = db.relationship('models.user.User', backref='spark_points_rel', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_sk': self.user_sk,
            'points': self.points,
            'activity_type': self.activity_type,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }