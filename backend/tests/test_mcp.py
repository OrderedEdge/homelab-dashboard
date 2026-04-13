import json
import tempfile
from unittest.mock import patch

from app.mcp_tools import add_service, get_dashboard_status, list_services, remove_service


def _with_temp_services(data: list[dict]):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(data, f)
    f.close()
    return patch("app.services.settings", services_file=f.name)


SEED = [{"name": "Grafana", "host": "cosmos", "ct": 117, "ip": "10.0.0.1",
         "instance": "10.0.0.1:3000", "category": "monitoring", "pinned": False}]


def test_mcp_list_services():
    with _with_temp_services(SEED):
        result = list_services()
        assert "1 services:" in result
        assert "Grafana" in result


def test_mcp_add_service():
    with _with_temp_services([]):
        result = add_service(
            name="Test", instance="10.0.0.1:9100", ct=100, ip="10.0.0.1",
            host="cosmos", category="monitoring",
        )
        assert "Added 'Test'" in result


def test_mcp_remove_service():
    with _with_temp_services(SEED):
        result = remove_service("Grafana")
        assert "Removed 'Grafana'" in result


def test_mcp_get_status_empty():
    result = get_dashboard_status()
    assert "0/0" in result or "No services" in result
