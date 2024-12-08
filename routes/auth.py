from flask import Blueprint, request, jsonify
from services.auth import generate_access_token, generate_refresh_token, verify_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # 사용자 인증 로직 (예시 데이터 사용)
    user = {"email": "user@example.com", "password": "password123"}
    if email != user["email"] or password != user["password"]:
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = generate_access_token({"email": email})
    refresh_token = generate_refresh_token({"email": email})
    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200

@auth_bp.route("/token/refresh", methods=["POST"])
def refresh_token():
    refresh_token = request.headers.get("Authorization")
    if not refresh_token:
        return jsonify({"message": "Refresh token is missing"}), 403

    data, error = verify_access_token(refresh_token)
    if error:
        return jsonify({"message": error}), 403

    new_access_token = generate_access_token(data)
    return jsonify({"access_token": new_access_token}), 200
