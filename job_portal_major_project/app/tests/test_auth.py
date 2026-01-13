from app.tests.factory import user_payload

def test_register(client):
    payload=user_payload()
    response=client.post("/auth/register", json=payload)
    assert response.status_code==200
    return response.json()

def test_login(client):
    reg_payload=user_payload()
    reg_resp=client.post("/auth/register", json=reg_payload)
    reg_data=reg_resp.json()
    payload=user_payload(uname=reg_data["user_name"], email=reg_data["email"], role=reg_data["role"])
    response=client.post("/auth/login", json=payload)
    assert response.status_code==200
    tokens=response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"]=="bearer"
    dirty_payload=user_payload(uname=reg_data["user_name"], email=reg_data["email"], password="InvalidPassword", role=reg_data["role"])
    response=client.post("/auth/login", json=dirty_payload)
    assert response.status_code==401

def test_refresh_token(client, login_and_get_tokens):
    tkns=login_and_get_tokens()
    refresh_tkn=tkns["refresh_token"]
    response=client.post("/auth/refresh", json={"refresh_token": refresh_tkn})
    assert response.status_code==200
