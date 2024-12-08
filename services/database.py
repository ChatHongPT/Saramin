from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

def save_to_mongodb(data):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    for job in data:
        if not collection.find_one({"링크": job["링크"]}):  # 중복 방지
            collection.insert_one(job)
    print(f"{len(data)} jobs saved to MongoDB.")
