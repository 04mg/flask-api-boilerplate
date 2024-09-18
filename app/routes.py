from .resources.user import UserResource, UserListResource


def register_routes(app):
    app.add_url_rule("/users", view_func=UserListResource.as_view("user_list_resource"))
    app.add_url_rule(
        "/users/<int:user_id>", view_func=UserResource.as_view("user_resource")
    )
