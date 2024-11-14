import pytest
from unittest.mock import patch, Mock
from transact_flask.app import create_app

# Set up the Flask app fixture with database mocking
@pytest.fixture
def app():
    # Mock psycopg2.connect to prevent actual database connections
    with patch("transact_flask.app.psycopg2.connect") as mock_connect:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Mock database responses
        mock_cursor.fetchone.side_effect = [(1,), (2,), (3,)]
        mock_cursor.fetchall.side_effect = [
            [
                (1, "Whats your favorite color?", "Jimmy", "2024-11-13 01:01:01"),
                (2, "Anyone finish their project already?", "Humpfre", "2024-11-12 23:59:59"),
            ],
            [
                ("Apple", "Humpfre"),
                ("Blue", "Diego")
            ],
            [
                ("Nope", "Diego"),
                ("RIP", "Jimmy")
            ]
        ]

        # Ensure commit and close methods don't raise exceptions
        mock_conn.commit.return_value = None
        mock_cursor.close.return_value = None
        mock_conn.close.return_value = None

        # Initialize and yield the app for testing
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
    response = client.get("/")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200


def test_add_post(client):
    # Mock session to simulate a logged-in user
    with client.session_transaction() as session:
        session["user_id"] = 1  # Use a sample user ID

    response = client.post("/add_post", data={"content": "This is a test post"})

    # Check that the response redirects back to the home page
    assert response.status_code == 302
    assert response.location == "/"

    # Verify the SQL execution with the correct data
    cursor = client.application.db.cursor.return_value
    cursor.execute.assert_called_with(
        """INSERT INTO "Post" (contents, user_id, created_at) VALUES (%s, %s, %s)""",
        ("This is a test post", 1, ANY),  # ANY for the timestamp
    )


def test_add_comment(client):
    # Mock session to simulate a logged-in user
    with client.session_transaction() as session:
        session["user_id"] = 1  # Sample user ID
        session["admin"] = False  # Simulate a regular user (non-admin)

    response = client.post(
        "/add_comment", data={"content": "This is a test comment", "post_id": 1}
    )

    # Check that the response redirects back to the home page
    assert response.status_code == 302
    assert response.location == "/"

    # Verify the SQL execution with the correct data
    cursor = client.application.db.cursor.return_value
    cursor.execute.assert_called_with(
        """INSERT INTO "Comment" (contents, user_id, post_id, created_at) VALUES (%s, %s, %s, %s)""",
        ("This is a test comment", 1, 1, ANY),  # ANY for the timestamp
    )
