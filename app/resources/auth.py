from flask.views import MethodView
from flask import request, current_app
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest, Unauthorized, Conflict

from ..models.user import User
from ..utils.tokens import generate_tokens
from ..extensions import db, oauth


class AuthBase(MethodView):
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def validate_email_password(email, password):
        if not email or not password:
            raise BadRequest("Email and password are required")

    @staticmethod
    def create_user(email, password):
        new_user = User(
            email=email, password=generate_password_hash(password) if password else None
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def generate_token_response(user_id):
        access_token, refresh_token = generate_tokens(user_id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }


class AuthLogin(AuthBase):
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")

        self.validate_email_password(email, password)

        user = self.get_user_by_email(email)
        if not user or not check_password_hash(user.password, password):
            raise Unauthorized("Invalid email or password")

        return self.generate_token_response(user.id)


class AuthLoginGoogle(AuthBase):
    def get(self):
        try:
            token = oauth.google.authorize_access_token()
        except Exception:
            raise Unauthorized("Invalid access token")

        email = token["userinfo"]["email"]

        user = self.get_user_by_email(email)

        if not user:
            user = self.create_user(email, None)

        return self.generate_token_response(user.id)


class AuthRegister(AuthBase):
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")

        self.validate_email_password(email, password)

        if self.get_user_by_email(email):
            raise Conflict("Email is already in use")

        new_user = self.create_user(email, password)

        return self.generate_token_response(new_user.id), 201


class AuthRefresh(AuthBase):
    def post(self):
        refresh_token = request.json.get("refresh_token")
        if not refresh_token:
            raise BadRequest("Refresh token is missing!")

        try:
            data = jwt.decode(
                refresh_token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            if data["token_type"] != "refresh":
                raise Unauthorized("Invalid token type!")
            user_id = data["user_id"]

            return self.generate_token_response(user_id)

        except jwt.ExpiredSignatureError:
            raise Unauthorized("Refresh token has expired!")
        except jwt.InvalidTokenError:
            raise Unauthorized("Invalid refresh token!")
