from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

class JobPosting:
    @staticmethod
    def create_job(data):
        db.job_postings.insert_one(data)

    @staticmethod
    def get_all_jobs():
        return list(db.job_postings.find({}, {"_id": 0}))

    @staticmethod
    def find_job_by_id(job_id):
        return db.job_postings.find_one({"_id": job_id})

    @staticmethod
    def delete_job(job_id):
        db.job_postings.delete_one({"_id": job_id})
