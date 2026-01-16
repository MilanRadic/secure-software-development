# Service Server

This is the service server implementation for the Secure Software Development course.

## Endpoints

### POST /user
Create a user in the service database. This endpoint is called internally by the auth server during registration.

**Request Body:**
```json
{
  "id": "user-uuid",
  "name": "John Doe",
  "role": "Student",
  "email": "john@example.com",
  "notes": "Optional notes"
}
```

**Response (200 OK):**
```json
{
  "message": "User created successfully"
}
```

### GET /courses
Retrieve all courses. Requires authentication (both Student and Instructor roles).

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
[
  {
    "id": "course-uuid",
    "title": "SSD",
    "description": "Secure software development"
  }
]
```

### POST /course
Create a new course. Requires authentication (Instructor role only).

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "SSD",
  "description": "Secure software development"
}
```

**Response (200 OK):**
```json
{
  "id": "course-uuid",
  "title": "SSD",
  "description": "Secure software development"
}
```

### POST /enroll
Enroll in a course. Requires authentication (Student role only).

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "course_title": "SSD"
}
```

**Response (200 OK):**
```json
{
  "id": "course-uuid",
  "title": "SSD",
  "description": "Secure software development"
}
```

## Setup and Running

1. **Navigate to the service directory:**
   ```bash
   cd service
   ```

2. **Create and activate virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the server:**
   ```powershell
   python app.py
   ```

   The server will run on `http://127.0.0.1:5006`

## Important Notes

- The auth server must be running on port 5005 for token validation to work
- All endpoints (except /user) require a valid JWT token in the Authorization header
- Token validation is done by calling the auth server's /introspect endpoint
- The service uses a separate database from the auth server

## Testing with Postman

1. First, register and login to get a token (using auth server endpoints)
2. Use the token in the Authorization header with Bearer scheme
3. Test the service endpoints with the token

Example Authorization header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Debug Endpoints

- `GET /getAllUsers` - View all users in service database
- `GET /enrollments` - View all course enrollments
