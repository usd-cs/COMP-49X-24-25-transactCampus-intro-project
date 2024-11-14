import pytest
from unittest.mock import patch, Mock
from transact_flask.app import create_app

# Fixture to create the app without modifying app.py
@pytest.fixture
def app():
    # Mock psycopg2.connect to avoid a real database connection
    with patch("transact_flask.app.psycopg2.connect") as mock_connect:
        # Set up the mock connection and cursor
        mock_conn = Mock()
        mock_cursor = Mock()

        # Make .cursor() return the mock cursor
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Mock `fetchone` to return a tuple with a fake ID (as would happen in the real db)
        mock_cursor.fetchone.return_value = (1,)  # Simulate returning a tuple like (id,)

        # Mock `fetchall` to return sample data for posts and comments
        # This should match the structure of the actual database query output in the app
        mock_cursor.fetchall.side_effect = [
            # Simulate posts data as list of tuples (id, contents, user_name, created_at)
            [(1, "Whats your favorite color?", "Jimmy", "2024-11-13 01:01:01"),
             (2, "Anyone finish their project already?", "Humpfre", "2024-11-12 23:59:59")],
            # Simulate comments data for the first post
            [("Apple", "Humpfre"), ("Blue", "Diego")],
            # Simulate comments data for the second post
            [("Nope", "Diego"), ("RIP", "Jimmy")]
        ]

        # Simulate commit to ensure no errors are raised
        mock_conn.commit.return_value = None

        # Initialize the Flask app without test-specific configurations
        app = create_app()
        yield app

        # After each test, verify that close() was called on the cursor and connection
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

# Fixture to provide a test client
@pytest.fixture
def client(app):
    return app.test_client()

# Test function to check if the homepage loads successfully
def test_homepage_loads(client):
    # Send a GET request 
    response = client.get('/')
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
