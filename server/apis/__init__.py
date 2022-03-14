import functools
from flask import session, jsonify

def login_required(status=401):
    def wrapper(f):
        @functools.wraps(f)
        def _wrapper(*args, **kwargs):
            if 'user' not in session:
                return jsonify({'error': { 'message': '権限がありません' }}), status
            return f(*args, **kwargs)
        return _wrapper
    return wrapper
