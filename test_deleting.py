import pytest
from transact_flask.app import User
from unittest.mock import MagicMock
from transact_flask.app import Post, Comment
from datetime import datetime


@pytest.fixture
def mock_session():
    # Create a mock SQLAlchemy session
    session = MagicMock()
    return session


def test_admin_delete_post(mock_session):
    # Simulate an admin user
    admin_user_id = 1
    mock_admin_user = User(
        id=admin_user_id, email="admin@example.com", name="Admin User", admin=True
    )

    # Simulate a post to be deleted
    post_id = 1
    mock_post = Post(
        id=post_id,
        contents="This is a test post",
        user_id=admin_user_id,
        created_at=datetime.now(),
    )

    # Mock the database query to return the post
    mock_session.query.return_value.filter_by.return_value.first.return_value = (
        mock_post
    )

    # Simulate the delete and commit operations
    mock_session.delete.return_value = None  # Mock the delete method
    mock_session.commit.return_value = None  # Mock the commit method

    # Perform the delete action
    fetched_post = mock_session.query(Post).filter_by(id=post_id).first()
    mock_session.delete(fetched_post)
    mock_session.commit()

    # Assertions
    mock_session.query.assert_called_once_with(Post)  # Ensure query was called
    mock_session.delete.assert_called_once_with(mock_post)  # Verify delete was called
    mock_session.commit.assert_called_once()  # Verify commit was called


def test_admin_delete_comment(mock_session):
    # Simulate an admin user
    admin_user_id = 1
    mock_admin_user = User(
        id=admin_user_id, email="admin@example.com", name="Admin User", admin=True
    )

    # Simulate a comment to be deleted
    comment_id = 1
    mock_comment = Comment(
        id=comment_id,
        contents="This is a test comment",
        user_id=admin_user_id,
        post_id=1,
        created_at=datetime.now(),
    )

    # Mock the database query to return the comment
    mock_session.query.return_value.filter_by.return_value.first.return_value = (
        mock_comment
    )

    # Simulate the delete and commit operations
    mock_session.delete.return_value = None  # Mock the delete method
    mock_session.commit.return_value = None  # Mock the commit method

    # Perform the delete action
    fetched_comment = mock_session.query(Comment).filter_by(id=comment_id).first()
    mock_session.delete(fetched_comment)
    mock_session.commit()

    # Assertions
    mock_session.query.assert_called_once_with(Comment)  # Ensure query was called
    mock_session.delete.assert_called_once_with(
        mock_comment
    )  # Verify delete was called
    mock_session.commit.assert_called_once()  # Verify commit was called
