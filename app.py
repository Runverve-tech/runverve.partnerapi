from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User_Spark(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    spark_points = db.Column(db.Integer, nullable=False, default=0)

with app.app_context():
    db.create_all()

@app.route('/user/spark-points', methods=['GET'])
def get_spark_points():
    user_id = request.headers.get('User-ID')

    if not user_id:
        return jsonify({"error": "User-ID header is required"}), 400

    user = User_Spark.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user_id": user.id, "spark_points": user.spark_points})

@app.route('/user/spark-points', methods=['POST'])
def post_spark_points():
    user_id = request.headers.get('User-ID')

    if not user_id:
        return jsonify({"error": "User-ID header is required"}), 400

    user = User_Spark.query.get(user_id)
    data = request.json
    if not data or "spark_points" not in data:
        return jsonify({"error": "Missing 'spark_points' in request body"}), 400

    try:
        spark_points = int(data["spark_points"])
        if spark_points < 0:
            raise ValueError("Spark Points must be a non-negative integer")
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid 'spark_points' value"}), 400

    if not user:
        user = User_Spark(id=user_id, spark_points=spark_points)
        db.session.add(user)
    else:
        user.spark_points = spark_points

    db.session.commit()
    return jsonify({"message": "Spark Points updated", "user_id": user.id, "spark_points": user.spark_points})

if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG') == 'True')
