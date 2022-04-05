import logging
import os

from bson.objectid import ObjectId
from flask import Flask
from flask.json import JSONEncoder
from flask_socketio import SocketIO, join_room

app = Flask(__name__)
app.secret_key = "DUMMY"
app.config["SESSION_COOKIE_NAME"] = "__session"
app.logger.setLevel(logging.INFO)

socketio = SocketIO(app)

if os.environ.get("PROFILE"):
    from werkzeug.middleware.profiler import ProfilerMiddleware

    app.config["PROFILE"] = True
    app.wsgi_app = ProfilerMiddleware(
        app.wsgi_app, sort_by=["tottime"], restrictions=[20]
    )


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


app.json_encoder = CustomJSONEncoder


@socketio.on("join")
def join(payload):
    if not payload.get("_id"):
        return
    join_room(payload.get("_id"))


from apis import chats, login, notifications, posts, users
