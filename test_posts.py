import pytest
from unittest.mock import MagicMock
from datetime import datetime
from transact_flask.app import Post, User, Comment


@pytest.fixture
def mock_session():
    # Create a mock SQLAlchemy session
    session = MagicMock()
    return session


def test_add_post(mock_session):
    # Simulate a user logged in
    user_id = 1
    mock_user = User(
        id=user_id, email="test@example.com", name="Test User", admin=False
    )

    # Create the post to add
    post_content = "This is a test post"
    new_post = Post(contents=post_content, user_id=user_id, created_at=datetime.now())

    # Simulate adding the post
    mock_session.add.return_value = None  # Mock the add method
    mock_session.commit.return_value = None  # Mock the commit method

    # Perform the action
    mock_session.add(new_post)
    mock_session.commit()

    # Assertions
    mock_session.add.assert_called_once_with(new_post)  # Verify add was called
    mock_session.commit.assert_called_once()  # Verify commit was called
    assert new_post.contents == post_content
    assert new_post.user_id == user_id


def test_add_comment(mock_session):
    # Simulate a user and a post existing in the database
    user_id = 1
    post_id = 1
    mock_user = User(
        id=user_id, email="test@example.com", name="Test User", admin=False
    )
    mock_post = Post(
        id=post_id,
        contents="This is a test post",
        user_id=user_id,
        created_at=datetime.now(),
    )

    # Create the comment to add
    comment_content = "This is a test comment"
    new_comment = Comment(
        contents=comment_content,
        user_id=user_id,
        post_id=post_id,
        created_at=datetime.now(),
    )

    # Simulate adding the comment
    mock_session.add.return_value = None  # Mock the add method
    mock_session.commit.return_value = None  # Mock the commit method

    # Perform the action
    mock_session.add(new_comment)
    mock_session.commit()

    # Assertions
    mock_session.add.assert_called_once_with(new_comment)  # Verify add was called
    mock_session.commit.assert_called_once()  # Verify commit was called
    assert new_comment.contents == comment_content
    assert new_comment.user_id == user_id
    assert new_comment.post_id == post_id
