from flask import Blueprint, jsonify, request
from services.database import applications_collection
from bson import ObjectId
from datetime import datetime

applications_bp = Blueprint('applications', __name__)

# 지원하기
@applications_bp.route('/', methods=['POST'])
def apply_job():
    data = request.json
    user_id = data.get('user_id')
    job_id = data.get('job_id')

    # 중복 지원 확인
    if applications_collection.find_one({"user_id": user_id, "job_id": job_id}):
        return jsonify({"status": "error", "message": "Already applied"}), 400

    applications_collection.insert_one({
        "user_id": user_id,
        "job_id": job_id,
        "application_date": datetime.now(),
        "status": "pending"
    })
    return jsonify({"status": "success", "message": "Application submitted successfully"}), 201

# 지원 내역 조회
@applications_bp.route('/', methods=['GET'])
def get_applications():
    user_id = request.args.get('user_id')
    applications = list(applications_collection.find({"user_id": user_id}))

    for app in applications:
        app['_id'] = str(app['_id'])

    return jsonify({"status": "success", "data": applications})
