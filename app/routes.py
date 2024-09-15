from .resources.user import UserResource, UserListResource


def register_routes(api):
    api.add_resource(UserListResource, "/users")
    api.add_resource(UserResource, "/users/<int:user_id>")
