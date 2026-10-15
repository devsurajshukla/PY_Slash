import os
import jwt

from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

def token_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({
                "success": False,
                "message": "Authentication token is required."
            }), 401

        token = auth_header.split(" ", 1)[1]

        try:
            payload = jwt.decode(
                token,
                JWT_SECRET_KEY,
                algorithms=["HS256"]
            )

            request.current_user = payload

        except jwt.ExpiredSignatureError:
            return jsonify({
                "success": False,
                "message": "Token has expired."
            }), 401

        except jwt.InvalidTokenError:
            return jsonify({
                "success": False,
                "message": "Invalid token."
            }), 401

        return f(*args, **kwargs)

    return wrapper

def role_required(*allowed_roles):

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            current_user = getattr(
                request,
                "current_user",
                None
            )

            if not current_user:
                return jsonify({
                    "success": False,
                    "message": "Authentication required."
                }), 401

            user_role = current_user.get("role")

            if user_role not in allowed_roles:
                return jsonify({
                    "success": False,
                    "message": "You do not have permission to access this resource."
                }), 403

            return function(*args, **kwargs)

        return wrapper

    return decorator