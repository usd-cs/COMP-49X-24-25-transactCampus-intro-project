def test_home(client):
    response = client.get("/home")  
    assert response.status_code == 200
   

def test_login(client):
    response = client.get("/login") 
    assert response.status_code == 200

def test_comment(client):
    response = client.get("/comment")  
    assert response.status_code == 200
