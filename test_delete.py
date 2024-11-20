import pytest
from flask import session
from transact_flask.app import create_app, Base, get_db_connection, User, Post, Comment
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Configuration for the test database
TEST_DATABASE_URL = "postgresql://postgres:!Peewee38!@localhost:5645/test_intro_project"

@pytest.fixture
def app():
    # Set up the app with the test database
    app = create_app({"DATABASE_URI": TEST_DATABASE_URL, "TESTING": True})
    
    # Create tables in the test database
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    test_db = DBSession()

    # Populate test data
    password = "test"
    admin_user = User(email="admin@test.com", name="Admin", admin=True, password="dGVzdA==")  # Encrypted "test"
    test_user = User(email="user@test.com", name="Test User", admin=False, password="dGVzdA==")
    test_db.add_all([admin_user, test_user])
    test_db.commit()

    admin_id = admin_user.id
    test_user_id = test_user.id

    # Add posts and comments
    test_post = Post(contents="Test Post", user_id=admin_id, created_at=datetime.now())
    test_db.add(test_post)
    test_db.commit()

    test_post_id = test_post.id

    test_comment = Comment(contents="Test Comment", user_id=test_user_id, post_id=test_post_id, created_at=datetime.now())
    test_db.add(test_comment)
    test_db.commit()

    yield app

    # Clean up the database after tests
    Base.metadata.drop_all(engine)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_login(client):
    # Log in as admin
    client.post("/login", data={"email": "admin@test.com", "password": "test"})

@pytest.fixture
def user_login(client):
    # Log in as a non-admin user
    client.post("/login", data={"email": "user@test.com", "password": "test"})

def test_delete_post(client, admin_login):
    # Admin tries to delete a post
    response = client.post("/delete_post/1")
    assert response.status_code == 302  # Redirect after deletion

    # Check if post was deleted
    db = get_db_connection()
    post = db.query(Post).filter_by(id=1).first()
    assert post is None

def test_delete_comment(client, admin_login):
    # Admin tries to delete a comment
    response = client.post("/delete_comment/1")
    assert response.status_code == 302  # Redirect after deletion

    # Check if comment was deleted
    db = get_db_connection()
    comment = db.query(Comment).filter_by(id=1).first()
    assert comment is None

def test_non_admin_cannot_delete_post(client, user_login):
    # Non-admin tries to delete a post
    response = client.post("/delete_post/1")
    assert response.status_code == 302  # Redirect to home or login

    # Ensure post still exists
    db = get_db_connection()
    post = db.query(Post).filter_by(id=1).first()
    assert post is not None

def test_non_admin_cannot_delete_comment(client, user_login):
    # Non-admin tries to delete a comment
    response = client.post("/delete_comment/1")
    assert response.status_code == 302  # Redirect to home or login

    # Ensure comment still exists
    db = get_db_connection()
    comment = db.query(Comment).filter_by(id=1).first()
    assert comment is not None
