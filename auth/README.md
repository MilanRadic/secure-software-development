# Authorization Server

This is the authorization server implementation for the Secure Software Development course.

## Endpoints

### POST /register
Register a new user.

**Request Body:**
```json
{
  "username": "student1",
  "password": "password123",
  "role": "Student"
}
```

**Response (200 OK):**
```json
{
  "message": "User registered successfully"
}
```

**Response (400 Bad Request):**
```json
{
  "message": "Missing required fields: username, password, and role are required"
}
```

### POST /login
Login and receive a JWT token.

**Request Body:**
```json
{
  "username": "student1",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (401 Unauthorized):**
```json
{
  "message": "Invalid credentials"
}
```

### POST /introspect
Validate a JWT token and retrieve user information.

**Request Body:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200 OK):**
```json
{
  "scope": "Student",
  "user_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

**Response (403 Forbidden):**
```json
{
  "message": "Invalid token"
}
```

## Setup and Running

1. **Navigate to the auth directory:**
   ```bash
   cd auth
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

   The server will run on `http://127.0.0.1:5005`

## Testing with Postman

1. Open Postman
2. Create a new HTTP request
3. Set method to POST
4. Set URL to `http://localhost:5005/register` (or `/login`, `/introspect`)
5. In Body tab, select "raw" and "JSON"
6. Enter the JSON payload
7. Click Send

## Security Features

- Passwords are hashed using SHA-256 with random salt (UUID)
- JWT tokens include issuer, subject (user ID), scope (role), and expiration
- Input validation on all endpoints
- SQL injection prevention using SQLAlchemy ORM
- Token expiration checking

## Database

The database is stored in `auth/data/users.db` (SQLite).

A debug endpoint `/getAllUsers` (GET) is available to view all registered users.
