from services.database import db

class User:
    @staticmethod
    def create_user(data):
        db.users.insert_one(data)

    @staticmethod
    def find_user_by_email(email):
        return db.users.find_one({"email": email})
