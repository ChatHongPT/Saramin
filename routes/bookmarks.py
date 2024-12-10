from flask import Blueprint, jsonify, request
from services.database import bookmarks_collection, jobs_collection
from bson import ObjectId
from datetime import datetime

bookmarks_bp = Blueprint('bookmarks', __name__)

# 북마크 추가/제거 (POST /bookmarks)
@bookmarks_bp.route('/', methods=['POST'])
def toggle_bookmark():
    data = request.json
    user_id = data.get('user_id')  # 사용자 인증 확인 (토큰 기반이면 토큰에서 추출)
    job_id = data.get('job_id')  # 북마크 대상 공고 ID

    # 데이터 유효성 검증
    if not user_id or not job_id:
        return jsonify({"status": "error", "message": "Missing user_id or job_id"}), 400

    # 북마크 존재 여부 확인
    bookmark = bookmarks_collection.find_one({"user_id": user_id, "job_id": job_id})

    if bookmark:
        # 북마크가 이미 존재하면 제거 (토글 처리)
        bookmarks_collection.delete_one({"_id": bookmark["_id"]})
        return jsonify({"status": "success", "message": "Bookmark removed"}), 200
    else:
        # 북마크가 없으면 추가
        bookmarks_collection.insert_one({
            "user_id": user_id,
            "job_id": job_id,
            "created_at": datetime.now()  # 북마크 생성 시간 기록
        })
        return jsonify({"status": "success", "message": "Bookmark added"}), 201


# 북마크 목록 조회 (GET /bookmarks)
@bookmarks_bp.route('/', methods=['GET'])
def get_bookmarks():
    user_id = request.args.get('user_id')  # 사용자 인증 확인 (토큰 기반이면 토큰에서 추출)
    page = int(request.args.get('page', 1))  # 페이지네이션 기본값 처리
    per_page = 20  # 페이지당 항목 수
    skip = (page - 1) * per_page

    # 필터 및 정렬
    query = {"user_id": user_id}
    if "location" in request.args:
        query["location"] = {"$regex": request.args["location"], "$options": "i"}
    if "experience" in request.args:
        query["experience"] = request.args["experience"]
    if "salary" in request.args:
        query["salary"] = {"$gte": int(request.args["salary"])}  # 최소 급여
    if "tech_stack" in request.args:
        query["tech_stack"] = {"$regex": request.args["tech_stack"], "$options": "i"}

    # 정렬
    sort_field = request.args.get('sort', 'created_at')  # 기본 정렬 필드: 북마크 추가 시간
    sort_order = int(request.args.get('order', -1))  # 기본 정렬 순서: 내림차순

    # 북마크 데이터 가져오기
    bookmarks = list(bookmarks_collection.find(query).skip(skip).limit(per_page).sort(sort_field, sort_order))
    total_count = bookmarks_collection.count_documents(query)

    # 공고 상세 정보를 함께 반환
    for bookmark in bookmarks:
        job = jobs_collection.find_one({"_id": ObjectId(bookmark["job_id"])})
        if job:
            job["_id"] = str(job["_id"])
            bookmark["job"] = job
        bookmark["_id"] = str(bookmark["_id"])  # ObjectId를 문자열로 변환

    return jsonify({
        "status": "success",
        "data": bookmarks,
        "pagination": {
            "currentPage": page,
            "totalPages": (total_count + per_page - 1) // per_page,
            "totalItems": total_count
        }
    }), 200


# 공고 상세 조회 (GET /jobs/:id)
@bookmarks_bp.route('/jobs/<job_id>', methods=['GET'])
def get_job_detail(job_id):
    try:
        job = jobs_collection.find_one({"_id": ObjectId(job_id)})
        if not job:
            return jsonify({"status": "error", "message": "Job not found"}), 404

        # 조회수 증가 처리
        jobs_collection.update_one({"_id": ObjectId(job_id)}, {"$inc": {"views": 1}})

        # 관련 공고 추천 (동일한 기술스택 또는 지역을 기준으로 추천)
        related_jobs = list(jobs_collection.find({
            "tech_stack": {"$in": job.get("tech_stack", [])},
            "location": job.get("location")
        }).limit(5))  # 최대 5개 관련 공고 추천
        for related in related_jobs:
            related["_id"] = str(related["_id"])

        # 상세 정보 반환
        job["_id"] = str(job["_id"])
        return jsonify({
            "status": "success",
            "data": job,
            "related_jobs": related_jobs
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
