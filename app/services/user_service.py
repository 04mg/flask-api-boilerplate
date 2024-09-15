from ..models.user import User
from ..extensions import db


def create_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


def get_user(user_id):
    return User.query.get(user_id)


def delete_user(user):
    db.session.delete(user)
    db.session.commit()
