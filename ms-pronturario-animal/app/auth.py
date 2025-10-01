from flask_jwt_extended import verify_jwt_in_request
from flask import jsonify
from functools import wraps

def jwt_protected(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            return jsonify({'message': 'Token inválido ou ausente'}), 401
        return fn(*args, **kwargs)
    return wrapper
