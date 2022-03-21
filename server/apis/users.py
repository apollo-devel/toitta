import pymongo
from bson.objectid import ObjectId
from flask import jsonify, request, session

from apis import error, login_required
from main import app
from models.user import User


@app.route("/api/users", methods=["POST"])
def register():
    body = request.json

    error_message = User.validate(body)
    if error_message:
        return error(error_message)

    if User._collection.find_one({"username": body["username"]}):
        return error("登録済みのユーザー名です。")
    if User._collection.find_one({"email": body["email"]}):
        return error("登録済みのメールアドレスです。")

    user = User(
        display_name=body["display_name"],
        username=body["username"],
        password=body["password"],
        email=body["email"],
    )
    user.create()
    user = vars(user)
    User.set_session_user(user)
    return jsonify(user)


@app.route("/api/users/<username>", methods=["GET"])
@login_required()
def get_user(username):
    user = User._collection.find_one({"username": username})
    if not user:
        return error("ユーザーが存在しません。")

    del user["hashed_password"]
    return jsonify(user)


@app.route("/api/users/<username>/follow", methods=["POST"])
@login_required()
def follow_user(username):
    user = User._collection.find_one({"username": username})
    if not user:
        return error("ユーザーが存在しません。", 404)
    own_id = session["user"]["_id"]
    user_id = user["_id"]
    User._collection.find_one_and_update(
        {"username": username},
        {"$addToSet": {"followers": ObjectId(own_id)}},
        return_document=pymongo.ReturnDocument.AFTER,
    )
    me = User._collection.find_one_and_update(
        {"_id": ObjectId(own_id)},
        {"$addToSet": {"following": ObjectId(user_id)}},
        return_document=pymongo.ReturnDocument.AFTER,
    )
    User.set_session_user(me)
    return jsonify(me)


@app.route("/api/users/<username>/follow", methods=["DELETE"])
@login_required()
def unfollow_user(username):
    user = User._collection.find_one({"username": username})
    if not user:
        return error("ユーザーが存在しません。", 404)
    own_id = session["user"]["_id"]
    user_id = user["_id"]
    User._collection.find_one_and_update(
        {"username": username},
        {"$pull": {"followers": ObjectId(own_id)}},
        return_document=pymongo.ReturnDocument.AFTER,
    )
    me = User._collection.find_one_and_update(
        {"_id": ObjectId(own_id)},
        {"$pull": {"following": ObjectId(user_id)}},
        return_document=pymongo.ReturnDocument.AFTER,
    )
    User.set_session_user(me)
    return jsonify(me)


@app.route("/api/users/<username>/following", methods=["GET"])
@login_required()
def list_following_users(username):
    user = User._collection.find_one({"username": username})
    if not user:
        return error("ユーザーが存在しません。", 404)
    result = []
    for user_id in user.get("following", []):
        u = User._collection.find_one({"_id": ObjectId(user_id)})
        if u:
            del u["hashed_password"]
            result.append(u)
    return jsonify(result)


@app.route("/api/users/<username>/followers", methods=["GET"])
@login_required()
def list_followers(username):
    user = User._collection.find_one({"username": username})
    if not user:
        return error("ユーザーが存在しません。", 404)
    result = []
    for user_id in user.get("followers", []):
        u = User._collection.find_one({"_id": ObjectId(user_id)})
        if u:
            del u["hashed_password"]
            result.append(u)
    return jsonify(result)
