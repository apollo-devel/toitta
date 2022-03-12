from server.database import db

import hashlib

class User:
    _collection = db['users']

    def __init__(self,
                display_name: str,
                username: str,
                password: str,
                email: str):
        self.display_name = display_name
        self.username = username
        self.hashed_password = self.encrypt(password)
        self.email = email
    
    @staticmethod
    def encrypt(password: str):
        return hashlib.sha256(password.encode()).hexdigest()

    def create(self):
        return self._collection.insert_one(vars(self))
    
