from flask import Blueprint, request, jsonify
from services.database import db
from services.auth import jwt_required
from bson import ObjectId

applications_bp = Blueprint("applications", __name__)

@applications_bp.route("/apply", methods=["POST"])
@jwt_required
def apply():
    required_fields = ["user_id", "job_posting_id"]
    data = validate_request(required_fields)
    if isinstance(data, tuple):
        return data

    db.applications.insert_one({
        "user_id": data["user_id"],
        "job_posting_id": data["job_posting_id"],
        "status": "Applied",
        "applied_date": datetime.now()
    })
    return jsonify({"message": "Application submitted successfully"})

@applications_bp.route("/cancel", methods=["DELETE"])
@jwt_required
def cancel_application():
    required_fields = ["application_id"]
    data = validate_request(required_fields)
    if isinstance(data, tuple):
        return data

    db.applications.delete_one({"_id": ObjectId(data["application_id"])})
    return jsonify({"message": "Application cancelled successfully"})
