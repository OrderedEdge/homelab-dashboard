import httpx
import pytest


from app.prometheus import fetch_targets


@pytest.fixture
def mock_targets_response():
    return {
        "data": {
            "activeTargets": [
                {"labels": {"instance": "10.0.0.1:9100"}, "health": "up"},
                {"labels": {"instance": "10.0.0.2:9100"}, "health": "down"},
            ]
        }
    }


async def test_fetch_targets(mock_targets_response, monkeypatch):
    async def mock_handler(request):
        return httpx.Response(200, json=mock_targets_response)

    transport = httpx.MockTransport(mock_handler)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        monkeypatch.setattr("app.prometheus.settings", type("S", (), {"prometheus_url": "http://test"})())
        result = await fetch_targets(client)
    assert result["10.0.0.1:9100"] == "up"
    assert result["10.0.0.2:9100"] == "down"


async def test_fetch_targets_handles_error(monkeypatch):
    async def mock_handler(request):
        return httpx.Response(500)

    transport = httpx.MockTransport(mock_handler)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        monkeypatch.setattr("app.prometheus.settings", type("S", (), {"prometheus_url": "http://test"})())
        result = await fetch_targets(client)
    assert result == {}
