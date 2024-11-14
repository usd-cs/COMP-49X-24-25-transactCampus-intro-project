import pytest
from unittest.mock import patch, Mock
from transact_flask.app import create_app

# Setup all mocking and fixtures in one file
@pytest.fixture
def app():
    # Mock psycopg2.connect to avoid a real database connection
    with patch("transact_flask.app.psycopg2.connect") as mock_connect:
        # Set up the mock connection and cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Mock database responses for various fetch calls
        mock_cursor.fetchone.side_effect = [(1,), (2,), (3,)]  # Return IDs for each user or post
        mock_cursor.fetchall.side_effect = [
            [
                (1, "Whats your favorite color?", "Jimmy", "2024-11-13 01:01:01"),
                (2, "Anyone finish their project already?", "Humpfre", "2024-11-12 23:59:59"),
            ],  # Mock posts data for `home` or `public_posts` route
            [
                ("Apple", "Humpfre"),
                ("Blue", "Diego")
            ],  # Comments for the first post
            [
                ("Nope", "Diego"),
                ("RIP", "Jimmy")
            ]  # Comments for the second post
        ]

        # Simulate commit and close methods
        mock_conn.commit.return_value = None
        mock_cursor.close.return_value = None
        mock_conn.close.return_value = None

        # Initialize the Flask app
        app = create_app()
        
        yield app  # Correctly yield the app for testing

@pytest.fixture
def client(app):
    return app.test_client()

# Test for homepage loading
def test_homepage_loads(client):
    response = client.get('/')
    assert response.status_code == 200

# Test for admin page loading (assuming a session-based admin view is implemented)
def test_admin_page_loads(client):
    with client.session_transaction() as session:
        session['admin'] = True  # Mock admin privilege in session
    response = client.get('/admin')
    assert response.status_code == 200

# Test login with valid credentials
def test_valid_login(client):
    with client.session_transaction() as session:
        session['user_id'] = 1  # Set up a logged-in user session
    response = client.post('/login', data={"email": "Jimmy@sandiego.edu", "password": "007"})
    assert response.status_code == 302  # Expect redirection after login
    assert response.location.endswith("/admin")  # Redirect to admin page if logged in as admin
