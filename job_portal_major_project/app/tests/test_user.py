from app.tests.factory import user_payload

def test_get_user(client, auth_headers):
    headers = auth_headers("candidate")
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "email" in data
    assert "user_name" in data
    assert "role" in data
    response = client.get("/users/me")
    assert response.status_code == 401

def test_list_users(client, auth_headers):
    headers = auth_headers("admin")
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    headers = auth_headers("candidate")
    response = client.get("/users/", headers=headers)
    assert response.status_code == 403


def test_update_user(client, auth_headers):
    payload={
        "user_name": "ABC",
        "email": "abc@pytest.com",
        "password": "abc@123pytest",
        "role": "recruiter",
        "current_organization": None
    }
    headers = auth_headers("candidate")
    response = client.put("/users/me", json=payload, headers=headers)
    assert response.status_code == 200

def test_delete_user(client, auth_headers):
    headers = auth_headers("candidate")
    response=client.delete("/users/me", headers=headers)
    assert response.status_code==204

