from unittest import mock
import pytest
from app import create_app, db
from app.config import TestConfig


@pytest.fixture(scope="module")
def app():
    app = create_app(TestConfig)
    with app.app_context():
        yield app


@pytest.fixture(scope="session", autouse=True)
def send_mail_mock():
    with mock.patch("app.resources.auth.send") as mock_send:
        yield mock_send


@pytest.fixture(scope="module")
def test_client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def setup_database():
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()
