from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from services.database import db

users_bp = Blueprint("users", __name__)

# 사용자 등록
@users_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if db.users.find_one({"email": email}):
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = generate_password_hash(password)
    user = {"email": email, "password": hashed_password, "name": name}
    db.users.insert_one(user)
    return jsonify({"message": "User registered successfully"}), 201

# 사용자 로그인
@users_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = db.users.find_one({"email": email})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful", "user": {"email": email, "name": user["name"]}})

# 사용자 조회
@users_bp.route("/", methods=["GET"])
def get_users():
    users = list(db.users.find({}, {"_id": 0, "password": 0}))
    return jsonify(users)
