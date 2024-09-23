from unittest.mock import patch


def test_get_users_me_returns_200(test_client, setup_database):
    response = test_client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "test"},
    )

    response = test_client.get(
        "/users/me",
        headers={"Authorization": response.json["access_token"]},
    )

    assert response.status_code == 200
    assert response.json["email"] == "test@example.com"


def test_get_users_me_without_token_returns_401(test_client, setup_database):
    response = test_client.get("/users/me")
    assert response.status_code == 401


def test_put_update_password_with_token(test_client, setup_database):
    response = test_client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "test"},
    )

    access_token = response.json["access_token"]

    with patch("app.extensions.db.session.commit") as mock_commit:
        response = test_client.put(
            "/users/password",
            headers={"Authorization": access_token},
            json={"new_password": "new_password_123"},
        )

        assert response.status_code == 200
        mock_commit.assert_called_once()


@patch("app.resources.users.send")
def test_put_recover_password_with_email(mock_send, test_client, setup_database):
    test_client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123"},
    )

    response = test_client.put("/users/password", json={"email": "test@example.com"})

    assert response.status_code == 200
    mock_send.assert_called_once()


def test_put_recover_password_without_email_returns_400(test_client, setup_database):
    response = test_client.put("/users/password", json={})

    assert response.status_code == 400
    assert response.json["message"] == "Email is required"


def test_put_recover_password_with_nonexistent_user_returns_404(
    test_client, setup_database
):
    response = test_client.put(
        "/users/password", json={"email": "nonexistent@example.com"}
    )

    assert response.status_code == 404
    assert response.json["message"] == "User not found"


def test_put_update_password_social_login_returns_401(test_client, setup_database):
    mock_token = {"userinfo": {"email": "new_user@example.com"}}
    with patch(
        "app.extensions.oauth.google.authorize_access_token",
        return_value=mock_token,
    ):
        access_token = test_client.get("/auth/google").json["access_token"]

        with patch("app.models.user.User.password", new=None):
            response = test_client.put(
                "/users/password",
                headers={"Authorization": access_token},
                json={"new_password": "new_password_123"},
            )

            assert response.status_code == 401
