TEST_DATA = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "password",
}


def test_post_token_register_returns_201(test_client, setup_database):
    response = test_client.post(
        "/tokens/register",
        json=TEST_DATA,
    )
    assert response.status_code == 201


def test_post_token_register_without_password_returns_400(test_client, setup_database):
    response = test_client.post(
        "/tokens/register",
        json=TEST_DATA | {"password": None},
    )

    assert response.status_code == 400


def test_post_token_register_without_email_returns_400(test_client, setup_database):
    response = test_client.post(
        "/tokens/register",
        json=TEST_DATA | {"email": None},
    )

    assert response.status_code == 400


def test_post_token_register_with_existing_email_returns_400(
    test_client, setup_database
):
    response = test_client.post(
        "/tokens/register",
        json=TEST_DATA,
    )

    response = test_client.post(
        "/tokens/register",
        json=TEST_DATA | {"username": "other"},
    )

    assert response.status_code == 400


def test_post_token_login_returns_200(test_client, setup_database):
    response = test_client.post(
        "/tokens/register",
        json=TEST_DATA,
    )

    response = test_client.post(
        "/tokens/login",
        json={"email": TEST_DATA["email"], "password": TEST_DATA["password"]},
    )

    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json


def test_post_token_login_with_invalid_password_returns_401(
    test_client, setup_database
):
    response = test_client.post(
        "/tokens/register",
        json=TEST_DATA,
    )

    response = test_client.post(
        "/tokens/login",
        json={"email": TEST_DATA["email"], "password": "wrongpassword"},
    )

    assert response.status_code == 401


def test_post_token_login_with_unknown_email_returns_401(test_client, setup_database):
    response = test_client.post(
        "/tokens/login",
        json={"email": TEST_DATA["email"], "password": TEST_DATA["password"]},
    )

    assert response.status_code == 401


def test_post_token_login_without_email_returns_400(test_client, setup_database):
    response = test_client.post(
        "/tokens/login",
        json={"password": TEST_DATA["password"]},
    )

    assert response.status_code == 400


def test_post_token_login_without_password_returns_400(test_client, setup_database):
    response = test_client.post(
        "/tokens/login",
        json={"email": TEST_DATA["email"]},
    )

    assert response.status_code == 400


def test_post_token_refresh_returns_200(test_client, setup_database):
    response = test_client.post(
        "/tokens/register",
        json=TEST_DATA,
    )

    response = test_client.post(
        "/tokens/login",
        json={"email": TEST_DATA["email"], "password": TEST_DATA["password"]},
    )

    response = test_client.post(
        "/tokens/refresh",
        json={"refresh_token": response.json["refresh_token"]},
    )

    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json


def test_post_token_refresh_without_refresh_token_returns_400(
    test_client, setup_database
):
    response = test_client.post(
        "/tokens/refresh",
        json={},
    )

    assert response.status_code == 400


def test_post_token_refresh_with_invalid_refresh_token_returns_401(
    test_client, setup_database
):
    response = test_client.post(
        "/tokens/refresh",
        json={"refresh_token": "invalid"},
    )

    assert response.status_code == 401
