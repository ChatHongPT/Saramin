from flask import Blueprint, jsonify, request
from services.database import jobs_collection
from bson import ObjectId  # ObjectId 임포트 추가

jobs_bp = Blueprint('jobs', __name__)

# 공고 목록 조회
@jobs_bp.route('/', methods=['GET'])
@jobs_bp.route('/list', methods=['GET'])  # '/list' 경로 추가
def list_jobs():
    try:
        # 페이지네이션 기본값 처리
        page = int(request.args.get('page', 1))
        per_page = 20
        skip = (page - 1) * per_page

        # 필터링 및 검색
        query = {}
        if "keyword" in request.args:
             query["title"] = {"$regex": request.args["keyword"].strip(), "$options": "i"}
        if "location" in request.args:
            query["location"] = {"$regex": f"^{request.args['location']}$", "$options": "i"}

        # 디버깅: 생성된 쿼리 확인
        print(f"Generated query: {query}")



        # 정렬
        sort_field = request.args.get('sort', 'date_crawled')  # 기본 정렬 필드
        sort_order = int(request.args.get('order', -1))       # 기본 정렬 순서: 내림차순

        # MongoDB 조회
        print(f"Generated query: {query}")  # 디버깅용 로그
        jobs = list(jobs_collection.find(query).skip(skip).limit(per_page).sort(sort_field, sort_order))
        total_count = jobs_collection.count_documents(query)

        # ObjectId를 문자열로 변환
        for job in jobs:
            job['_id'] = str(job['_id'])

        return jsonify({
            "status": "success",
            "data": jobs,
            "pagination": {
                "currentPage": page,
                "totalPages": (total_count + per_page - 1) // per_page,
                "totalItems": total_count
            }
        }), 200
    except Exception as e:
        # 에러 처리
        print(f"Error occurred: {e}")  # 디버깅용
        return jsonify({"status": "error", "message": str(e)}), 400

# 공고 상세 조회
@jobs_bp.route('/<job_id>', methods=['GET'])
def get_job_detail(job_id):
    try:
        print(f"Received request for job ID: {job_id}")
        job = jobs_collection.find_one({"_id": ObjectId(job_id)})
        if not job:
            print("Job not found in the database.")
            return jsonify({"status": "error", "message": "Job not found"}), 404
        job['_id'] = str(job['_id'])
        return jsonify({"status": "success", "data": job}), 200
    except Exception as e:
        # `ObjectId` 변환 실패 및 기타 예외 처리
        print(f"Invalid Job ID or Error: {e}")  # 디버깅용
        return jsonify({"status": "error", "message": f"Invalid Job ID: {e}"}), 400
