from app.tests.factory import user_payload
import pytest
from uuid import uuid4

@pytest.mark.parametrize("role", ["candidate", "recruiter", "admin"])
def test_create_company(client, auth_headers, role):
    identity=str(uuid4().hex)
    payload={
        "name": f"Company_{identity}",
        "description": f"Our company is the best",
        "website": f"{identity}.com",
        "location": "Gandhinagar",
        "domain": "Python",
        "company_size": 100
    }
    headers=auth_headers(role)
    response=client.post("/companies/", json=payload, headers=headers)
    assert response.status_code==201
    company_data=response.json()
    assert "id" in company_data
    assert "owner_id" in company_data

@pytest.mark.parametrize("role", ["candidate", "recruiter", "admin"])
def test_get_company_by_id(client, get_created_company, auth_headers, role):
    headers=auth_headers(role)
    company_id = get_created_company["id"]
    response = client.get(f"/companies/{company_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == company_id
    response = client.get("/companies/ssjk")
    assert response.status_code == 422

def test_update_company(client, auth_headers, get_created_company):
    company_id = get_created_company["id"]
    headers = auth_headers("admin")

    payload = {
        "name": f"NEWNAME_{uuid4()}",
        "description": f"Our company is the best, new one",
        "website": f"{uuid4()}.com",
        "location": "Gandhinagar",
        "domain": "Python",
        "company_size": 100
    }
    response = client.put(f"/companies/{company_id}", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Our company is the best, new one"
    assert data["company_size"] == 100

def test_delete_company(client, auth_headers, get_created_company):
    headers = auth_headers("admin")
    company_id = get_created_company["id"]
    response = client.delete(f"/companies/{company_id}", headers=headers)
    assert response.status_code == 204
    response = client.get(f"/companies/{company_id}")
    assert response.status_code == 404

def test_list_companies(client):
    response = client.get("/companies/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1