from datetime import datetime

from bson.objectid import ObjectId

from database import db


class Like:
    _collection = db["likes"]

    def __init__(
        self, post: str, posted_at: datetime, liked_by: str, liked_at: datetime = None
    ):
        self.post = post
        self.posted_at = posted_at
        self.liked_by = liked_by
        if not liked_at:
            liked_at = datetime.now()
        self.liked_at = liked_at

    def create(self):
        data = vars(self)
        data["post"] = ObjectId(data["post"])
        data["liked_by"] = ObjectId(data["liked_by"])
        return self._collection.insert_one(data)
