def test_home(client):
    response = client.get("/home")  # Replace with an actual endpoint
    assert response.status_code == 200
    # Add other assertions as needed

def test_login(client):
    response = client.get("/login")  # Replace with an actual endpoint
    assert response.status_code == 200

def test_comment(client):
    response = client.get("/comment")  # Replace with an actual endpoint
    assert response.status_code == 200
