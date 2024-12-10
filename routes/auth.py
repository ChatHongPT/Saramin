from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from services.database import users_collection
from services.auth import generate_access_token, generate_refresh_token, decode_access_token, decode_refresh_token

auth_bp = Blueprint('auth', __name__)

# 회원 가입
@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # 필드 검증
    if not all([username, email, password]):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    if len(password) < 6:
        return jsonify({"status": "error", "message": "Password must be at least 6 characters long"}), 400

    if '@' not in email or '.' not in email:
        return jsonify({"status": "error", "message": "Invalid email format"}), 400

    # 이메일 중복 확인
    if users_collection.find_one({"email": email}):
        return jsonify({"status": "error", "message": "Email already registered"}), 400

    # 비밀번호 암호화 및 저장
    hashed_password = generate_password_hash(password)
    users_collection.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password
    })
    return jsonify({"status": "success", "message": "User registered successfully"}), 201

# 로그인
@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # 사용자 확인
    user = users_collection.find_one({"email": email})
    if user and check_password_hash(user["password"], password):
        access_token = generate_access_token(str(user["_id"]))
        refresh_token = generate_refresh_token(str(user["_id"]))
        return jsonify({
            "status": "success",
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200

    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    refresh_token = request.json.get('refresh_token')
    if not refresh_token:
        return jsonify({"status": "error", "message": "Refresh token is missing"}), 400

    # Refresh Token 디코딩
    user_data = decode_refresh_token(refresh_token)
    if not user_data or "user_id" not in user_data:
        return jsonify({"status": "error", "message": "Invalid or expired refresh token"}), 401

    # 새 Access Token 생성
    new_access_token = generate_access_token(user_data['user_id'])
    return jsonify({"status": "success", "access_token": new_access_token}), 200

# 회원 정보 수정
@auth_bp.route('/profile', methods=['PUT'])
def update_profile():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"status": "error", "message": "Token is missing"}), 401

    user_data = decode_access_token(token)
    if not user_data:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    # 클라이언트가 수정할 수 있는 필드 제한
    allowed_fields = {"username", "password"}
    update_data = {key: value for key, value in request.json.items() if key in allowed_fields}

    # 비밀번호 암호화 처리
    if "password" in update_data:
        update_data["password"] = generate_password_hash(update_data["password"])

    users_collection.update_one({"_id": user_data["user_id"]}, {"$set": update_data})
    return jsonify({"status": "success", "message": "Profile updated successfully"}), 200
