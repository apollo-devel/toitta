from datetime import datetime
from typing import List

from bson.objectid import ObjectId

from database import db


class Message:
    _collection = db["messages"]

    def __init__(
        self,
        content: str,
        chat: str,
        sender: str,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        self.content = content
        self.chat = chat
        self.sender = sender
        self.read_by = []
        if not created_at:
            created_at = datetime.now()
        self.created_at = created_at
        if not updated_at:
            updated_at = datetime.now()
        self.updated_at = updated_at

    def create(self):
        data = vars(self)
        data["chat"] = ObjectId(data["chat"])
        data["sender"] = ObjectId(data["sender"])
        return self._collection.insert_one(data)

    @classmethod
    def validate(cls, body, logged_in_user_id):
        if not body.get("sender"):
            return "投稿者は必須です。"
        if body["sender"] != logged_in_user_id:
            return "この操作は許可されていません。"
        if not body.get("content", "").strip():
            return "本文が指定されていません。"
        return
