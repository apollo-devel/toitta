from datetime import datetime
from typing import List

from bson.objectid import ObjectId

from database import db


class Chat:
    _collection = db["chats"]

    def __init__(
        self,
        name: str,
        is_group_chat: bool,
        users: List,
        latest_message: str = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        self.name = name
        self.is_group_chat = is_group_chat
        self.users = users
        self.latest_message = latest_message
        if not created_at:
            created_at = datetime.now()
        self.created_at = created_at
        if not updated_at:
            updated_at = datetime.now()
        self.updated_at = updated_at

    def create(self):
        data = vars(self)
        data["users"] = [ObjectId(u) for u in data["users"]]
        return self._collection.insert_one(data)

    @classmethod
    def validate(cls, body, logged_in_user_id):
        if "users" not in body or not body["users"]:
            return "ユーザーは必須です"

        if logged_in_user_id not in body["users"]:
            return "自身を含まないチャットは作成できません"

        return None
