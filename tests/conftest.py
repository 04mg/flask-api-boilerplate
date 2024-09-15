import pytest
from app import create_app, db
from app.config import TestConfig


@pytest.fixture(scope="module")
def app():
    app = create_app(TestConfig)
    with app.app_context():
        yield app


@pytest.fixture(scope="module")
def test_client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def setup_database():
    db.create_all()
    yield
    db.drop_all()
