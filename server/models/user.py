import hashlib
import re

from flask import session

from database import db


class User:
    _collection = db["users"]

    MIN_USERNAME_LENGTH = 1
    MAX_USERNAME_LENGTH = 15
    USERNAME_PATTERN = "^[a-zA-Z0-9_]+$"
    MIN_DISPLAY_NAME_LENGTH = 4
    MAX_DISPLAY_NAME_LENGTH = 50
    MIN_PASSWORD_LENGTH = 6
    MAX_PASSWORD_LENGTH = 100
    EMAIL_PATTERN = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    def __init__(self, display_name: str, username: str, password: str, email: str):
        self.display_name = display_name
        self.username = username
        self.hashed_password = self.encrypt(password)
        self.email = email
        self.following = []
        self.followers = []

    @staticmethod
    def encrypt(password: str):
        return hashlib.sha256(password.encode()).hexdigest()

    def create(self):
        return self._collection.insert_one(vars(self))

    @classmethod
    def validate(cls, body):
        if "username" not in body or not body["username"]:
            return "ユーザー名は必須です。"
        username = body["username"]
        if not re.match(cls.USERNAME_PATTERN, username):
            return "ユーザー名には英数字(a~z A~z 0~9)とアンダースコア(_)以外利用できません。"
        if len(username) < cls.MIN_USERNAME_LENGTH:
            return f"ユーザー名は{cls.MIN_USERNAME_LENGTH}文字以上で指定してください。"
        if len(username) > cls.MAX_USERNAME_LENGTH:
            return f"ユーザー名は{cls.MAX_USERNAME_LENGTH}文字以下で指定してください。"

        if "display_name" not in body or not body["display_name"]:
            return "表示名は必須です。"
        display_name = body["display_name"]
        if len(display_name) < cls.MIN_DISPLAY_NAME_LENGTH:
            return f"表示名は{cls.MIN_DISPLAY_NAME_LENGTH}文字以上で指定してください。"
        if len(display_name) > cls.MAX_DISPLAY_NAME_LENGTH:
            return f"表示名は{cls.MAX_DISPLAY_NAME_LENGTH}文字以下で指定してください。"

        if "password" not in body or not body["password"]:
            return "パスワードは必須です。"
        password = body["password"]
        if len(password) < cls.MIN_PASSWORD_LENGTH:
            return f"パスワードは{cls.MIN_PASSWORD_LENGTH}文字以上で指定してください。"
        if len(password) > cls.MAX_PASSWORD_LENGTH:
            return f"パスワードは{cls.MAX_PASSWORD_LENGTH}文字以下で指定してください。"

        if "email" not in body or not body["email"]:
            return "メールアドレスは必須です。"
        email = body["email"]
        if not re.match(cls.EMAIL_PATTERN, email):
            return "メールアドレスが正しくありません。"

        return None

    @staticmethod
    def set_session_user(user):
        del user["hashed_password"]
        user["_id"] = str(user["_id"])
        if "following" not in user:
            user["following"] = []
        user["following"] = [str(_id) for _id in user["following"]]
        if "followers" not in user:
            user["followers"] = []
        user["followers"] = [str(_id) for _id in user["followers"]]
        session["user"] = user
