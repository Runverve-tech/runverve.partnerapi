from flask import Blueprint, request, jsonify
from models.spark_points import SparkLedger  # Fixed import path
from extensions import db
from middleware.auth import token_required
from datetime import datetime

bp = Blueprint('spark_points', __name__, url_prefix='/user')  # Add url_prefix

@bp.route('/spark-points', methods=['GET', 'POST'])
@token_required
def handle_spark_points(current_user):
    if request.method == 'GET':
        # Get total points from all records
        total_points = db.session.query(db.func.sum(SparkLedger.points)).filter_by(
            user_sk=current_user.user_sk
        ).scalar() or 0
        
        # Get latest record for timestamp
        latest_record = SparkLedger.query.filter_by(
            user_sk=current_user.user_sk
        ).order_by(SparkLedger.timestamp.desc()).first()
        
        return jsonify({
            'total_spark_points': total_points,
            'last_updated': latest_record.timestamp.isoformat() if latest_record else None,
            'user_sk': current_user.user_sk
        })
    
    elif request.method == 'POST':
        data = request.get_json()
        new_spark = SparkLedger(
            user_sk=current_user.user_sk,
            points=data.get('points', 0),
            activity_type=data.get('activity_type', 'general'),
            timestamp=datetime.utcnow()
        )
        db.session.add(new_spark)
        db.session.commit()
        return jsonify(new_spark.to_dict()), 201

@bp.route('/spark-points/history', methods=['GET'])
@token_required
def get_spark_points_history(current_user):
    spark_history = SparkLedger.query.filter_by(user_sk=current_user.user_sk)\
        .order_by(SparkLedger.timestamp.desc()).all()
    return jsonify([entry.to_dict() for entry in spark_history])

def init_app(app):
    app.register_blueprint(bp)