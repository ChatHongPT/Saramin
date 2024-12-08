import base64
from flask import Blueprint, request, jsonify
from services.database import db
from services.auth import generate_jwt, jwt_required

users_bp = Blueprint("users", __name__)

@users_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if db.users.find_one({"email": email}):
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = base64.b64encode(password.encode()).decode()
    db.users.insert_one({"email": email, "password": hashed_password, "name": name})
    return jsonify({"message": "User registered successfully"}), 201

@users_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = db.users.find_one({"email": email})
    if not user:
        return jsonify({"message": "User not found"}), 404

    hashed_password = base64.b64encode(password.encode()).decode()
    if hashed_password != user["password"]:
        return jsonify({"message": "Invalid credentials"}), 401

    token = generate_jwt({"email": email})
    return jsonify({"token": token, "user": {"email": email, "name": user["name"]}})
