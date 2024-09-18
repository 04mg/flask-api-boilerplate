from .resources.tokens import (
    TokenLogin,
    TokenRefresh,
    TokenRegister,
)
from .resources.users import UsersMe


def register_routes(app):
    app.add_url_rule("/users/me", view_func=UsersMe.as_view("user_list_resource"))

    app.add_url_rule(
        "/tokens/login", view_func=TokenLogin.as_view("token_login_resource")
    )

    app.add_url_rule(
        "/tokens/register",
        view_func=TokenRegister.as_view("token_register_resource"),
    )

    app.add_url_rule(
        "/tokens/refresh",
        view_func=TokenRefresh.as_view("token_refresh_resource"),
    )
