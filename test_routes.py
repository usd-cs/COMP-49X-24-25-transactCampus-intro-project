import pytest
import psycopg2
from transact_flask.app import create_app  # Import your app factory function


@pytest.fixture
def client():
    app = create_app(
        {
            "TESTING": True,  # Enable testing mode
        }
    )
    with app.test_client() as client:
        with app.app_context():
            # Initialize any database setup or other configuration here if needed
            pass
        yield client  # Provide the test client to tests


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_login(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_comment(client):
    response = client.get("/comment")
    assert response.status_code == 200


def test_public_posts(client):
    response = client.get("/public")
    assert response.status_code == 200


def test_valid_login(client):
    # Add a test user to the database directly
    with client.application.app_context():
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute(
            """INSERT INTO "User" (email, name, admin, password) VALUES ('testuser@sandiego.edu', 'Test User', FALSE, 'testpassword');"""
        )
        connection.commit()
        cur.close()

    # Attempt login with the test user's credentials
    response = client.post(
        "/login",
        data={"email": "testuser@sandiego.edu", "password": "testpassword"},
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_create_post(client):
    # Simulate a logged-in user
    with client.session_transaction() as session:
        session["user_id"] = 1  # Use an appropriate user ID

    response = client.post(
        "/add_post", data={"content": "Test post content"}, follow_redirects=True
    )
    assert response.status_code == 200


def get_db_connection():
    conn = psycopg2.connect(
        database="intro_project",
        user="postgres",
        password="8412",
        host="localhost",
        port="5432",
    )
    return conn
