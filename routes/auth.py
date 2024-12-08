from flask import Blueprint, request
from services.auth import generate_access_token, generate_refresh_token
from services.utils import success_response, error_response
from services.database import db
import base64

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if db.users.find_one({"email": email}):
        return error_response("Email already exists", code="EMAIL_EXISTS")

    encoded_password = base64.b64encode(password.encode()).decode()
    db.users.insert_one({"email": email, "password": encoded_password, "name": name})
    return success_response({"message": "User registered successfully"})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = db.users.find_one({"email": email})
    if not user:
        return error_response("User not found", code="USER_NOT_FOUND")

    if base64.b64decode(user["password"]).decode() != password:
        return error_response("Invalid credentials", code="INVALID_CREDENTIALS")

    access_token = generate_access_token({"email": email})
    refresh_token = generate_refresh_token({"email": email})
    return success_response({"access_token": access_token, "refresh_token": refresh_token})
