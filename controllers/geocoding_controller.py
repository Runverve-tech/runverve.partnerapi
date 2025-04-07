from flask import current_app
from extensions import db
from models.geocoding import GeocodingResult
from flask import jsonify, request
import requests

def geocode_address(address):
    """Get geocoding information for an address using Google Maps API"""
    try:
        api_key = current_app.config['GOOGLE_API_KEY']
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
        
        response = requests.get(url)
        data = response.json()
        
        if data['status'] != 'OK':
            return {"error": f"Geocoding API error: {data['status']}"}, 400
            
        # Extract the first result
        result = data['results'][0]
        
        # Store in database
        geo_result = GeocodingResult(
            formatted_address=result['formatted_address'],
            latitude=result['geometry']['location']['lat'],
            longitude=result['geometry']['location']['lng'],
            place_id=result['place_id'],
            types=result.get('types'),
            address_components=result.get('address_components'),
            plus_code=result.get('plus_code'),
            viewport=result['geometry'].get('viewport')
        )
        
        db.session.add(geo_result)
        db.session.commit()
        
        return {
            "id": geo_result.id,
            "formatted_address": geo_result.formatted_address,
            "latitude": geo_result.latitude,
            "longitude": geo_result.longitude,
            "place_id": geo_result.place_id
        }, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def get_geocoding_result(place_id=None, lat=None, lng=None, formatted_address=None):
    """Get geocoding result by place_id, coordinates, or formatted address"""
    try:
        if place_id:
            result = GeocodingResult.query.filter_by(place_id=place_id).first()
        elif lat is not None and lng is not None:
            result = GeocodingResult.query.filter_by(latitude=lat, longitude=lng).first()
        elif formatted_address:
            result = GeocodingResult.query.filter_by(formatted_address=formatted_address).first()
        else:
            return {"error": "Please provide a place_id, latitude and longitude, or a formatted_address."}, 400

        if not result:
            return {"message": "No geocoding result found for the given input."}, 404

        return {
            "id": result.id,
            "formatted_address": result.formatted_address,
            "latitude": result.latitude,
            "longitude": result.longitude,
            "place_id": result.place_id,
            "types": result.types,
            "address_components": result.address_components,
            "plus_code": result.plus_code,
            "viewport": result.viewport
        }, 200
    except Exception as e:
        return {"error": str(e)}, 500

def delete_geocoding_result(id):
    """Delete a geocoding result by ID"""
    try:
        geocode_entry = GeocodingResult.query.get(id)
        
        if not geocode_entry:
            return {"message": "Address not found"}, 404
        
        db.session.delete(geocode_entry)
        db.session.commit()
        return {"message": f"Address with ID {id} successfully deleted"}, 200
    except Exception as e:
        db.session.rollback()
        return {"message": "Error deleting address", "error": str(e)}, 500


class GeocodingController:
    @staticmethod
    def get_location():
        # Implementation here
        pass