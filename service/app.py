import os
import requests
from requests.exceptions import HTTPError
from flask import Flask, request, jsonify
from models import db, User, Course, Enrollment

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

DB_PATH = os.path.join(DATA_DIR, "tables.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DB_PATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Auth service URL (local or Docker)
AUTH_URL = os.getenv("AUTH_URL", "http://localhost:5005")

# ----------------------------
# Database initialization
# ----------------------------
db.init_app(app)

with app.app_context():
    db.create_all()

# ----------------------------
# Helper functions
# ----------------------------
def validate_token(token):
    """Validate token by calling auth server's /introspect endpoint"""
    try:
        response = requests.post(
            f"{AUTH_URL}/introspect",
            json={"token": token},
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None


def get_token_from_header():
    """Extract token from Authorization header"""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0] != "Bearer":
        return None
    return parts[1]


# ----------------------------
# Develops your routes here
# ----------------------------
@app.route("/user", methods=["POST"])
def create_user():
    # Check if the request has JSON data
    if not request.is_json:
        return jsonify({"message": "Invalid input, JSON data expected"}), 400
    
    # Retrieve the JSON payload
    data = request.get_json()
    
    # Extract fields from the payload
    user_id = data.get('id')
    name = data.get('name')
    role = data.get('role')
    email = data.get('email')
    notes = data.get('notes')
    
    # Validate input
    if not user_id or not name or not role or not email:
        return jsonify({"message": "Missing required fields: id, name, role, and email are required"}), 400
    
    # Validate role
    if role not in ['Student', 'Instructor']:
        return jsonify({"message": "Invalid role. Must be 'Student' or 'Instructor'"}), 400
    
    try:
        # Check if user already exists
        existing_user = User.query.filter_by(id=user_id).first()
        if existing_user:
            return jsonify({"message": "User already exists"}), 400
        
        # Create new user and store in database
        new_user = User(
            id=user_id,
            name=name,
            role=role,
            email=email,
            notes=notes if notes else None
        )
        db.session.add(new_user)
        db.session.commit()
        
        response = {
            "message": "User created successfully"
        }
        return jsonify(response), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"User creation failed: {str(e)}"}), 400


@app.route("/courses", methods=["GET"])
def get_courses():
    # Extract token from Authorization header
    token = get_token_from_header()
    if not token:
        return jsonify({"message": "Missing or invalid Authorization header"}), 403
    
    # Validate token
    token_info = validate_token(token)
    if not token_info:
        return jsonify({"message": "Invalid token"}), 403
    
    # Both Student and Instructor roles can view courses
    scope = token_info.get("scope")
    if scope not in ['Student', 'Instructor']:
        return jsonify({"message": "Invalid role"}), 403
    
    try:
        # Retrieve all courses from database
        courses = Course.query.all()
        courses_list = [course.to_dict() for course in courses]
        
        return jsonify(courses_list), 200
        
    except Exception as e:
        return jsonify({"message": f"Failed to retrieve courses: {str(e)}"}), 400


@app.route("/course", methods=["POST"])
def create_course():
    # Extract token from Authorization header
    token = get_token_from_header()
    if not token:
        return jsonify({"message": "Missing or invalid Authorization header"}), 403
    
    # Validate token
    token_info = validate_token(token)
    if not token_info:
        return jsonify({"message": "Invalid token"}), 403
    
    # Check if user is Instructor
    scope = token_info.get("scope")
    if scope != "Instructor":
        return jsonify({"message": "Only Instructors can create courses"}), 403
    
    # Check if the request has JSON data
    if not request.is_json:
        return jsonify({"message": "Invalid input, JSON data expected"}), 400
    
    # Retrieve the JSON payload
    data = request.get_json()
    
    # Extract fields from the payload
    title = data.get('title')
    description = data.get('description')
    
    # Validate input
    if not title or not description:
        return jsonify({"message": "Missing required fields: title and description are required"}), 400
    
    try:
        # Get instructor ID from token
        instructor_id = token_info.get("user_id")
        
        # Create new course and store in database
        new_course = Course(
            title=title,
            description=description,
            instructor_id=instructor_id
        )
        db.session.add(new_course)
        db.session.commit()
        
        response = new_course.to_dict()
        return jsonify(response), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Course creation failed: {str(e)}"}), 400


@app.route("/enroll", methods=["POST"])
def enroll():
    # Extract token from Authorization header
    token = get_token_from_header()
    if not token:
        return jsonify({"message": "Missing or invalid Authorization header"}), 403
    
    # Validate token
    token_info = validate_token(token)
    if not token_info:
        return jsonify({"message": "Invalid token"}), 403
    
    # Check if user is Student
    scope = token_info.get("scope")
    if scope != "Student":
        return jsonify({"message": "Only Students can enroll in courses"}), 403
    
    # Check if the request has JSON data
    if not request.is_json:
        return jsonify({"message": "Invalid input, JSON data expected"}), 400
    
    # Retrieve the JSON payload
    data = request.get_json()
    
    # Extract fields from the payload
    course_title = data.get('course_title')
    
    # Validate input
    if not course_title:
        return jsonify({"message": "Missing required field: course_title is required"}), 400
    
    try:
        # Get student ID from token
        student_id = token_info.get("user_id")
        
        # Check if course exists
        course = Course.query.filter_by(title=course_title).first()
        if not course:
            return jsonify({"message": "Course not found"}), 400
        
        # Check if student is already enrolled
        existing_enrollment = Enrollment.query.filter_by(
            user_id=student_id,
            course_id=course.id
        ).first()
        if existing_enrollment:
            return jsonify({"message": "Already enrolled in this course"}), 400
        
        # Create new enrollment
        new_enrollment = Enrollment(
            user_id=student_id,
            course_id=course.id
        )
        db.session.add(new_enrollment)
        db.session.commit()
        
        response = course.to_dict()
        return jsonify(response), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Enrollment failed: {str(e)}"}), 400


# ----------------------------
# Debug routes
# ----------------------------
@app.route("/enrollments", methods=["GET"])
def get_enrollments():
    enrollments = Enrollment.query.all()
    res = []

    for e in enrollments:
        user = User.query.filter_by(id=e.user_id).first()
        course = Course.query.filter_by(id=e.course_id).first()
        res.append({
            "user": user.name if user else None,
            "course": course.title if course else None
        })

    return jsonify(res), 200


@app.route("/getAllUsers", methods=["GET"])
def getAllUsers():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200


# ----------------------------
# App entry point
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5006)
