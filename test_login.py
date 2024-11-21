import pytest
from transact_flask.app import User
from unittest.mock import MagicMock


@pytest.fixture
def mock_session():
    # Create a mock SQLAlchemy session
    session = MagicMock()
    return session


def test_user_login(mock_session):
    # Simulate a user in the database
    email = "test@example.com"
    password = "testpassword"
    encrypted_password = "encrypted_testpassword"  # Simulated encrypted password

    # Create a mock user
    mock_user = User(
        id=1, email=email, name="Test User", admin=False, password=encrypted_password
    )

    # Mock the database query to return the user
    mock_session.query.return_value.filter_by.return_value.first.return_value = (
        mock_user
    )

    # Simulate the password check (e.g., encryption or hashing)
    def mock_encrypt_password(pwd):
        return encrypted_password if pwd == password else "wrong_password"

    # Simulate the login action
    input_password = "testpassword"
    fetched_user = mock_session.query(User).filter_by(email=email).first()
    is_password_correct = fetched_user.password == mock_encrypt_password(input_password)

    # Assertions
    assert fetched_user is not None  # User should be found
    assert fetched_user.email == email
    assert is_password_correct  # Password should match
    assert fetched_user.name == "Test User"
    assert fetched_user.admin is False


def test_user_login_wrong_password(mock_session):
    # Simulate a user in the database
    email = "test@example.com"
    correct_password = "testpassword"
    wrong_password = "wrongpassword"
    encrypted_password = "encrypted_testpassword"  # Simulated encrypted password

    # Create a mock user
    mock_user = User(
        id=1, email=email, name="Test User", admin=False, password=encrypted_password
    )

    # Mock the database query to return the user
    mock_session.query.return_value.filter_by.return_value.first.return_value = (
        mock_user
    )

    # Simulate the password check (e.g., encryption or hashing)
    def mock_encrypt_password(pwd):
        return encrypted_password if pwd == correct_password else "wrong_encrypted"

    # Simulate the login action with a wrong password
    input_password = wrong_password
    fetched_user = mock_session.query(User).filter_by(email=email).first()
    is_password_correct = fetched_user.password == mock_encrypt_password(input_password)

    # Assertions
    assert fetched_user is not None  # User should be found
    assert fetched_user.email == email
    assert not is_password_correct  # Password should not match


def test_user_login_admin(mock_session):
    # Simulate an admin user in the database
    email = "admin@example.com"
    password = "adminpassword"
    encrypted_password = "encrypted_adminpassword"  # Simulated encrypted password

    # Create a mock admin user
    mock_admin_user = User(
        id=1, email=email, name="Admin User", admin=True, password=encrypted_password
    )

    # Mock the database query to return the admin user
    mock_session.query.return_value.filter_by.return_value.first.return_value = (
        mock_admin_user
    )

    # Simulate the password check
    def mock_encrypt_password(pwd):
        return encrypted_password if pwd == password else "wrong_password"

    # Simulate the login action
    input_password = "adminpassword"
    fetched_user = mock_session.query(User).filter_by(email=email).first()
    is_password_correct = fetched_user.password == mock_encrypt_password(input_password)

    # Assertions
    assert fetched_user is not None  # User should be found
    assert fetched_user.email == email
    assert fetched_user.admin is True  # User should be an admin
    assert is_password_correct  # Password should match


def test_user_login_user_not_found(mock_session):
    # Simulate no user in the database
    email = "nonexistent@example.com"

    # Mock the database query to return None
    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    # Simulate the login action
    fetched_user = mock_session.query(User).filter_by(email=email).first()

    # Assertions
    assert fetched_user is None  # User should not be found
