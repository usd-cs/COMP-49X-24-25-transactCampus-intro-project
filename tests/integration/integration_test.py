import pytest
from transact_flask import app 
import psycopg2
import os

@pytest.fixture
def app():
    app = app()
    app.config.update({
        "TESTING": True,
        # Add any other configuration needed for integration tests
    })
    yield app

@pytest.fixture
def db_connection():
    # Use the test database URI
    database_uri = os.getenv("TEST_DATABASE_URI", "postgresql://user:password@localhost/test_database")
    conn = psycopg2.connect(database_uri)
    yield conn
    
    # Cleanup
    conn.close()



@pytest.fixture
def client(app, db_connection):
    app.config["db_connection"] = db_connection
    return app.test_client()




