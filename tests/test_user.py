def test_user_creation(test_client):
    response = test_client.post(
        "/users", json={"username": "testuser", "email": "test@example.com"}
    )
    assert response.status_code == 201
