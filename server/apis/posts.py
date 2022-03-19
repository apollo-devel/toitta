import pymongo
from bson.objectid import ObjectId
from flask import jsonify, request, session

from apis import login_required
from main import app
from models.like import Like
from models.post import Post
from models.retweet import Retweet
from models.user import User


@app.route("/api/posts", methods=["POST"])
@login_required()
def create_post():
    body = request.json

    error_message = Post.validate(body)
    if error_message:
        return jsonify({"error": {"message": error_message}}), 400

    if session["user"]["_id"] != body["posted_by"]:
        return jsonify({"error": {"message": "投稿者が不正です"}}), 400

    last = Post._collection.find_one(
        {"posted_by": body["posted_by"]}, sort=[("created_at", pymongo.DESCENDING)]
    )

    if last and last["content"] == body["content"]:
        return jsonify({"error": {"message": "すでに同じ内容のツイートが投稿されています"}}), 400

    post = Post(content=body["content"], posted_by=body["posted_by"])

    post.create()

    body["_id"] = str(post._id)
    return jsonify(body)


@app.route("/api/posts", methods=["GET"])
@login_required()
def list_posts():
    results = []
    for post in Post._collection.find(sort=[("created_at", pymongo.DESCENDING)]):
        results.append(_populate(post))

    if results:
        user_id = ObjectId(session["user"]["_id"])
        term = {"$gte": results[-1]["created_at"], "$lte": results[0]["created_at"]}

        liked_posts = {
            str(like["post"])
            for like in Like._collection.find({"liked_by": user_id, "posted_at": term})
        }
        retweeted_posts = {
            str(retweet["post"])
            for retweet in Retweet._collection.find(
                {"retweeted_by": user_id, "posted_at": term}
            )
        }
        for result in results:
            result["liking"] = result["_id"] in liked_posts
            result["retweeting"] = result["_id"] in retweeted_posts

        for result in results:
            if (
                "retweeted_post" in result
                and result["retweeted_post"]
                and "_id" in result["retweeted_post"]
            ):
                retweeted_post_id = ObjectId(result["retweeted_post"]["_id"])
                result["retweeted_post"]["liking"] = (
                    Like._collection.find_one(
                        {"liked_by": user_id, "post": retweeted_post_id}
                    )
                    is not None
                )
                result["retweeted_post"]["retweeting"] = (
                    Retweet._collection.find_one(
                        {"retweeted_by": user_id, "post": retweeted_post_id}
                    )
                    is not None
                )

    return jsonify(results)


@app.route("/api/posts/<post_id>/like", methods=["POST"])
@login_required()
def like_post(post_id):
    post = Post._collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        return jsonify({"error": {"message": "投稿が存在しません"}}), 404
    user_id = session["user"]["_id"]
    like = Like._collection.find_one(
        {"post": ObjectId(post_id), "liked_by": ObjectId(user_id)}
    )
    if like:
        post["liking"] = True
        return jsonify(_populate(post))
    else:
        like = Like(post=post_id, posted_at=post["created_at"], liked_by=user_id)
        try:
            like.create()
        except pymongo.errors.DuplicateKeyError:
            pass
        like_count = Like._collection.count_documents({"post": ObjectId(post_id)})
        post = Post._collection.find_one_and_update(
            {"_id": ObjectId(post_id)},
            {"$set": {"like_count": like_count}},
            return_document=pymongo.ReturnDocument.AFTER,
        )
        post["liking"] = True
        return jsonify(_populate(post))


@app.route("/api/posts/<post_id>/like", methods=["DELETE"])
@login_required()
def unlike_post(post_id):
    post = Post._collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        return jsonify({"error": {"message": "投稿が存在しません"}}), 404
    user_id = session["user"]["_id"]
    like = Like._collection.find_one_and_delete(
        {"post": ObjectId(post_id), "liked_by": ObjectId(user_id)}
    )
    if not like:
        post["liking"] = False
        return jsonify(_populate(post))
    else:
        like_count = Like._collection.count_documents({"post": ObjectId(post_id)})
        post = Post._collection.find_one_and_update(
            {"_id": ObjectId(post_id)},
            {"$set": {"like_count": like_count}},
            return_document=pymongo.ReturnDocument.AFTER,
        )
        post["liking"] = False
        return jsonify(_populate(post))


@app.route("/api/posts/<post_id>/retweet", methods=["POST"])
@login_required()
def retweet_post(post_id):
    post = Post._collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        return jsonify({"error": {"message": "投稿が存在しません"}}), 404
    user_id = session["user"]["_id"]
    retweet = Retweet._collection.find_one(
        {"post": ObjectId(post_id), "retweeted_by": ObjectId(user_id)}
    )
    if retweet:
        post["retweeting"] = True
        return jsonify(_populate(post))
    else:
        retweet = Retweet(
            post=post_id, posted_at=post["created_at"], retweeted_by=user_id
        )
        try:
            retweet.create()
            retweeting_post = Post(
                content=None, posted_by=user_id, retweeted_post=post_id
            )
            retweeting_post.create()
        except pymongo.errors.DuplicateKeyError:
            pass
        retweet_count = Retweet._collection.count_documents({"post": ObjectId(post_id)})
        post = Post._collection.find_one_and_update(
            {"_id": ObjectId(post_id)},
            {"$set": {"retweet_count": retweet_count}},
            return_document=pymongo.ReturnDocument.AFTER,
        )
        post["retweeting"] = True

        return jsonify(_populate(post))


@app.route("/api/posts/<post_id>/retweet", methods=["DELETE"])
@login_required()
def unretweet_post(post_id):
    post = Post._collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        return jsonify({"error": {"message": "投稿が存在しません"}}), 404
    user_id = session["user"]["_id"]
    retweet = Retweet._collection.find_one_and_delete(
        {"post": ObjectId(post_id), "retweeted_by": ObjectId(user_id)}
    )
    Post._collection.find_one_and_delete(
        {"posted_by": ObjectId(user_id), "retweeted_post": ObjectId(post_id)}
    )
    if not retweet:
        post["retweeting"] = False
        return jsonify(_populate(post))
    else:
        retweet_count = Retweet._collection.count_documents({"post": ObjectId(post_id)})
        post = Post._collection.find_one_and_update(
            {"_id": ObjectId(post_id)},
            {"$set": {"retweet_count": retweet_count}},
            return_document=pymongo.ReturnDocument.AFTER,
        )
        post["retweeting"] = False

        return jsonify(_populate(post))


def _populate(post):
    if not post:
        return post
    post["_id"] = str(post["_id"])
    posted_by = User._collection.find_one({"_id": post["posted_by"]})
    if posted_by:
        posted_by["_id"] = str(posted_by["_id"])
        del posted_by["hashed_password"]
        post["posted_by"] = posted_by
    if "retweeted_post" in post and post["retweeted_post"]:
        post["retweeted_post"] = _populate(
            Post._collection.find_one({"_id": post["retweeted_post"]})
        )
    return post
