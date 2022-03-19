from flask import jsonify, request, session

from apis import login_required
from main import app
from models.user import User


@app.route("/api/login", methods=["POST"])
def login():
    body = request.json
    if "identifier" not in body or not body["identifier"]:
        return jsonify({"error": {"message": "ユーザー名 または メールアドレスは必須です。"}}), 400
    if "password" not in body or not body["password"]:
        return jsonify({"error": {"message": "パスワードは必須です。"}}), 400

    identifier = body["identifier"]
    user = User._collection.find_one(
        {"$or": [{"email": identifier}, {"username": identifier}]}
    )

    if not user:
        return jsonify({"error": {"message": "ユーザーが存在しません。"}}), 400

    hashed_password = User.encrypt(body["password"])
    if user["hashed_password"] != hashed_password:
        return jsonify({"error": {"message": "パスワードが一致しません。"}}), 400

    del user["hashed_password"]

    user["_id"] = str(user["_id"])
    if "following" not in user:
        user["following"] = []
    user["following"] = [str(_id) for _id in user["following"]]
    if "followers" not in user:
        user["followers"] = []
    user["followers"] = [str(_id) for _id in user["followers"]]
    session["user"] = user
    return jsonify(user)


@app.route("/api/logout", methods=["POST"])
def logout():
    del session["user"]
    return "", 204


@app.route("/api/session", methods=["GET"])
@login_required()
def get_session():
    return jsonify(session["user"])
