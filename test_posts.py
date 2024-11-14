import pytest
from flask import session
from transact_flask.app import create_app, get_db_connection


def test_post(test_client):
    # Send a POST request to the add_post route
    response = test_client.post(
        "/add_post", data={"content": "This is a test post"}, follow_redirects=False
    )

    # Check for a redirect response
    assert response.status_code == 302
    assert response.headers["Location"].endswith(
        "/login"
    )  # Redirects to home for regular users


def test_add_comment_route(test_client):
    # Simulate adding a post directly into the session to comment on

    # Send a POST request to add a comment to the mock post
    response = test_client.post(
        "/add_comment",
        data={"content": "This is a test comment", "post_id": 1},
        follow_redirects=False,
    )

    # Check for a redirect response
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")  # Expected redirect location
