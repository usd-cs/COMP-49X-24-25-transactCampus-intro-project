# conftest.py
import pytest
import psycopg2
from transact_flask.app import create_app, get_db_connection

@pytest.fixture(scope="function")
def test_client():
    # Configure your application to use the test database
    app = create_app(test_config={
        "TESTING": True,
        "DATABASE": "intro_project_test"  # Test database name
    })

    # Seed the test database with sample data
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO "User" (email, name, admin, password) VALUES
        ('testuser@example.com', 'Test User', FALSE,'test_password'),
        ('adminuser@example.com', 'Admin User', TRUE, 'admin_password')
    """)
    conn.commit()

    yield app.test_client()  # Provide the test client to the tests

    # Teardown: Drop the test table after tests complete
    cursor.execute("DROP TABLE IF EXISTS \"User\";")
    conn.commit()
    conn.close()

