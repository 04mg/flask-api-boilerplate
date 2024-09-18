from flask.views import MethodView
from flask import request
from ..models.user import User
from ..extensions import db


class UserResource(MethodView):
    def get(self, user_id):
        user = db.get_or_404(User, user_id)
        return {"id": user.id, "username": user.username, "email": user.email}

    def delete(self, user_id):
        user = db.get_or_404(User, user_id)
        db.session.delete(user)
        db.session.commit()
        return "", 204


class UserListResource(MethodView):
    def get(self):
        print("a" *100)
        users = User.query.all()
        print("b"*100)
        return [
            {"id": user.id, "username": user.username, "email": user.email}
            for user in users
        ]

    def post(self):
        args = request.get_json()
        new_user = User(username=args["username"], email=args["email"])
        db.session.add(new_user)
        db.session.commit()
        return {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
        }, 201
