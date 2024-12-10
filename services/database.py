from pymongo import MongoClient

MONGO_URI = 'mongodb://job_portal_user:securepassword123@localhost:27017/job_portal?authSource=job_portal'
client = MongoClient(MONGO_URI)

db = client['job_portal']

# 컬렉션 참조
users_collection = db['users']
jobs_collection = db['jobs']
applications_collection = db['applications']
bookmarks_collection = db['bookmarks']
