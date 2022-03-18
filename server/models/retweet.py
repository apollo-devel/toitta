from datetime import datetime

from bson.objectid import ObjectId

from database import db


class Retweet:
    _collection = db["retweets"]

    def __init__(
        self,
        post: str,
        posted_at: datetime,
        retweeted_by: str,
        retweeted_at: datetime = None,
    ):
        self.post = post
        self.posted_at = posted_at
        self.retweeted_by = retweeted_by
        if not retweeted_at:
            retweeted_at = datetime.now()
        self.retweeted_at = retweeted_at

    def create(self):
        data = vars(self)
        data["post"] = ObjectId(data["post"])
        data["retweeted_by"] = ObjectId(data["retweeted_by"])
        return self._collection.insert_one(data)
