from services.database import db

class JobPosting:
    @staticmethod
    def create(data):
        db.job_postings.insert_one(data)

    @staticmethod
    def find_all(filters, skip, limit):
        return list(db.job_postings.find(filters).skip(skip).limit(limit))

    @staticmethod
    def find_by_id(job_id):
        return db.job_postings.find_one({"_id": job_id})
