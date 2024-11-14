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

@pytest.fixture
def client(app):
    return app.test_client()
