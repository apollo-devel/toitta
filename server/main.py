import logging

from bson.objectid import ObjectId
from flask import Flask
from flask.json import JSONEncoder

app = Flask(__name__)
app.secret_key = "DUMMY"
app.config["SESSION_COOKIE_NAME"] = "__session"
app.logger.setLevel(logging.INFO)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


app.json_encoder = CustomJSONEncoder

from apis import login, posts, users
