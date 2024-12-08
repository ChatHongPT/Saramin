from flask import Blueprint, request
from services.database import db
from services.utils import success_response, error_response
from bson import ObjectId

bookmarks_bp = Blueprint("bookmarks", __name__)

@bookmarks_bp.route("/", methods=["POST"])
def toggle_bookmark():
    """
    북마크 추가/제거 API
    ---
    tags:
      - Bookmarks
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - user_id
            - job_id
          properties:
            user_id:
              type: string
              example: "60c72b2f4f1a256a3b123456"
            job_id:
              type: string
              example: "60c72b2f4f1a256a3b654321"
    responses:
      200:
        description: 북마크 추가/제거 결과
    """
    data = request.json
    required_fields = ["user_id", "job_id"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return error_response(f"Missing fields: {', '.join(missing_fields)}", code="MISSING_FIELDS")

    bookmark = db.bookmarks.find_one({"user_id": data["user_id"], "job_id": data["job_id"]})
    if bookmark:
        # 북마크 제거
        db.bookmarks.delete_one({"_id": bookmark["_id"]})
        return success_response({"message": "Bookmark removed"})
    else:
        # 북마크 추가
        db.bookmarks.insert_one(data)
        return success_response({"message": "Bookmark added"})

@bookmarks_bp.route("/", methods=["GET"])
def list_bookmarks():
    """
    북마크 목록 조회 API
    ---
    tags:
      - Bookmarks
    parameters:
      - name: user_id
        in: query
        required: true
        type: string
        description: 사용자 ID
    responses:
      200:
        description: 북마크 목록
    """
    user_id = request.args.get("user_id")
    if not user_id:
        return error_response("User ID is required", code="USER_ID_REQUIRED")

    page = int(request.args.get("page", 1))
    per_page = 10
    skip = (page - 1) * per_page

    bookmarks = list(db.bookmarks.find({"user_id": user_id}).skip(skip).limit(per_page))
    total_count = db.bookmarks.count_documents({"user_id": user_id})

    return success_response(bookmarks, pagination={
        "currentPage": page,
        "totalPages": (total_count + per_page - 1) // per_page,
        "totalItems": total_count
    })
