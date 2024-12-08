from flask import Blueprint, request, jsonify
from services.database import db
from bson import ObjectId
from services.auth import jwt_required

jobs_bp = Blueprint("jobs", __name__)

@jobs_bp.route("/", methods=["GET"])
def get_jobs():
    jobs = list(db.job_postings.find({}, {"_id": 0}))
    return jsonify(jobs)

@jobs_bp.route("/", methods=["POST"])
@jwt_required
def create_job():
    data = request.json
    db.job_postings.insert_one(data)
    return jsonify({"message": "Job created successfully"}), 201
