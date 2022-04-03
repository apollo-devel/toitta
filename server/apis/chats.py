from bson.objectid import ObjectId
from flask import jsonify, request, session

from apis import error, login_required
from main import app
from models.chat import Chat
from models.message import Message


@app.route("/api/chats", methods=["POST"])
@login_required()
def create_chat():
    body = request.json

    error_message = Chat.validate(body, session["user"]["_id"])
    if error_message:
        return error(error_message)
    users = body["users"]
    chat = Chat(name=body.get("name"), is_group_chat=True, users=users)
    chat.create()
    return jsonify(vars(chat))


@app.route("/api/chats", methods=["GET"])
@login_required()
def list_chats():
    chats = [chat for chat in Chat.list_chats(session["user"]["_id"])]
    return jsonify(chats)


@app.route("/api/chats/<chat_id>/messages", methods=["POST"])
@login_required()
def create_message(chat_id):
    body = request.json

    user_id = session["user"]["_id"]
    error_message = Message.validate(body, user_id)
    if error_message:
        return error(error_message)

    chat = Chat._collection.find_one({"_id": ObjectId(chat_id)})
    if not chat or ObjectId(user_id) not in chat.get("users", []):
        return error("チャットが存在しないか、参加していないチャットです")

    message = Message(content=body["content"], chat=chat_id, sender=user_id)
    message.create()
    message = vars(message)
    message["sender"] = session["user"]
    return jsonify(message)


@app.route("/api/chats/<chat_id>", methods=["GET"])
@login_required()
def get_chat(chat_id):
    chat = Chat.get_chat(chat_id)
    if not chat:
        return error("チャットが存在しないか、参加していないチャットです")
    user_id = session["user"]["_id"]
    if not [u for u in chat.get("users", []) if u["_id"] == ObjectId(user_id)]:
        return error("チャットが存在しないか、参加していないチャットです")
    return jsonify(chat)


@app.route("/api/chats/<chat_id>/messages", methods=["GET"])
@login_required()
def list_messages(chat_id):
    chat = Chat.get_chat(chat_id)
    if not chat:
        return error("チャットが存在しないか、参加していないチャットです")
    user_id = session["user"]["_id"]
    if not [u for u in chat.get("users", []) if u["_id"] == ObjectId(user_id)]:
        return error("チャットが存在しないか、参加していないチャットです")
    return jsonify(list(Message.list_messages(chat_id)))
