from ..connections import Database
from auth.hasher import Hasher
from datetime import datetime

class Users:
    def __init__(self, keep_alive=False):
        self.database = Database()
        db = self.database.create_client()
        self.users = db['users']
        self.keep_alive = keep_alive

    def get_user_by_email(self, email):
        user = self.users.find_one({'email': email})
        if self.keep_alive is False:
            self.database.close_client()
        return user
    
    def update_password(self, email, password):
        hashed_password = Hasher([password]).generate()[0]
        self.users.update_one({"email": email}, {"$set": {"password": hashed_password}})
        self.database.close_client()

    def create_user(self, email, name, password, postal_code):
        user = {
            'email': email,
            'name': name,
            'password': Hasher([password]).generate()[0],
            'verified': False,  # Add a verified field, initially False
            'postal_code': postal_code,
            'created': datetime.now()
        }
        self.users.insert_one(user)
        self.database.close_client()

    def update_by_key(self, key, value, email):
        self.users.update_one({"email": email}, {"$set": {key: value}})
        self.database.close_client()
    
    def disconnect(self):
        self.database.close_client()