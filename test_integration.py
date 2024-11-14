import pytest
from transact_flask.app import create_app

# Set up the Flask app fixture without database dependencies
@pytest.fixture
def app():
    app = create_app()
    return app

# Provide a test client to send requests
@pytest.fixture
def client(app):
    return app.test_client()

# Test that the app's homepage loads successfully
def test_homepage_loads(client):
    response = client.get('/')
    assert response.status_code == 200

# Test that the app's admin page loads (if it exists), without checking for admin permissions
def test_admin_page_loads(client):
    response = client.get('/admin')
    assert response.status_code in [200, 302, 404]  # Check for OK, redirect, or not found

# Test that the login page loads successfully
def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200
