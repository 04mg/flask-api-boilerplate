import pytest
from app import create_app, db
from app.config import TestConfig


@pytest.fixture(scope="module")
def test_client():
    app = create_app(TestConfig)
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()
