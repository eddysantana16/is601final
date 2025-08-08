from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

client = TestClient(app)

def _register_and_login(email="int1@example.com", username="int1", password="pass12345"):
    client.post("/api/register", json={"username": username, "email": email, "password": password})
    r = client.post("/api/login", json={"email": email, "password": password})
    token = r.headers.get("X-Access-Token")
    assert token, "Expected X-Access-Token header on login"
    return {"Authorization": f"Bearer {token}"}

def test_full_flow_auth_history_summary():
    headers = _register_and_login()

    # Create
    r = client.post("/api/calculations/", json={"operation":"add","operand1":10,"operand2":5}, headers=headers)
    assert r.status_code == 201
    created = r.json()
    assert created["result"] == 15
    calc_id = created["id"]

    # List (filter)
    r = client.get("/api/calculations?op=add&limit=10&offset=0", headers=headers)
    assert r.status_code == 200
    rows = r.json()
    assert any(row["id"] == calc_id for row in rows)

    # Get one
    r = client.get(f"/api/calculations/{calc_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["id"] == calc_id

    # Update (recompute)
    r = client.put(f"/api/calculations/{calc_id}", json={"operation":"power","operand1":2,"operand2":3}, headers=headers)
    assert r.status_code == 200
    assert r.json()["result"] == 8

    # Summary
    r = client.get("/api/calculations/reports/summary", headers=headers)
    assert r.status_code == 200
    summary = r.json()
    assert summary["total_calculations"] >= 1
    assert "by_operation" in summary

    # Delete
    r = client.delete(f"/api/calculations/{calc_id}", headers=headers)
    assert r.status_code in (200, 204)
