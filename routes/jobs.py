from flask import Blueprint, request
from services.database import db
from services.utils import success_response, error_response

jobs_bp = Blueprint("jobs", __name__)

@jobs_bp.route("/", methods=["GET"])
def list_jobs():
    """
    채용 공고 목록 조회 API
    ---
    responses:
      200:
        description: 채용 공고 목록
    """
    page = int(request.args.get("page", 1))
    per_page = 20
    skip = (page - 1) * per_page

    query = {}
    if "location" in request.args:
        query["location"] = request.args.get("location")
    if "experience" in request.args:
        query["experience"] = request.args.get("experience")
    if "company" in request.args:
        query["company"] = {"$regex": request.args.get("company"), "$options": "i"}

    jobs = list(db.job_postings.find(query).skip(skip).limit(per_page))
    total_count = db.job_postings.count_documents(query)

    return success_response(jobs, pagination={
        "currentPage": page,
        "totalPages": (total_count + per_page - 1) // per_page,
        "totalItems": total_count
    })

@jobs_bp.route("/<job_id>", methods=["GET"])
def job_detail(job_id):
    """
    채용 공고 상세 조회 API
    """
    job = db.job_postings.find_one({"_id": job_id})
    if not job:
        return error_response("Job not found", code="JOB_NOT_FOUND")
    return success_response(job)

@jobs_bp.route("/", methods=["POST"])
def create_job():
    """
    채용 공고 등록 API
    """
    data = request.json
    required_fields = ["title", "company", "location", "deadline"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return error_response(f"Missing fields: {', '.join(missing_fields)}")

    db.job_postings.insert_one(data)
    return success_response({"message": "Job created successfully"})
