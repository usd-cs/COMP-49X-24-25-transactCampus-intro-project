import pytest
import psycopg2
from transact_flask.app import create_app, encrypt_password,get_db_connection

@pytest.fixture(scope="function")
def test_client():
    # Configure your application to use the test database
    app = create_app(test_config={
        "TESTING": True,
    })

    # Directly assign the test database connection to the app config
    conn = get_db_connection()

    cursor = conn.cursor()
    
    password1 = encrypt_password('test_password')
    password2 = encrypt_password('admin_password')

    cursor.execute("""
        INSERT INTO "User" (email, name, admin, password) VALUES
        ('testuser@example.com', 'Test User', FALSE, %s),
        ('adminuser@example.com', 'Admin User', TRUE, %s)
    """, (password1, password2))
    conn.commit()

    yield app.test_client()  # Provide the test client to the tests

    # Teardown: Truncate the User table after tests complete
    cursor.execute("TRUNCATE TABLE \"User\" RESTART IDENTITY CASCADE;")
    conn.commit()
    conn.close()

