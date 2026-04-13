import json
import tempfile
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


def _with_temp_services(data: list[dict]):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(data, f)
    f.close()
    return patch("app.services.settings", services_file=f.name)


SEED = [{"name": "Grafana", "host": "cosmos", "ct": 117, "ip": "10.0.0.1",
         "instance": "10.0.0.1:3000", "category": "monitoring", "pinned": False}]


def test_list_services_api():
    with _with_temp_services(SEED):
        client = TestClient(app)
        resp = client.get("/api/services")
        assert resp.status_code == 200
        assert len(resp.json()) == 1


def test_add_service_api():
    with _with_temp_services([]):
        client = TestClient(app)
        resp = client.post("/api/services", json={
            "name": "New", "host": "zeus", "ct": 200, "ip": "10.0.0.2",
            "instance": "10.0.0.2:9100", "category": "infra",
        })
        assert resp.status_code == 201
        assert resp.json()["name"] == "New"


def test_add_duplicate_returns_409():
    with _with_temp_services(SEED):
        client = TestClient(app)
        resp = client.post("/api/services", json={
            "name": "Grafana", "host": "cosmos", "ct": 117, "ip": "10.0.0.1",
            "instance": "10.0.0.1:3000", "category": "monitoring",
        })
        assert resp.status_code == 409


def test_update_service_api():
    with _with_temp_services(SEED):
        client = TestClient(app)
        resp = client.patch("/api/services/Grafana", json={"pinned": True})
        assert resp.status_code == 200
        assert resp.json()["pinned"] is True


def test_delete_service_api():
    with _with_temp_services(SEED):
        client = TestClient(app)
        resp = client.delete("/api/services/Grafana")
        assert resp.status_code == 204


def test_delete_nonexistent_returns_404():
    with _with_temp_services([]):
        client = TestClient(app)
        resp = client.delete("/api/services/Ghost")
        assert resp.status_code == 404
