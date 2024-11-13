import psycopg2

def test_add_user(client, db_connection):
    # Define the data to send in the POST request
    new_user_data = {"name": "Test User", "email": "test@example.com"}
    
    # Simulate a POST request to the `/add_user` endpoint
    response = client.post("/add_user", json=new_user_data)
    
    # Check that the response status code is 201 (Created)
    assert response.status_code == 201

    # Parse the response JSON
    response_json = response.get_json()
    user_id = response_json["id"]

    # Verify that the user was actually added to the database
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
    user = cursor.fetchone()
    
    assert user is not None  # Ensure the user was added
    assert user[1] == "Test User"
    assert user[2] == "test@example.com"
    
    # Cleanup: remove the test user from the database
    cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
    db_connection.commit()
    cursor.close()
