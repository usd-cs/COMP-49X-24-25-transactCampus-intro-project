import pytest
from flask import session
from unittest.mock import patch, Mock
from transact_flask.app import create_app  # Import your app factory function

# Mock database connection and cursor
@pytest.fixture
def mock_db():
    with patch("transact_flask.app.psycopg2.connect") as mock_connect:
        # Mock connection and cursor behavior
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Simulate fetchone to return sample IDs
        mock_cursor.fetchone.side_effect = [(1,), (2,)]  # User ID, Post ID

        # Yield the app with the mock database
        yield mock_connect, mock_cursor

        # Ensure cursor and connection are closed after each test
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

# Fixture to create a test app with mock database connection
@pytest.fixture
def app(mock_db):
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app

# Fixture to create a test client for HTTP requests
@pytest.fixture
def client(app):
    return app.test_client()

def test_add_comment(client, mock_db):
    mock_connect, mock_cursor = mock_db

    # Simulate adding a user and a post
    with client.application.app_context():
        # Create a test post and user session
        mock_cursor.fetchone.side_effect = [(1,), (2,)]  # Mock user_id and post_id

    # Simulate user login by setting session
    with client.session_transaction() as session:
        session["user_id"] = 1  # Use the mocked user ID

    # Post a comment to a test post
    response = client.post(
        "/add_comment",
        data={"post_id": 2, "content": "This is a test comment"},
        follow_redirects=True
    )

    # Verify response and that the comment was "added" (check cursor call args)
    assert response.status_code == 200
    mock_cursor.execute.assert_any_call(
        """INSERT INTO "Comment" (contents, user_id, post_id, created_at) VALUES (%s, %s, %s, %s)""",
        ("This is a test comment", 1, 2, pytest.mock.ANY)
    )
