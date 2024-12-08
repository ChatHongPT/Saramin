from flask import Blueprint, request
from services.database import db
from services.utils import success_response, error_response
from bson import ObjectId

applications_bp = Blueprint("applications", __name__)

@applications_bp.route("/", methods=["POST"])
def apply():
    """
    지원하기 API
    """
    data = request.json
    required_fields = ["user_id", "job_id"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return error_response(f"Missing fields: {', '.join(missing_fields)}")

    # 중복 지원 체크
    if db.applications.find_one({"user_id": data["user_id"], "job_id": data["job_id"]}):
        return error_response("Already applied to this job", code="DUPLICATE_APPLICATION")

    application = {
        "user_id": data["user_id"],
        "job_id": data["job_id"],
        "status": "Applied",
        "applied_at": datetime.now()
    }
    db.applications.insert_one(application)
    return success_response({"message": "Application submitted successfully"})

@applications_bp.route("/", methods=["GET"])
def list_applications():
    """
    지원 내역 조회 API
    """
    user_id = request.args.get("user_id")
    if not user_id:
        return error_response("User ID is required", code="USER_ID_REQUIRED")

    applications = list(db.applications.find({"user_id": user_id}))
    return success_response(applications)

@applications_bp.route("/<application_id>", methods=["DELETE"])
def cancel_application(application_id):
    """
    지원 취소 API
    """
    application = db.applications.find_one({"_id": ObjectId(application_id)})
    if not application:
        return error_response("Application not found", code="APPLICATION_NOT_FOUND")

    # 상태 업데이트
    db.applications.update_one(
        {"_id": ObjectId(application_id)},
        {"$set": {"status": "Cancelled"}}
    )
    return success_response({"message": "Application cancelled successfully"})
