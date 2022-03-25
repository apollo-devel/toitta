import pymongo
from bson.objectid import ObjectId
from flask import jsonify, request, session

from apis import error, login_required
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
        return error(error_message)

    if session["user"]["_id"] != body["posted_by"]:
        return error("投稿者が不正です")

    last = Post._collection.find_one(
        {"posted_by": body["posted_by"]}, sort=[("created_at", pymongo.DESCENDING)]
    )

    if last and last["content"] == body["content"]:
        return error("すでに同じ内容のツイートが投稿されています")

    reply_to = None
    if "reply_to" in body and body["reply_to"]:
        reply_to = body["reply_to"]

    post = Post(content=body["content"], posted_by=body["posted_by"], reply_to=reply_to)

    post.create()

    if "reply_to" in body and body["reply_to"]:
        reply_count = Post._collection.count_documents({"reply_to": ObjectId(reply_to)})
        Post._collection.find_one_and_update(
            {"_id": ObjectId(reply_to)}, {"$set": {"reply_count": reply_count}}
        )

    return jsonify(_populate(vars(post)))


@app.route("/api/posts", methods=["GET"])
@login_required()
def list_posts():
    ids = [ObjectId(idx) for idx in session["user"]["following"]]
    ids.append(ObjectId(session["user"]["_id"]))

    results = []
    for post in Post._collection.find(
        {"posted_by": {"$in": ids}}, sort=[("created_at", pymongo.DESCENDING)]
    ):
        results.append(_populate(post))

    if results:
        _set_liking_and_retweeting(results)

    return jsonify(results)


@app.route("/api/users/<username>/posts", methods=["GET"])
@login_required()
def list_user_posts(username):
    user = User._collection.find_one({"username": username})
    if not user:
        return error("ユーザーが存在しません。")

    post_type = request.args.get("type", "tweets")

    results = []
    if post_type == "tweets":
        # ツイート
        condition = {"posted_by": user["_id"], "reply_to": None}
        for post in Post._collection.find(
            condition, sort=[("created_at", pymongo.DESCENDING)]
        ):
            results.append(_populate(post))
    elif post_type == "tweets_and_replies":
        # ツイートと返信
        condition = {"posted_by": user["_id"]}
        for post in Post._collection.find(
            condition, sort=[("created_at", pymongo.DESCENDING)]
        ):
            results.append(_populate(post))
    elif post_type == "likes":
        # いいね
        for like in Like._collection.find(
            {"liked_by": user["_id"]}, sort=[("liked_at", pymongo.DESCENDING)]
        ):
            post = Post._collection.find_one({"_id": like["post"]})
            results.append(_populate(post))
    else:
        app.logger.error(f"不明な種別が指定されました: {post_type}")
        return error("Internal Server Error", 500)

    if results:
        _set_liking_and_retweeting(results)

    return jsonify(results)


def _set_liking_and_retweeting(results):
    """
    resultsの各要素に、ログインユーザーが いいね / リツイート をしたかどうかを
    表す liking / retweeting フィールドを設定する。

    results は Post._collection.find の戻り値の各要素を _populate した配列
    が渡されることを想定している。
    """
    user_id = ObjectId(session["user"]["_id"])
    term = {"$gte": results[-1]["created_at"], "$lte": results[0]["created_at"]}

    liked_posts = {
        like["post"]
        for like in Like._collection.find({"liked_by": user_id, "posted_at": term})
    }
    retweeted_posts = {
        retweet["post"]
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


@app.route("/api/posts/<post_id>/like", methods=["POST"])
@login_required()
def like_post(post_id):
    post = Post._collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        return error("投稿が存在しません", 404)
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
        return error("投稿が存在しません", 404)
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
        return error("投稿が存在しません", 404)
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
        return error("投稿が存在しません", 404)
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


@app.route("/api/posts/<post_id>", methods=["GET"])
@login_required()
def get_post(post_id):
    post = Post._collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        return error("投稿が存在しません", 404)
    post = _populate(post, True)
    replies = []
    for reply in Post._collection.find(
        {"reply_to": ObjectId(post_id)}, sort=[("created_at", pymongo.ASCENDING)]
    ):
        replies.append(_populate(reply, True))
    post["replies"] = replies
    return jsonify(post)


@app.route("/api/posts/<post_id>", methods=["DELETE"])
@login_required()
def delete_post(post_id):
    post = Post._collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        return error("投稿が存在しません", 404)
    user_id = session["user"]["_id"]
    if str(post["posted_by"]) != user_id:
        return error("投稿を削除できません")
    Like._collection.delete_many({"post": ObjectId(post_id)})
    Retweet._collection.delete_many({"post": ObjectId(post_id)})

    Post._collection.find_one_and_delete({"_id": ObjectId(post_id)})

    if "reply_to" in post and post["reply_to"]:
        reply_to = post["reply_to"]
        reply_count = Post._collection.count_documents({"reply_to": reply_to})
        Post._collection.find_one_and_update(
            {"_id": reply_to}, {"$set": {"reply_count": reply_count}}
        )

    return "", 204


def _populate(post, set_liking_and_retweeting=False):
    if not post:
        return post
    posted_by = User._collection.find_one({"_id": post["posted_by"]})
    if posted_by:
        del posted_by["hashed_password"]
        post["posted_by"] = posted_by
    if "retweeted_post" in post and post["retweeted_post"]:
        post["retweeted_post"] = _populate(
            Post._collection.find_one({"_id": post["retweeted_post"]}),
            set_liking_and_retweeting,
        )
    if "reply_to" in post and post["reply_to"]:
        post["reply_to"] = _populate(
            Post._collection.find_one({"_id": post["reply_to"]}),
            set_liking_and_retweeting,
        )
    if set_liking_and_retweeting:
        user_id = ObjectId(session["user"]["_id"])
        post_id = post["_id"]
        if not isinstance(post_id, ObjectId):
            post_id = ObjectId(post_id)
        post["liking"] = (
            Like._collection.find_one({"liked_by": user_id, "post": post_id})
            is not None
        )
        post["retweeting"] = (
            Retweet._collection.find_one({"retweeted_by": user_id, "post": post_id})
            is not None
        )
    return post
