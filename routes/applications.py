from flask import Blueprint, jsonify, request
from services.database import applications_collection
from bson import ObjectId
from datetime import datetime

# Blueprint 정의
applications_bp = Blueprint('applications', __name__)

# 지원하기 (POST)
@applications_bp.route('/', methods=['POST'])
def apply_job():
    # 클라이언트 요청 데이터 파싱
    data = request.json
    user_id = data.get('user_id')  # 요청에서 사용자 ID 가져오기
    job_id = data.get('job_id')    # 요청에서 공고 ID 가져오기

    # 중요 포인트 1: 요청 데이터 검증
    if not user_id or not job_id:
        return jsonify({"status": "error", "message": "user_id and job_id are required"}), 400

    # 중요 포인트 2: 중복 지원 체크
    if applications_collection.find_one({"user_id": user_id, "job_id": job_id}):
        return jsonify({"status": "error", "message": "Already applied"}), 400

    # 중요 포인트 3: 지원 데이터 저장
    applications_collection.insert_one({
        "user_id": user_id,                      # 사용자 ID
        "job_id": job_id,                        # 공고 ID
        "application_date": datetime.utcnow(),   # 지원 날짜 (UTC 기준)
        "status": "pending"                      # 초기 지원 상태
    })

    # 응답 반환
    return jsonify({"status": "success", "message": "Application submitted successfully"}), 201


# 지원 내역 조회 (GET)
@applications_bp.route('/', methods=['GET'])
def get_applications():
    # 클라이언트 요청에서 user_id 가져오기
    user_id = request.args.get('user_id')

    # 중요 포인트 4: 요청 데이터 검증
    if not user_id:
        return jsonify({"status": "error", "message": "user_id is required"}), 400

    # 중요 포인트 5: 사용자별 지원 내역 조회
    applications = list(applications_collection.find({"user_id": user_id}))

    # MongoDB ObjectId를 문자열로 변환 (JSON 직렬화 가능하도록)
    for app in applications:
        app['_id'] = str(app['_id'])

    # 지원 내역 반환
    return jsonify({"status": "success", "data": applications})

@applications_bp.route('/<application_id>', methods=['DELETE'])
def delete_application(application_id):
    try:
        # ObjectId 변환 시도
        application_id = ObjectId(application_id)
        application = applications_collection.find_one({"_id": application_id})
        if not application:
            return jsonify({"status": "error", "message": "Application not found"}), 404
        
        # 상태 확인 (예: 이미 취소된 지원은 취소 불가)
        if application["status"] == "canceled":
            return jsonify({"status": "error", "message": "Application is already canceled"}), 400
        
        # 지원 삭제 또는 상태 업데이트
        applications_collection.update_one({"_id": application_id}, {"$set": {"status": "canceled"}})
        return jsonify({"status": "success", "message": "Application canceled successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Invalid Application ID: {e}"}), 400
