from fastapi.testclient import TestClient

from costengine.api import app
from costengine.generate import demo

client = TestClient(app)


def test_estimate_endpoint():
    response = client.post("/estimate", json=demo())
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    assert data["audit"]
    assert data["project_id"] == "P-100"


def test_tracking_endpoint():
    response = client.post("/cost-tracking", json={"budget": 1000, "committed": 400, "actual": 300, "percent_complete": 40})
    assert response.status_code == 200
    assert response.json()["forecast_at_completion"] == 750.0
