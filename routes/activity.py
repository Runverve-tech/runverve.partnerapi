from flask import Blueprint, request, jsonify
from models.activity import Activity
from extensions import db
from middleware.auth import token_required

bp = Blueprint('activity', __name__)

@bp.route('/activities', methods=['GET', 'POST'])
@token_required
def handle_activities(current_user):
    if request.method == 'GET':
        activities = Activity.query.filter_by(athlete_id=current_user.user_sk).all()
        return jsonify([activity.to_dict() for activity in activities])

    data = request.get_json()
    activity = Activity(
        athlete_id=current_user.user_sk,
        name=data.get('name'),
        distance=data.get('distance'),
        moving_time=data.get('moving_time'),
        elapsed_time=data.get('elapsed_time'),
        total_elevation_gain=data.get('total_elevation_gain'),
        type=data.get('type'),
        description=data.get('description'),
        calories=data.get('calories')
    )
    db.session.add(activity)
    db.session.commit()
    return jsonify(activity.to_dict()), 201

@bp.route('/activities/<int:activity_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def handle_activity(current_user, activity_id):
    activity = Activity.query.filter_by(
        activity_id=activity_id, 
        athlete_id=current_user.user_sk
    ).first()
    
    if not activity:
        return jsonify({'error': 'Activity not found'}), 404

    if request.method == 'GET':
        return jsonify(activity.to_dict())

    elif request.method == 'PUT':
        data = request.get_json()
        for key, value in data.items():
            if hasattr(activity, key):
                setattr(activity, key, value)
        db.session.commit()
        return jsonify(activity.to_dict())

    elif request.method == 'DELETE':
        db.session.delete(activity)
        db.session.commit()
        return '', 204

@bp.route('/activities/update', methods=['PUT'])
@token_required
def update_activities(current_user):
    try:
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({'error': 'Expected an array of activities'}), 400

        updated_activities = []
        errors = []

        for item in data:
            activity_id = item.get('activity_id')
            if not activity_id:
                errors.append({'error': 'activity_id is required', 'data': item})
                continue

            activity = Activity.query.filter_by(
                activity_id=activity_id,
                athlete_id=current_user.user_sk
            ).first()

            if not activity:
                errors.append({'error': f'Activity {activity_id} not found', 'data': item})
                continue

            # Define allowed fields
            allowed_fields = {
                'name', 'distance', 'moving_time', 'elapsed_time',
                'total_elevation_gain', 'type', 'description', 'calories'
            }

            # Update fields
            for key, value in item.items():
                if key in allowed_fields and hasattr(activity, key):
                    setattr(activity, key, value)
            
            updated_activities.append(activity)

        if updated_activities:
            db.session.commit()

        response = {
            'updated': [activity.to_dict() for activity in updated_activities],
            'total_updated': len(updated_activities)
        }
        
        if errors:
            response['errors'] = errors

        return jsonify(response), 200 if updated_activities else 400

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to update activities',
            'details': str(e)
        }), 500

def init_app(app):
    app.register_blueprint(bp)