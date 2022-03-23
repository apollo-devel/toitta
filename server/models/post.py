from datetime import datetime

from bson.objectid import ObjectId

from database import db


class Post:
    _collection = db["posts"]

    MAX_CONTENT_LENGTH = 140

    def __init__(
        self,
        content: str,
        posted_by: str,
        retweeted_post: str = None,
        reply_to: str = None,
        reply_count: int = 0,
        like_count: int = 0,
        retweet_count: int = 0,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        self.content = content
        self.posted_by = posted_by
        self.retweeted_post = retweeted_post
        self.reply_to = reply_to
        self.reply_count = reply_count
        self.like_count = like_count
        self.retweet_count = retweet_count
        if not created_at:
            created_at = datetime.now()
        self.created_at = created_at
        if not updated_at:
            updated_at = datetime.now()
        self.updated_at = updated_at

    def create(self):
        data = vars(self)
        data["posted_by"] = ObjectId(data["posted_by"])
        if "retweeted_post" in data and data["retweeted_post"]:
            data["retweeted_post"] = ObjectId(data["retweeted_post"])
        if "reply_to" in data and data["reply_to"]:
            data["reply_to"] = ObjectId(data["reply_to"])
        return self._collection.insert_one(data)

    @classmethod
    def validate(cls, body):
        if "content" not in body or not body["content"]:
            return "本文は必須です。"
        content = body["content"]
        if len(content) > cls.MAX_CONTENT_LENGTH:
            return f"本文は{cls.MAX_CONTENT_LENGTH}文字以下で入力してください。"

        if "posted_by" not in body or not body["posted_by"]:
            return "投稿者は必須です。"

        return None
