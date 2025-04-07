from extensions import db
from datetime import datetime

class GeocodingResult(db.Model):
    __tablename__ = 'geocoding_results'
    __module__ = 'models.geocoding'
    
    id = db.Column(db.Integer, primary_key=True)
    user_sk = db.Column(db.Integer, db.ForeignKey('users.user_sk'), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Define relationship with unique backref
    user = db.relationship('models.user.User', backref='geocoding_results_rel', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'formatted_address': self.formatted_address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'place_id': self.place_id,
            'types': self.types,
            'address_components': self.address_components,
            'plus_code': self.plus_code,
            'viewport': self.viewport,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user': {
                'username': self.user.username,
                'email': self.user.email
            } if self.user else None
        }