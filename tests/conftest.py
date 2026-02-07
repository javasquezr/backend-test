import pytest
from app.app import create_app
from app.config import Config

class TestConfig(Config):
    TESTING = True
    EXTERNAL_API_URL = "https://mock-api.com"

@pytest.fixture
def app():
    app = create_app(TestConfig)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
