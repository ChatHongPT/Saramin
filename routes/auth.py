import jwt
import datetime
from flask import request, jsonify
from functools import wraps
from config import SECRET_KEY

def generate_access_token(data, expires_in=3600):
    payload = {
        "data": data,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def generate_refresh_token(data):
    payload = {"data": data}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_access_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["data"], None
    except jwt.ExpiredSignatureError:
        return None, "Token expired"
    except jwt.InvalidTokenError:
        return None, "Invalid token"

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing"}), 403
        data, error = verify_access_token(token)
        if error:
            return jsonify({"message": error}), 403
        return f(*args, **kwargs, current_user=data)
    return decorated_function
