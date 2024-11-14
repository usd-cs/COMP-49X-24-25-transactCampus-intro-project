import pytest
from transact_flask import app


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        # Add any other configuration needed for integration tests
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()
