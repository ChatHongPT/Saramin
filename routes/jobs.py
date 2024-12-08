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

@jobs_bp.route("/filter", methods=["GET"])
def filter_jobs():
    location = request.args.get("location")
    employment_type = request.args.get("employment_type")

    query = {}
    if location:
        query["location"] = location
    if employment_type:
        query["employment_type"] = employment_type

    jobs = list(db.job_postings.find(query, {"_id": 0}))
    return jsonify(jobs)

@jobs_bp.route("/paginate", methods=["GET"])
def paginate_jobs():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    jobs = list(db.job_postings.find().skip((page - 1) * per_page).limit(per_page))
    return jsonify(jobs)

@jobs_bp.route("/sort", methods=["GET"])
def sort_jobs():
    sort_by = request.args.get("sort_by", "posted_date")
    order = int(request.args.get("order", 1))
    jobs = list(db.job_postings.find().sort(sort_by, order))
    return jsonify(jobs)
