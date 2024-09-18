from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import request, current_app
import jwt


def generate_tokens(user_id):
    access_token_payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(timezone.utc),
        "token_type": "access",
    }
    access_token = jwt.encode(
        access_token_payload, current_app.config["SECRET_KEY"], algorithm="HS256"
    )

    refresh_token_payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=30),
        "iat": datetime.now(timezone.utc),
        "token_type": "refresh",
    }
    refresh_token = jwt.encode(
        refresh_token_payload, current_app.config["SECRET_KEY"], algorithm="HS256"
    )

    return access_token, refresh_token


def requires_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return {"message": "Token is missing"}, 401
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            if data["token_type"] != "access":
                return {"message": "Invalid token type"}, 401
        except jwt.ExpiredSignatureError:
            return {"message": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"message": "Invalid token"}, 401
        return f(*args, **kwargs)

    return decorated


def get_user_id_from_token():
    try:
        token = request.headers.get("Authorization")
        data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return data["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
