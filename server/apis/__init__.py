import functools

from flask import jsonify, session


def login_required(status=401):
    def wrapper(f):
        @functools.wraps(f)
        def _wrapper(*args, **kwargs):
            if (
                "user" not in session
                or not session["user"]
                or "_id" not in session["user"]
            ):
                return jsonify({"error": {"message": "権限がありません"}}), status
            return f(*args, **kwargs)

        return _wrapper

    return wrapper
