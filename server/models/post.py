from bson.objectid import ObjectId
from database import db

from datetime import datetime


class Post:
    _collection = db['posts']

    MAX_CONTENT_LENGTH = 140

    def __init__(self,
                content: str,
                posted_by: str,
                like_count: int = 0,
                created_at: datetime = None,
                updated_at: datetime = None):
        self.content = content
        self.posted_by = posted_by
        self.like_count = like_count
        if not created_at:
            created_at = datetime.now()
        self.created_at = created_at
        if not updated_at:
            updated_at = datetime.now()
        self.updated_at = updated_at

    def create(self):
        data = vars(self)
        data['posted_by'] = ObjectId(data['posted_by'])
        return self._collection.insert_one(data)
    
    @classmethod
    def validate(cls, body):
        if 'content' not in body or not body['content']:
            return '本文は必須です。'
        content = body['content']
        if len(content) > cls.MAX_CONTENT_LENGTH:
            return f'本文は{cls.MAX_CONTENT_LENGTH}文字以下で入力してください。'
        
        if 'posted_by' not in body or not body['posted_by']:
            return '投稿者は必須です。'
        
        return None

