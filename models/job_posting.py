from services.database import db

class JobPosting:
    @staticmethod
    def create_job(data):
        db.job_postings.insert_one(data)

    @staticmethod
    def get_all_jobs():
        return list(db.job_postings.find({}, {"_id": 0}))
