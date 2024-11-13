import psycopg2

def test_insert_user(client, db_connection):
    # Insert a new user into the database
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;", ("Test User", "test@example.com"))
    user_id = cursor.fetchone()[0]
    db_connection.commit()
    
    # Verify the user was added
    cursor.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
    user = cursor.fetchone()
    assert user is not None
    assert user[1] == "Test User"
    assert user[2] == "test@example.com"
    
    # Cleanup
    cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
    db_connection.commit()
    cursor.close()
