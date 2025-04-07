from flask import Blueprint, request, jsonify
from models.supplements import UserSupplement, Supplement
from extensions import db
from middleware.auth import token_required

bp = Blueprint('supplements', __name__)

@bp.route('/supplements', methods=['GET', 'POST'])
@token_required
def handle_supplements(current_user):
    if request.method == 'GET':
        supplements = Supplement.query.all()
        return jsonify([supp.to_dict() for supp in supplements])
    
    data = request.get_json()
    
    # Check if supplement with same name already exists
    existing_supplement = Supplement.query.filter_by(name=data['name']).first()
    if existing_supplement:
        return jsonify({'error': f"Supplement '{data['name']}' already exists"}), 409
    
    supplement = Supplement(
        name=data['name'],
        description=data.get('description', '')
    )
    db.session.add(supplement)
    db.session.commit()
    return jsonify(supplement.to_dict()), 201

@bp.route('/user/supplements', methods=['GET', 'POST'])
@token_required
def handle_user_supplements(current_user):
    if request.method == 'GET':
        user_supplements = UserSupplement.query.filter_by(user_sk=current_user.user_sk).all()
        return jsonify([{
            'id': supp.id,
            'user_sk': supp.user_sk,
            'supplement_id': supp.supplement_id,
            'dosage': supp.dosage,
            'frequency': supp.frequency,
            'created_at': supp.created_at.isoformat() if supp.created_at else None
        } for supp in user_supplements])

    data = request.get_json()
    
    # Check if supplement exists
    supplement_exists = Supplement.query.get(data['supplement_id'])
    if not supplement_exists:
        return jsonify({'error': f"Supplement with ID {data['supplement_id']} does not exist"}), 404

    supplement = UserSupplement(
        user_sk=current_user.user_sk,
        supplement_id=data['supplement_id'],
        dosage=data['dose'],
        frequency=data['frequency']
    )
    db.session.add(supplement)
    db.session.commit()
    
    return jsonify({
        'id': supplement.id,
        'user_sk': supplement.user_sk,
        'supplement_id': supplement.supplement_id,
        'dosage': supplement.dosage,
        'frequency': supplement.frequency,
        'created_at': supplement.created_at.isoformat() if supplement.created_at else None
    }), 201

def init_app(app):
    app.register_blueprint(bp)