from flask import Blueprint, request, jsonify
from services.database import db
from services.auth import generate_jwt
from models.user import User

users_bp = Blueprint("users", __name__)

@users_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if User.find_user_by_email(email):
        return jsonify({"message": "Email already exists"}), 400

    User.create_user({"email": email, "password": password, "name": name})
    return jsonify({"message": "User registered successfully"}), 201
