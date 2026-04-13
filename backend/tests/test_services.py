import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from app.models import Service, ServiceUpdate
from app.services import add_service, get_service, list_services, remove_service, update_service


def _temp_services(data: list[dict]):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(data, f)
    f.close()
    return patch("app.services.settings", services_file=f.name)


def test_list_services_empty():
    with _temp_services([]):
        assert list_services() == []


def test_add_and_list_service():
    with _temp_services([]):
        svc = Service(
            name="Test", host="cosmos", ct=100, ip="10.0.0.1",
            instance="10.0.0.1:9100", category="monitoring",
        )
        add_service(svc)
        result = list_services()
        assert len(result) == 1
        assert result[0].name == "Test"


def test_add_duplicate_raises():
    seed = [{"name": "Test", "host": "cosmos", "ct": 100, "ip": "10.0.0.1",
             "instance": "10.0.0.1:9100", "category": "monitoring", "pinned": False}]
    with _temp_services(seed):
        with pytest.raises(ValueError, match="already exists"):
            add_service(Service(
                name="Test", host="cosmos", ct=100, ip="10.0.0.1",
                instance="10.0.0.1:9100", category="monitoring",
            ))


def test_get_service():
    seed = [{"name": "Grafana", "host": "cosmos", "ct": 117, "ip": "10.0.0.1",
             "instance": "10.0.0.1:3000", "category": "monitoring", "pinned": True}]
    with _temp_services(seed):
        svc = get_service("Grafana")
        assert svc is not None
        assert svc.ct == 117
        assert get_service("Nonexistent") is None


def test_update_service():
    seed = [{"name": "Grafana", "host": "cosmos", "ct": 117, "ip": "10.0.0.1",
             "instance": "10.0.0.1:3000", "category": "monitoring", "pinned": False}]
    with _temp_services(seed):
        updated = update_service("Grafana", ServiceUpdate(pinned=True, category="infra"))
        assert updated.pinned is True
        assert updated.category == "infra"


def test_remove_service():
    seed = [{"name": "Grafana", "host": "cosmos", "ct": 117, "ip": "10.0.0.1",
             "instance": "10.0.0.1:3000", "category": "monitoring", "pinned": False}]
    with _temp_services(seed):
        remove_service("Grafana")
        assert list_services() == []


def test_remove_nonexistent_raises():
    with _temp_services([]):
        with pytest.raises(ValueError, match="not found"):
            remove_service("Ghost")
