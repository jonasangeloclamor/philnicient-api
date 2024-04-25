from functools import wraps
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.user_service import get_user_service

def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = get_user_service(current_user_id)
            if user.role in roles:
                return fn(*args, **kwargs)
            else:
                if len(roles) == 1:
                    role_message = 'Unauthorized. Role required: {}'.format(roles[0])
                else:
                    role_message = 'Unauthorized. Roles required: {}'.format(roles)
                return {'message': role_message}, 403
        return wrapper
    return decorator
