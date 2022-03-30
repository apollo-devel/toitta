import logging
import os

from bson.objectid import ObjectId
from flask import Flask
from flask.json import JSONEncoder
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = "DUMMY"
app.config["SESSION_COOKIE_NAME"] = "__session"
app.logger.setLevel(logging.INFO)

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

socketio = SocketIO(app)


@socketio.on("connect")
def connect():
    app.logger.info("CONNECT")
    emit("connected", {"data": "connected!"})


@socketio.on("ev1")
def ev1():
    app.logger.info("EV1")
    emit("resp1", {"data": "resp1!"})


from apis import login, notifications, posts, users
