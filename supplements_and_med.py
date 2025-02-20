from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

app.secret_key = os.getenv('SERVER_SECRET_KEY')

# Load database URI directly from the environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
# Disable modification tracking overhead
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)


class Supplements(db.Model):
    __tablename__ = 'supplements'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
class SupplementsMain(db.Model):
    __tablename__ = "supplements_main"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_sk = db.Column(db.Integer, db.ForeignKey('users.user_sk'), nullable=False)
    name = db.Column(db.String(100))
    dosage = db.Column(db.Double)
    frequency = db.Column(db.Integer)
    purpose = db.Column(db.JSON)


@app.before_request
def create_tables():
    db.create_all()

@app.route("/user/supplements", methods=["GET"])
def get_supplements():
    
    data = SupplementsMain.query.all()
    
    if data != [] and not data:
        return jsonify({"error": "Fetching failed."}), 400

    response = []
    
    for record in data:
        part = dict()
        part['id'] = record.id
        part['name'] =  record.name
        part['dosage'] = record.dosage
        part['frequency'] = record.frequency
        part['purpose'] = record.purpose
        part['user_sk'] = record.user_sk
        
        response.append(part)
        
    return jsonify(response), 200

@app.route("/user/supplements/<athlete_id>", methods=["GET"])
def get_supplements_by_athlete(athlete_id):
    data = SupplementsMain.query.filter_by(user_sk=athlete_id)
    if not data:
        return jsonify({"error": "Supplements not found"}), 404
    
    response = []
    
    for record in data:
        part = dict()
        part['id'] = record.id
        part['name'] =  record.name
        part['dosage'] = record.dosage
        part['frequency'] = record.frequency
        part['purpose'] = record.purpose
        
        response.append(part)
        
    return jsonify(response), 200
    

@app.route("/user/supplements/<athlete_id>", methods=["POST"])
def post_supplement(athlete_id):
    '''
    Required JSON
    
    {
        "name": <Supplement name> (String),
        "dosage": (Double),
        "frequency": (Integer),
        "purpose": (JSON)
    }
    '''
    
    data = request.json
    
    if not data:
        return jsonify({"error": "Invalid input JSON"}), 400
    
    requirements = ["name", "dosage", "frequency", "purpose"]
    
    for requirement in requirements:
        if requirement not in data:
            return jsonify({"error": "Invalid input JSON"}), 400
    
    record = SupplementsMain(name=data["name"], dosage=data["dosage"], frequency=data["frequency"], purpose=data["purpose"], user_sk=athlete_id)
    
    db.session.add(record)
    db.session.commit()
    
    return jsonify({"message": "Supplement added successfully."}), 200

@app.route("/user/supplements/<id>", methods=["PUT"])
def update_supplement(id):
    '''
    Input JSON contains one or more of the following fields
    
    - name
    - dosage
    - frequency
    - purpose
    
    '''
    
    data = request.json
    
    if not data:
        return jsonify({"error": "Invalid input JSON"}), 400
    
    requirements = ["name", "dosage", "frequency", "purpose"]
    
    for field in data:
        
        if field not in requirements:
            return jsonify({"error": "Invalid input JSON"}), 400
        db.session.query(SupplementsMain).filter_by(id=id).update({field: data[field]})
        
    db.session.commit()
    
    return jsonify({"message": "Update successful"}), 200

@app.route("/user/supplements/<id>", methods=["DELETE"])
def delete_supplement(id):
    
    record = SupplementsMain.query.filter_by(id=id).first()
    
    if not record:
        return jsonify({"error": "Invalid supplement ID"}), 200
    
    db.session.delete(record)
    db.session.commit()
    
    return jsonify({"message": "Deletion successful"}), 200


# Supplement end


if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 8000))  # Railway provides a PORT env variable
    app.run(host="0.0.0.0", port=PORT)