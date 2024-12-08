from flask import Blueprint, request, jsonify
from services.auth import generate_access_token, jwt_required
from models.user import User
from services.utils import validate_request

users_bp = Blueprint("users", __name__)

@users_bp.route("/register", methods=["POST"])
def register():
    required_fields = ["email", "password", "name"]
    data = validate_request(required_fields)
    if isinstance(data, tuple):
        return data

    if User.find_by_email(data["email"]):
        return jsonify({"message": "Email already exists"}), 400

    User.create(data)
    return jsonify({"message": "User registered successfully"}), 201

@users_bp.route("/login", methods=["POST"])
def login():
    required_fields = ["email", "password"]
    data = validate_request(required_fields)
    if isinstance(data, tuple):
        return data

    user = User.find_by_email(data["email"])
    if not user:
        return jsonify({"message": "User not found"}), 404

    if data["password"] != user["password"]:
        return jsonify({"message": "Invalid password"}), 401

    token = generate_access_token({"email": data["email"]})
    return jsonify({"token": token})
