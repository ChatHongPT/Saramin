class User:
    @staticmethod
    def create_user(data):
        db.users.insert_one(data)

    @staticmethod
    def find_user_by_email(email):
        return db.users.find_one({"email": email})

    @staticmethod
    def get_all_users():
        return list(db.users.find({}, {"_id": 0, "password": 0}))

    @staticmethod
    def delete_user_by_email(email):
        db.users.delete_one({"email": email})
