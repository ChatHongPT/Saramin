from flask import request, jsonify
from services.auth import decode_access_token

def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"status": "error", "message": "Token is missing"}), 401
        user_data = decode_access_token(token)
        if not user_data:
            return jsonify({"status": "error", "message": "Invalid or expired token"}), 401
        return f(user_data, *args, **kwargs)
    return wrapper
