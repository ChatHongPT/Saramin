from flask import Blueprint, request, jsonify
from services.auth import generate_jwt, jwt_required
from models.user import User

users_bp = Blueprint("users", __name__)

@users_bp.route("/register", methods=["POST"])
def register():
    required_fields = ["email", "password", "name"]
    data = validate_request(required_fields)
    if isinstance(data, tuple):  # Error from validate_request
        return data

    if User.find_user_by_email(data["email"]):
        return jsonify({"message": "Email already exists"}), 400

    User.create_user(data)
    return jsonify({"message": "User registered successfully"}), 201

@users_bp.route("/login", methods=["POST"])
def login():
    required_fields = ["email", "password"]
    data = validate_request(required_fields)
    if isinstance(data, tuple):
        return data

    user = User.find_user_by_email(data["email"])
    if not user:
        return jsonify({"message": "User not found"}), 404

    # 비밀번호 검증 및 JWT 발급
    if data["password"] != user["password"]:
        return jsonify({"message": "Invalid password"}), 401

    token = generate_jwt({"email": data["email"]})
    return jsonify({"token": token})
