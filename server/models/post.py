from datetime import datetime

import pymongo
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

    @staticmethod
    def _liking_and_retweeting(logged_in_user_id):
        return [
            {
                "$lookup": {
                    "from": "likes",
                    "let": {"post_id": "$_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {"$eq": ["$post", "$$post_id"]},
                                        {"$eq": ["$liked_by", logged_in_user_id]},
                                    ]
                                }
                            }
                        },
                        {"$project": {"_id": True}},
                    ],
                    "as": "liking",
                }
            },
            {"$set": {"liking": {"$toBool": {"$size": "$liking"}}}},
            {
                "$lookup": {
                    "from": "retweets",
                    "let": {"post_id": "$_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {"$eq": ["$post", "$$post_id"]},
                                        {"$eq": ["$retweeted_by", logged_in_user_id]},
                                    ]
                                }
                            }
                        },
                        {"$project": {"_id": True}},
                    ],
                    "as": "retweeting",
                }
            },
            {"$set": {"retweeting": {"$toBool": {"$size": "$retweeting"}}}},
        ]

    @classmethod
    def _load_posts(cls, condition, user_logged_in, sort):
        logged_in_user_id = user_logged_in["_id"]

        pipelines = [
            condition,
            # 投稿者
            {
                "$lookup": {
                    "from": "users",
                    "localField": "posted_by",
                    "foreignField": "_id",
                    "as": "posted_by",
                }
            },
            {"$unwind": {"path": "$posted_by"}},
            # リツイート
            {
                "$lookup": {
                    "from": "posts",
                    "localField": "retweeted_post",
                    "foreignField": "_id",
                    "as": "retweeted_post",
                    "pipeline": [
                        {
                            "$lookup": {
                                "from": "users",
                                "localField": "posted_by",
                                "foreignField": "_id",
                                "as": "posted_by",
                            }
                        },
                        {
                            "$unwind": {
                                "path": "$posted_by",
                                "preserveNullAndEmptyArrays": True,
                            }
                        },
                        *cls._liking_and_retweeting(logged_in_user_id),
                    ],
                }
            },
            {
                "$unwind": {
                    "path": "$retweeted_post",
                    "preserveNullAndEmptyArrays": True,
                }
            },
            # 返信
            {
                "$lookup": {
                    "from": "posts",
                    "localField": "reply_to",
                    "foreignField": "_id",
                    "as": "reply_to",
                    "pipeline": [
                        {
                            "$lookup": {
                                "from": "users",
                                "localField": "posted_by",
                                "foreignField": "_id",
                                "as": "posted_by",
                            }
                        },
                        {
                            "$unwind": {
                                "path": "$posted_by",
                                "preserveNullAndEmptyArrays": True,
                            }
                        },
                        # 表示に利用しないので返信には liking, retweeting は不要
                    ],
                }
            },
            {"$unwind": {"path": "$reply_to", "preserveNullAndEmptyArrays": True}},
            *cls._liking_and_retweeting(logged_in_user_id),
        ]

        if sort:
            pipelines.append(sort)

        return cls._collection.aggregate(pipelines)

    @classmethod
    def list_posts(cls, user_logged_in):
        ids = [i for i in user_logged_in["following"]]
        ids.append(user_logged_in["_id"])
        condition = {"$match": {"posted_by": {"$in": ids}}}
        sort = {"$sort": {"created_at": pymongo.DESCENDING}}
        return cls._load_posts(condition, user_logged_in, sort)

    @classmethod
    def search_posts(cls, query, user_logged_in):
        condition = {"$match": {"content": {"$regex": query, "$options": "i"}}}
        sort = {"$sort": {"created_at": pymongo.DESCENDING}}
        return cls._load_posts(condition, user_logged_in, sort)

    @classmethod
    def list_profile_posts(cls, user, user_logged_in):
        condition = {"$match": {"posted_by": user["_id"], "reply_to": None}}
        sort = {"$sort": {"created_at": pymongo.DESCENDING}}
        return cls._load_posts(condition, user_logged_in, sort)

    @classmethod
    def list_profile_posts_and_replies(cls, user, user_logged_in):
        condition = {"$match": {"posted_by": user["_id"]}}
        sort = {"$sort": {"created_at": pymongo.DESCENDING}}
        return cls._load_posts(condition, user_logged_in, sort)
