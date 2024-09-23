from flask import request, render_template
from flask.views import MethodView
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized
from werkzeug.security import generate_password_hash
from ..models.user import User
from ..extensions import db
from ..utils.tokens import requires_token, get_user_id_from_token, generate_tokens
from ..utils.mail import send


class UserBase(MethodView):
    @staticmethod
    def get_user(user_id=None, email=None):
        if user_id:
            user = db.session.get(User, user_id)
        elif email:
            user = User.query.filter_by(email=email).first()
        else:
            raise BadRequest("User ID or email is required")

        if not user:
            raise NotFound("User not found")
        return user

    @staticmethod
    def check_user_has_password(user):
        if not user.password:
            raise Unauthorized("You registered using social login")


class UsersMe(UserBase):
    @requires_token
    def get(self):
        user_id = get_user_id_from_token()
        user = self.get_user(user_id=user_id)
        return {
            "id": user.id,
            "email": user.email,
        }


class UsersPassword(UserBase):
    def put(self):
        user_id = get_user_id_from_token()
        if user_id:
            return self._update_password(user_id)
        else:
            return self._recover_password()

    def _update_password(self, user_id):
        user = self.get_user(user_id=user_id)
        self.check_user_has_password(user)

        new_password = request.json.get("new_password")
        if not new_password:
            raise BadRequest("New password is required")

        user.password = generate_password_hash(new_password)
        db.session.commit()
        return {"message": "Your password has been changed"}, 200

    def _recover_password(self):
        email = request.json.get("email")

        if not email:
            raise BadRequest("Email is required")

        user = self.get_user(email=email)
        self.check_user_has_password(user)

        access_token, _ = generate_tokens(user.id)
        send(
            to_email=email,
            subject="Password recovery",
            body=render_template("password_recovery.html", token=access_token),
        )
        return {"message": "If the email exists, a recovery email was sent"}, 200
