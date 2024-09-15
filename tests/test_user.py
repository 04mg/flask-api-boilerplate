def test_post_user_returns_201(test_client, setup_database):
    response = test_client.post(
        "/users", json={"username": "testuser", "email": "test@example.com"}
    )
    assert response.status_code == 201


def test_get_users_by_id_returns_user(test_client, setup_database):
    response = test_client.post(
        "/users", json={"username": "testuser", "email": "test@example.com"}
    )
    user_id = response.json["id"]
    response = test_client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json["username"] == "testuser"
    assert response.json["email"] == "test@example.com"


def test_get_users_by_id_returns_404_for_nonexistent_user(test_client, setup_database):
    response = test_client.get("/users/123")
    assert response.status_code == 404


def test_get_users_returns_all_users(test_client, setup_database):
    response = test_client.post(
        "/users", json={"username": "testuser", "email": "test@example.com"}
    )
    response = test_client.get("/users")
    assert response.status_code == 200
    assert len(response.json) == 1


def test_delete_user_returns_204(test_client, setup_database):
    response = test_client.post(
        "/users", json={"username": "testuser", "email": "test@example.com"}
    )
    user_id = response.json["id"]
    response = test_client.delete(f"/users/{user_id}")
    assert response.status_code == 204
