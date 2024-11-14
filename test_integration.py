import pytest
from transact_flask.app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,  # Enable testing mode
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_homepage_loads(client):
    # Send a GET request to the homepage
    response = client.get('/')
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
