from flask.views import MethodView
from ..models.user import User
from ..extensions import db
from ..utils.tokens import requires_token, get_user_id_from_token


class UsersMe(MethodView):
    @requires_token
    def get(self):
        user_id = get_user_id_from_token()
        user = db.session.get(User, user_id)
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
