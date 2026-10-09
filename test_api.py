from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_empty_question_rejected():
    r = client.post("/ask", json={"question": "   "})
    assert r.status_code == 400


def test_ask_returns_answer(monkeypatch):
    monkeypatch.setattr("api.ask", lambda q: "stub answer")
    monkeypatch.setattr("api.log_query", lambda q, a: None)
    r = client.post("/ask", json={"question": "What is SPF?"})
    assert r.status_code == 200
    assert r.json()["answer"] == "stub answer"