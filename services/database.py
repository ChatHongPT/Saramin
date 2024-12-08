from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def save_jobs_to_db(jobs):
    """
    크롤링한 채용 공고를 MongoDB에 저장하는 함수.

    Args:
        jobs (list): 크롤링된 채용 공고 리스트
    """
    for job in jobs:
        if not collection.find_one({"link": job["link"]}):  # 중복 방지
            collection.insert_one(job)

def get_all_jobs():
    """
    MongoDB에서 모든 채용 공고를 가져오는 함수.

    Returns:
        list: 모든 채용 공고 리스트
    """
    return list(collection.find({}, {"_id": 0}))
