from models.hydration import HydrationLog
from extensions import db
from datetime import datetime
from flask import request, current_app
import jwt

def log_hydration(data):
    try:
        hydration_log = HydrationLog(
            user_sk=data['user_sk'],
            water_intake=data['quantity'],  # Changed to water_intake
            timestamp=datetime.utcnow()
        )
        
        db.session.add(hydration_log)
        db.session.commit()
        
        return {
            "message": "Hydration log added successfully",
            "data": hydration_log.to_dict()
        }, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400