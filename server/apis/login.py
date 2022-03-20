from flask import jsonify, request, session

from apis import error, login_required
from main import app
from models.user import User


@app.route("/api/login", methods=["POST"])
def login():
    body = request.json
    if "identifier" not in body or not body["identifier"]:
        return error("ユーザー名 または メールアドレスは必須です。")
    if "password" not in body or not body["password"]:
        return error("パスワードは必須です。")

    identifier = body["identifier"]
    user = User._collection.find_one(
        {"$or": [{"email": identifier}, {"username": identifier}]}
    )

    if not user:
        return error("ユーザーが存在しません。")

    hashed_password = User.encrypt(body["password"])
    if user["hashed_password"] != hashed_password:
        return error("パスワードが一致しません。")
    User.set_session_user(user)
    return jsonify(user)


@app.route("/api/logout", methods=["POST"])
def logout():
    del session["user"]
    return "", 204


@app.route("/api/session", methods=["GET"])
@login_required()
def get_session():
    return jsonify(session["user"])
