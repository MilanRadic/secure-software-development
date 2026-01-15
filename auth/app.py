from flask import Flask, request, jsonify
from models import db, User
import re, uuid, jwt, datetime, hashlib, os
import requests


# ----------------------------
# Flask app initialization
# ----------------------------
app = Flask(__name__)

# ----------------------------
# Paths & configuration
# ----------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "users.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DB_PATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

SECRET_KEY = os.getenv("SECRET_KEY", "my_secret_key")

# Service URL (Docker or local)
SERVICE_URL = os.getenv("SERVICE_URL", "http://localhost:5006")

# ----------------------------
# Database initialization
# ----------------------------
db.init_app(app)

with app.app_context():
    db.create_all()

# ----------------------------
# Routes
# ----------------------------
@app.route("/register", methods=["POST"])
def register():
    # Check if the request has JSON data
    if not request.is_json:
        return jsonify({"message": "Invalid input, JSON data expected"}), 400
    
    # Retrieve the JSON payload
    data = request.get_json()
    
    # Extract fields from the payload
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    
    # Validate input
    if not username or not password or not role:
        return jsonify({"message": "Missing required fields: username, password, and role are required"}), 400
    
    # Check if username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400
    
    # Validate role
    if role not in ['Student', 'Instructor']:
        return jsonify({"message": "Invalid role. Must be 'Student' or 'Instructor'"}), 400
    
    try:
        # Generate a UUID and use it as a salt
        salt = str(uuid.uuid4())
        
        # Concatenate the salt with the password
        combined_string = salt + password
        
        # Hash the concatenated string using SHA-256
        hashed_value = hashlib.sha256(combined_string.encode()).hexdigest()
        
        # Create new user and store in database
        new_user = User(
            username=username,
            password=hashed_value,
            salt=salt,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        
        response = {
            "message": "User registered successfully"
        }
        return jsonify(response), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Registration failed: {str(e)}"}), 400


@app.route("/login", methods=["POST"])
def login():
    # Check if the request has JSON data
    if not request.is_json:
        return jsonify({"message": "Invalid input, JSON data expected"}), 400
    
    # Retrieve the JSON payload
    data = request.get_json()
    
    # Extract fields from the payload
    username = data.get('username')
    password = data.get('password')
    
    # Validate input
    if not username or not password:
        return jsonify({"message": "Missing required fields: username and password are required"}), 400
    
    try:
        # Retrieve user from database
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({"message": "Invalid credentials"}), 401
        
        # Concatenate the stored salt with the received password
        combined_string = user.salt + password
        
        # Hash the concatenated string using SHA-256
        hashed_value = hashlib.sha256(combined_string.encode()).hexdigest()
        
        # Compare with stored password hash
        if hashed_value != user.password:
            return jsonify({"message": "Invalid credentials"}), 401
        
        # Create JWT token
        expires_in_minutes = 60  # Token expires in 60 minutes
        payload = {
            "iss": "AuthServer",
            "sub": user.id,
            "scope": user.role,
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=expires_in_minutes)
        }
        
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        
        response = {
            "token": token
        }
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"message": f"Login failed: {str(e)}"}), 400


@app.route("/introspect", methods=["POST"])
def introspect():
    # Check if the request has JSON data
    if not request.is_json:
        return jsonify({"message": "Invalid input, JSON data expected"}), 400
    
    # Retrieve the JSON payload
    data = request.get_json()
    token = data.get('token')
    
    if not token:
        return jsonify({"message": "Missing token"}), 400
    
    try:
        # Decode and validate the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        # Check issuer
        if payload.get("iss") != "AuthServer":
            return jsonify({"message": "Invalid token"}), 403
        
        # Check expiration (jwt.decode already checks exp, but we verify explicitly)
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            exp_time = datetime.datetime.fromtimestamp(exp_timestamp)
            if exp_time < datetime.datetime.now():
                return jsonify({"message": "Token expired"}), 403
        
        # Retrieve scope and user id
        scope = payload.get("scope")
        user_id = payload.get("sub")
        
        if not scope or not user_id:
            return jsonify({"message": "Invalid token"}), 403
        
        response = {
            "scope": scope,
            "user_id": user_id
        }
        return jsonify(response), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 403
    except Exception as e:
        return jsonify({"message": "Invalid token"}), 403


# ----------------------------
# Debug route
# ----------------------------
@app.route("/getAllUsers", methods=["GET"])
def getAllUsers():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


# ----------------------------
# App entry point
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5005)
