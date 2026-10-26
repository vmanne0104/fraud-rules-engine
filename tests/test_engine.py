from fastapi.testclient import TestClient
from app.main import app
from app.engine import score_event

client = TestClient(app)

def test_low_risk_approved():
    r = score_event({"account_age_days": 900, "order_amount": 50})
    assert r["decision"] == "APPROVE" and r["score"] == 0

def test_sim_swap_plus_new_country_steps_up():
    r = score_event({"hours_since_sim_swap": 2, "new_country": True})
    assert r["score"] == 65 and r["decision"] == "STEP_UP_AUTH"

def test_stacked_signals_decline():
    r = score_event({"hours_since_sim_swap": 1, "account_age_days": 2,
                     "failed_otp": 4, "order_amount": 1500})
    assert r["decision"] == "DECLINE" and r["score"] == 100  # capped

def test_api_score():
    resp = client.post("/v1/score", json={"account_id": "A1", "hours_since_sim_swap": 3, "failed_otp": 3})
    assert resp.status_code == 200 and resp.json()["decision"] == "STEP_UP_AUTH"

def test_api_validation():
    assert client.post("/v1/score", json={"account_id": "A1", "failed_otp": -1}).status_code == 422
