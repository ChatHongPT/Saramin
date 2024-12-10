from flask import Blueprint, jsonify, request
from services.database import bookmarks_collection
from bson import ObjectId
from datetime import datetime

bookmarks_bp = Blueprint('bookmarks', __name__)

# 북마크 추가/제거
@bookmarks_bp.route('/', methods=['POST'])
def toggle_bookmark():
    data = request.json
    user_id = data.get('user_id')
    job_id = data.get('job_id')

    bookmark = bookmarks_collection.find_one({"user_id": user_id, "job_id": job_id})
    if bookmark:
        bookmarks_collection.delete_one({"_id": bookmark["_id"]})
        return jsonify({"status": "success", "message": "Bookmark removed"}), 200

    bookmarks_collection.insert_one({
        "user_id": user_id,
        "job_id": job_id,
        "created_at": datetime.now()
    })
    return jsonify({"status": "success", "message": "Bookmark added"}), 201
