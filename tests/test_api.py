from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_chat():
    r = client.post("/chat", json={"query":"What documents are required to change a contract?","provider":"mock","top_k":3})
    assert r.status_code == 200
    data = r.json()
    assert data["route"] == "rag_answer"
    assert data["citations"]
