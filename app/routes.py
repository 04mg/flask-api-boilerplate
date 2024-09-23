from .resources.auth import (
    AuthLoginGoogle,
    AuthLogin,
    AuthRefresh,
    AuthRegister,
)
from .resources.users import UsersMe, UsersPassword


def register_routes(app):
    app.add_url_rule("/auth/login", view_func=AuthLogin.as_view("token_login_resource"))

    app.add_url_rule(
        "/auth/register",
        view_func=AuthRegister.as_view("token_register_resource"),
    )

    app.add_url_rule(
        "/auth/refresh",
        view_func=AuthRefresh.as_view("token_refresh_resource"),
    )

    app.add_url_rule(
        "/auth/google",
        view_func=AuthLoginGoogle.as_view("token_google_login_resource"),
    )

    app.add_url_rule("/users/me", view_func=UsersMe.as_view("users_me"))
    app.add_url_rule(
        "/users/password", view_func=UsersPassword.as_view("users_password")
    )
