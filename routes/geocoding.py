from flask import Blueprint, request, jsonify
from controllers import geocoding_controller
from middleware.auth_middleware import login_required

bp = Blueprint('geocoding', __name__)

@bp.route('/geocode', methods=['POST'])
def geocode():
    data = request.json
    if not data or not data.get('address'):
        return jsonify({"error": "Address is required."}), 400
    
    result, status_code = geocoding_controller.geocode_address(data.get('address'))
    return jsonify(result), status_code

@bp.route('/geocode', methods=['GET'])
def get_geocoding_result():
    """Retrieve geocoding data by place_id, coordinates, or formatted address."""
    place_id = request.args.get('place_id')
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    formatted_address = request.args.get('formatted_address')
    
    result, status_code = geocoding_controller.get_geocoding_result(place_id, lat, lng, formatted_address)
    return jsonify(result), status_code

@bp.route('/geocode/<int:id>', methods=['DELETE'])
@login_required
def delete_address(id):
    """Delete an address by its ID."""
    result, status_code = geocoding_controller.delete_geocoding_result(id)
    return jsonify(result), status_code