from flask import Flask, request, jsonify, redirect, render_template, session,Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import api
from flask_migrate import Migrate
import requests

os.add_dll_directory(r'C:\Program Files\PostgreSQL\17\bin')

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load database URI directly from the environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
# Disable modification tracking overhead
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key=os.getenv('SECRET_KEY' , 'ABCD')

app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size 16MB

CLIENT_ID = '<your client id>'
CLIENT_SECRET = '<your client secret>'
REDIRECT_URI = 'http://localhost:5000/exchange_token'
GOOGLE_API_KEY = '<your api key>'

db = SQLAlchemy(app)
migrrate = Migrate(app,db)

@app.route('/')
def home():
    auth_url = api.generate_auth_url()
    print(session.get('email'))
    return redirect(auth_url)

@app.route('/exchange_token')
def exchange_token():
    code = request.args.get('code')
    if code:
        token_data = api.exchange_token(code)
        if token_data:
            access_token = token_data.get("access_token")
            user_data = api.get_user_data(access_token) 
            user_sk = user_data.get("id")  
            user = User.query.filter_by(user_sk=user_sk).first()
            if user is None:
                user = User(
                    user_sk=user_sk,
                    username=user_data.get("username"),
                    email=user_data.get("email") or "unknown@example.com"
                )
                db.session.add(user)
                db.session.commit()

            # Store `user_sk` in the session
            session['user_sk'] = user_sk

            return render_template('upload_photos.html', access_token=access_token)
        else:
            return "Error exchanging code for token", 400
    else:
        return "Error: No authorization code received", 400

# Define the User model
class User(db.Model):
    __tablename__ = 'users'
    user_sk = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Define the UserToken model


class UserToken(db.Model):
    __tablename__ = 'user_token'
    user_sk = db.Column(db.Integer, db.ForeignKey(
        'users.user_sk'), primary_key=True)
    token = db.Column(db.String(255), nullable=False)

# Define the SparkLedger model


class SparkLedger(db.Model):
    __tablename__ = 'spark_ledger'
    id = db.Column(db.Integer, primary_key=True)
    user_sk = db.Column(db.Integer, db.ForeignKey('users.user_sk'))
    credit_score = db.Column(db.Integer)
    debit_score = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.utcnow)

# Define the Activity model


class Activity(db.Model):
    __tablename__ = 'activity'
    activity_id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey('users.user_sk'))
    name = db.Column(db.String(255))
    distance = db.Column(db.Float)
    moving_time = db.Column(db.Integer)
    elapsed_time = db.Column(db.Integer)
    total_elevation_gain = db.Column(db.Float)
    type = db.Column(db.String(50))
    start_date = db.Column(db.DateTime)
    description = db.Column(db.Text)
    calories = db.Column(db.Float)


class photo2(db.Model):
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_sk = db.Column(db.Integer, db.ForeignKey('users.user_sk'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    photo_data = db.Column(db.LargeBinary, nullable=False)

class GeocodingResult(db.Model):
    __tablename__ = 'geocoding_results'

    id = db.Column(db.Integer, primary_key=True)
    formatted_address = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    place_id = db.Column(db.Text, nullable=False)
    types = db.Column(db.JSON, nullable=True)
    address_components = db.Column(db.JSON, nullable=True)
    plus_code = db.Column(db.JSON, nullable=True)
    viewport = db.Column(db.JSON, nullable=True)


class SupplementPhoto(db.Model):
    __tablename__ = 'supplement_photos'
    pic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_sk = db.Column(db.Integer, db.ForeignKey('users.user_sk'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    supplement_type = db.Column(db.String(100), nullable=False)
    photo_data = db.Column(db.LargeBinary, nullable=False)

    # def __repr__(self):
    #     return f"<SupplementPhoto {self.pic_id}>"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created", "user_sk": new_user.user_sk}), 201


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"user_sk": user.user_sk, "username": user.username, "email": user.email} for user in users])


@app.route('/user/photos', methods=['POST'])
def upload_photos():
    if 'user_sk' not in session:
        return jsonify({"message": "User not logged in"}), 401

    user_sk = session['user_sk']  
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        photo_data = file.read()
        filename = secure_filename(file.filename)
        new_photo = photo2(
            user_sk=user_sk,
            filename=filename,
            photo_data=photo_data
        )
        db.session.add(new_photo)
        db.session.commit()

        return jsonify({"message": "File successfully uploaded", "photo_id": new_photo.pid,  }), 201
    else:
        return jsonify({"message": "File type not allowed"}), 400

    
@app.route('/user/photos', methods=['GET'])
def render_photo_upload():
    """Render the photo upload page."""
    return render_template('upload_photos.html')

@app.route('/user/photos/<int:photo_id>', methods=['GET'])
def view_photo(photo_id):
    photo = photo2.query.get(photo_id)
    if not photo:
        return jsonify({"message": "Photo not found"}), 404
    
    mime_type = None
    if photo.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
        mime_type = f"image/{photo.filename.rsplit('.', 1)[1].lower()}"

    if not mime_type:
        return jsonify({"message": "Unsupported file type"}), 400

    return Response(photo.photo_data, content_type=mime_type)


@app.before_request
def create_tables():
    db.create_all()



@app.route('/geocode', methods=['POST'])
def geocode():
    
    data = request.json
    if not data or 'address' not in data:
        return jsonify({"error": "Please provide an address"}), 400

    address = data['address']
   
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_API_KEY}"

    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Failed to connect to Google API"}), response.status_code
    
    #return jsonify(response.json())
    #############################

    response_data = response.json()
    print("Google API Response:", response_data)

    if response_data['status'] != 'OK':
        return jsonify({"error": "Failed to geocode address"}), 400

    result = response_data['results'][0]

    geocoding_entry = GeocodingResult(
        formatted_address=result['formatted_address'],
        latitude=result['geometry']['location']['lat'],
        longitude=result['geometry']['location']['lng'],
        place_id=result['place_id'],
        types=result.get('types', []),
        address_components=result.get('address_components', []),
        plus_code=result.get('plus_code', {}),
        viewport=result['geometry']['viewport']
    )

    db.session.add(geocoding_entry)
    db.session.commit()

    return jsonify({
        "message": "Geocoding data stored successfully",
        "stored_data": {
            "formatted_address": geocoding_entry.formatted_address,
            "latitude": geocoding_entry.latitude,
            "longitude": geocoding_entry.longitude
        }
    }), 201
    
