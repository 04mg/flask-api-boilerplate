from flask.views import MethodView
from flask import request, current_app
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

from ..models.user import User
from ..utils.tokens import generate_tokens
from ..extensions import db


class TokenLogin(MethodView):
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"message": "Email and password are required"}, 400

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return {"message": "Invalid email or password"}, 401

        access_token, refresh_token = generate_tokens(user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id,
        }


class TokenRegister(MethodView):
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"message": "Email and password are required"}, 400

        if User.query.filter_by(email=email).first():
            return {"message": "Email is already in use"}, 400


        new_user = User(
            email=email, password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        access_token, refresh_token = generate_tokens(new_user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": new_user.id,
        }, 201


class TokenRefresh(MethodView):
    def post(self):
        refresh_token = request.json.get("refresh_token")
        if not refresh_token:
            return {"message": "Refresh token is missing!"}, 400
        try:
            data = jwt.decode(
                refresh_token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            if data["token_type"] != "refresh":
                return {"message": "Invalid token type!"}, 401
            user_id = data["user_id"]

            new_access_token, new_refresh_token = generate_tokens(user_id)

            return {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
            }, 200
        except jwt.ExpiredSignatureError:
            return {"message": "Refresh token has expired!"}, 401
        except jwt.InvalidTokenError:
            return {"message": "Invalid refresh token!"}, 401
