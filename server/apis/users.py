import pymongo
from bson.objectid import ObjectId
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
    if "following" not in user:
        user["following"] = []
    user["following"] = [str(_id) for _id in user["following"]]
    if "followers" not in user:
        user["followers"] = []
    user["followers"] = [str(_id) for _id in user["followers"]]
    return jsonify(user)


@app.route("/api/users/<username>/follow", methods=["POST"])
@login_required()
def follow_user(username):
    user = User._collection.find_one({"username": username})
    if not user:
        return jsonify({"error": {"message": "ユーザーが存在しません。"}}), 404
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
    del me["hashed_password"]
    me["_id"] = str(me["_id"])
    if "following" not in me:
        me["following"] = []
    me["following"] = [str(_id) for _id in me["following"]]
    if "followers" not in me:
        me["followers"] = []
    me["followers"] = [str(_id) for _id in me["followers"]]
    session["user"] = me
    return jsonify(me)


@app.route("/api/users/<username>/follow", methods=["DELETE"])
@login_required()
def unfollow_user(username):
    user = User._collection.find_one({"username": username})
    if not user:
        return jsonify({"error": {"message": "ユーザーが存在しません。"}}), 404
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
    del me["hashed_password"]
    me["_id"] = str(me["_id"])
    if "following" not in me:
        me["following"] = []
    me["following"] = [str(_id) for _id in me["following"]]
    if "followers" not in me:
        me["followers"] = []
    me["followers"] = [str(_id) for _id in me["followers"]]
    session["user"] = me
    return jsonify(me)
