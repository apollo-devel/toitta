from flask import jsonify, request, session

from apis import login_required
from main import app
from models.user import User


@app.route("/api/users", methods=["POST"])
def register():
    body = request.json

    error_message = User.validate(body)
    if error_message:
        return jsonify({"error": {"message": error_message}}), 400

    if User._collection.find_one({"username": body["username"]}):
        return jsonify({"error": {"message": "登録済みのユーザー名です。"}}), 400
    if User._collection.find_one({"email": body["email"]}):
        return jsonify({"error": {"message": "登録済みのメールアドレスです。"}}), 400

    user = User(
        display_name=body["display_name"],
        username=body["username"],
        password=body["password"],
        email=body["email"],
    )
    user.create()
    del body["password"]
    user = vars(user)
    body["_id"] = user["_id"] = str(user["_id"])
    session["user"] = user
    return jsonify(body)


@app.route("/api/users/<username>", methods=["GET"])
@login_required()
def get_user(username):
    user = User._collection.find_one({"username": username})
    if not user:
        return jsonify({"error": {"message": "ユーザーが存在しません。"}}), 404

    user["_id"] = str(user["_id"])
    del user["hashed_password"]
    return jsonify(user)
