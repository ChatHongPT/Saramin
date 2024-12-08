from flask import Blueprint, request, jsonify
from services.database import db
from services.auth import jwt_required

jobs_bp = Blueprint("jobs", __name__)

@jobs_bp.route("/", methods=["GET"])
def get_jobs():
    jobs = list(db.job_postings.find({}, {"_id": 0}))
    return jsonify(jobs)

@jobs_bp.route("/search", methods=["GET"])
def search_jobs():
    query = request.args.get("query")
    jobs = list(db.job_postings.find({"title": {"$regex": query, "$options": "i"}}, {"_id": 0}))
    return jsonify(jobs)
