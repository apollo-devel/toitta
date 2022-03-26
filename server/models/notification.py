from datetime import datetime

from bson.objectid import ObjectId

from database import db


class Notification:
    _collection = db["notifications"]

    def __init__(
        self,
        user_from: str,
        user_to: str,
        notification_type: str,
        params: object,
        opened: bool = False,
        created_at: datetime = None,
    ):
        self.user_from = user_from
        self.user_to = user_to
        self.notification_type = notification_type
        self.params = params
        self.opened = opened
        if not created_at:
            created_at = datetime.now()
        self.created_at = created_at

    def create(self):
        data = vars(self)
        data["user_from"] = ObjectId(data["user_from"])
        data["user_to"] = ObjectId(data["user_to"])

        if self.notification_type in ["like", "retweet", "reply"]:
            self.params["post_id"] = ObjectId(self.params["post_id"])
        return self._collection.insert_one(data)

    @classmethod
    def like(cls, user_from, user_to, post_id):
        return cls(user_from, user_to, "like", {"post_id": post_id})

    @classmethod
    def retweet(cls, user_from, user_to, post_id):
        return cls(user_from, user_to, "retweet", {"post_id": post_id})

    @classmethod
    def reply(cls, user_from, user_to, post_id):
        return cls(user_from, user_to, "reply", {"post_id": post_id})

    @classmethod
    def follow(cls, user_from, user_to):
        return cls(user_from, user_to, "follow", {})
