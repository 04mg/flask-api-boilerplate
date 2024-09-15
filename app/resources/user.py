from flask_restful import Resource, reqparse
from ..models.user import User
from ..extensions import db

parser = reqparse.RequestParser()
parser.add_argument("username", required=True, help="Username is required")
parser.add_argument("email", required=True, help="Email is required")


class UserResource(Resource):
    def get(self, user_id):
        user = db.get_or_404(User, user_id)
        return {"id": user.id, "username": user.username, "email": user.email}

    def delete(self, user_id):
        user = db.get_or_404(User, user_id)
        db.session.delete(user)
        db.session.commit()
        return "", 204


class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return [
            {"id": user.id, "username": user.username, "email": user.email}
            for user in users
        ]

    def post(self):
        args = parser.parse_args()
        new_user = User(username=args["username"], email=args["email"])
        db.session.add(new_user)
        db.session.commit()
        return {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
        }, 201
