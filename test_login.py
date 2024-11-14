import pytest
from flask import session
from transact_flask.app import encrypt_password



def test_valid_user_login(test_client):
    response = test_client.post(
        "/login",
        data={"email": "testuser@example.com", "password": "test_password"},
        follow_redirects=False  # Important: set to False to check redirection location without following it
    )
    # Check that it redirects to the 'home' route
    assert response.status_code == 302  # HTTP status code for redirection
    assert response.headers["Location"].endswith("/")  # Expected redirect location for regular users



def test_admin_user_login(test_client):
    response = test_client.post(
        "/login",
        data={"email": "adminuser@example.com", "password": "admin_password"},
        follow_redirects=False
    )
    # Check that it redirects to the 'admin' route
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/admin")  # Expected redirect location for admin users



def test_invalid_password(test_client):
    response = test_client.post(
        "/login",
        data={"email": "testuser@example.com", "password": "wrong_password"},
        follow_redirects=False
    )
    # Check that it redirects back to the login route on failure
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")  # Expected redirect location for failed login



def test_nonexistent_user(test_client):
    response = test_client.post(
        "/login",
        data={"email": "nonexistent@example.com", "password": "some_password"},
        follow_redirects=False
    )
    # Check that it redirects back to the login route for non-existent user
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")  # Expected redirect location for non-existent user
