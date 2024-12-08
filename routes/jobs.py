from flask import Blueprint, request, jsonify
from services.crawler import crawl_saramin
from services.database import save_jobs_to_db, get_all_jobs

jobs_bp = Blueprint("jobs", __name__)

@jobs_bp.route("/crawl/<keyword>/<int:pages>", methods=["POST"])
def crawl_jobs(keyword, pages):
    jobs = crawl_saramin(keyword, pages)
    save_jobs_to_db(jobs)
    return jsonify({"message": f"{len(jobs)} jobs crawled and saved."})

@jobs_bp.route("/", methods=["GET"])
def get_jobs():
    jobs = get_all_jobs()
    return jsonify(jobs)