@app.route('/geocode', methods=['GET'])
def get_geocoding_result():
    """Retrieve geocoding data by place_id, coordinates, or formatted address."""
 
    place_id = request.args.get('place_id')
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    formatted_address = request.args.get('formatted_address')


    if place_id:
        result = GeocodingResult.query.filter_by(id=place_id).first()

    elif lat is not None and lng is not None:
        result = GeocodingResult.query.filter_by(latitude=lat, longitude=lng).first()
    elif formatted_address:
        result = GeocodingResult.query.filter_by(formatted_address=formatted_address).first()
    else:
        return jsonify({"error": "Please provide a place_id, latitude and longitude, or a formatted_address."}), 400

    if not result:
        return jsonify({"message": "No geocoding result found for the given input."}), 404

    return jsonify({
        "id": result.id,
        "formatted_address": result.formatted_address,
        "latitude": result.latitude,
        "longitude": result.longitude,
        "place_id": result.place_id,
        "types": result.types,
        "address_components": result.address_components,
        "plus_code": result.plus_code,
        "viewport": result.viewport
    }), 200

@app.route('/geocode/<int:id>', methods=['DELETE'])
def delete_address(id):
    """Delete an address by its ID."""
    geocode_entry = GeocodingResult.query.get(id)
    
    if not geocode_entry:
        return jsonify({"message": "Address not found"}), 404
    
    try:
        db.session.delete(geocode_entry)
        db.session.commit()
        return jsonify({"message": f"Address with ID {id} successfully deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error deleting address", "error": str(e)}), 500



@app.route('/user/supplements', methods=['POST'])
def upload_supplement_photo():
    """Allows users to upload photos of their supplements."""
    if 'user_sk' not in session:
        return jsonify({"message": "User not logged in"}), 401

    user_sk = session['user_sk']  # Retrieve user_sk from session

    if 'file' not in request.files or 'supplement_type' not in request.form:
        return jsonify({"message": "File and supplement type are required"}), 400

    file = request.files['file']
    supplement_type = request.form['supplement_type']

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Read the binary data and secure the filename
        photo_data = file.read()
        filename = secure_filename(file.filename)

        # Create and save the photo in the database
        new_photo = SupplementPhoto(
            user_sk=user_sk,
            filename=filename,
            supplement_type=supplement_type,
            photo_data=photo_data
        )
        db.session.add(new_photo)
        db.session.commit()

        return jsonify({"message": "File successfully uploaded", "pic_id": new_photo.pic_id}), 201
    else:
        return jsonify({"message": "File type not allowed"}), 400

@app.route('/user/supplements/<int:pic_id>', methods=['GET'])
def view_supplement_photo(pic_id):
    """Retrieve and display the uploaded supplement photo."""
    photo = SupplementPhoto.query.get(pic_id)
    if not photo:
        return jsonify({"message": "Photo not found"}), 404

    # Determine the MIME type based on file extension
    mime_type = None
    if photo.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
        mime_type = f"image/{photo.filename.rsplit('.', 1)[1].lower()}"

    if not mime_type:
        return jsonify({"message": "Unsupported file type"}), 400

    return Response(photo.photo_data, content_type=mime_type)

@app.route('/user/supplements', methods=['GET'])
def render_supplement_photo_upload():
    """Render the supplement photo upload page."""
    return render_template('upload_supplements.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)