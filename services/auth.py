import jwt
import datetime
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 비밀 키 설정
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "default_refresh_secret_key")

# Access Token 생성
def generate_access_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 유효 기간: 1시간
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Refresh Token 생성
def generate_refresh_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)  # 유효 기간: 7일
    }
    return jwt.encode(payload, REFRESH_SECRET_KEY, algorithm="HS256")

# Access Token 검증
def decode_access_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

# Refresh Token 검증
# Refresh Token 검증
def decode_refresh_token(token):
    try:
        decoded = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=["HS256"])
        print("Decoded refresh token:", decoded)  # 디버깅용 로그
        return decoded
    except jwt.ExpiredSignatureError:
        print("Refresh token expired")  # 디버깅 로그
        return None
    except jwt.InvalidTokenError as e:
        print("Invalid refresh token:", str(e))  # 디버깅 로그
        return None
