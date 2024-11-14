# test_login.py
import pytest
from flask import session
from transact_flask.app import encrypt_password

def test_login_success(test_client):
    # Simulate a successful login with the test user's credentials
    response = test_client.post("/login", data={
        "email": "testuser@example.com",
        "password": "test_password"
    }, follow_redirects=True)

    # Verify that the login redirects to the home page
    assert response.status_code == 200  # or the status code for the redirected route (e.g., 302 for redirects)
    assert b"Welcome" in response.data  # Verify part of the home page's welcome message is present

    # Check if session variables are set correctly
    with test_client.session_transaction() as session_data:
        assert session_data.get("user_id") is not None
        assert session_data.get("email") == "testuser@example.com"
        assert session_data.get("name") == "Test User"
        assert session_data.get("admin") is False

def test_login_failure(test_client):
    # Simulate a failed login attempt with incorrect password
    response = test_client.post("/login", data={
        "email": "testuser@example.com",
        "password": "wrong_password"
    })

    # Verify redirection back to the login page on failure
    assert response.status_code == 302  # Redirection status code
    assert b"Incorrect login" in response.data  # Assuming there's a login error message

def test_admin_login_redirect(test_client):
    # Simulate a successful login as an admin user
    response = test_client.post("/login", data={
        "email": "adminuser@example.com",
        "password": "admin_password"
    }, follow_redirects=True)

    # Verify redirection to the admin page
    assert response.status_code == 200
    assert b"Admin Dashboard" in response.data  # Part of the admin page content

    # Verify admin session variables
    with test_client.session_transaction() as session_data:
        assert session_data.get("admin") is True