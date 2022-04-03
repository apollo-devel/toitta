from flask import jsonify, request, session

from apis import error, login_required
from main import app
from models.chat import Chat


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
