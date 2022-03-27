import pymongo
from bson.objectid import ObjectId
from flask import jsonify, request, session

from apis import login_required
from main import app
from models.notification import Notification
from models.user import User


@app.route("/api/notifications", methods=["GET"])
@login_required()
def list_notifications():
    user_id = ObjectId(session["user"]["_id"])
    condition = {"user_to": user_id}
    unread_only = request.args.get("unread_only", False)
    if unread_only:
        condition["opened"] = False

    results = []
    for notification in Notification._collection.find(
        condition, sort=[("created_at", pymongo.DESCENDING)]
    ):
        results.append(_populate(notification))

    if not unread_only and results:
        _mark_as_read(results)

    return jsonify(results)


def _populate(notification):
    user_from = User._collection.find_one({"_id": notification["user_from"]})
    if user_from:
        del user_from["hashed_password"]
        notification["user_from"] = user_from

    return notification


def _mark_as_read(notifications):
    ids = [n["_id"] for n in notifications]
    Notification._collection.update_many(
        {"_id": {"$in": ids}}, {"$set": {"opened": True}}
    )
