def test_get_users_me_returns_200(test_client, setup_database):
    response = test_client.post(
        "/tokens/register",
        json={"email": "test@example.com", "username": "test", "password": "test"},
    )

    response = test_client.get(
        "/users/me",
        headers={"Authorization": response.json["access_token"]},
    )

    assert response.status_code == 200
    assert response.json["username"] == "test"
    assert response.json["email"] == "test@example.com"


def test_get_users_me_without_token_returns_401(test_client, setup_database):
    response = test_client.get("/users/me")
    assert response.status_code == 401
