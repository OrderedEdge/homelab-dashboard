import httpx

from app.config import settings

HOSTS = {
    "cosmos": "192.168.10.50",
    "zeus": "192.168.10.60",
    "nuc": "192.168.10.77",
    "titan": "192.168.10.117",
    "forge": "34.38.78.238",
}


async def fetch_targets(client: httpx.AsyncClient) -> dict[str, str]:
    """Fetch Prometheus targets and return {instance: health} map."""
    try:
        resp = await client.get(f"{settings.prometheus_url}/api/v1/targets", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return {
            t["labels"].get("instance", ""): t["health"]
            for t in data["data"]["activeTargets"]
        }
    except Exception:
        return {}


async def fetch_instant(client: httpx.AsyncClient, query: str) -> dict[str, float]:
    """Run a Prometheus instant query and return {metric_label: value} map."""
    try:
        resp = await client.get(
            f"{settings.prometheus_url}/api/v1/query",
            params={"query": query},
            timeout=5,
        )
        resp.raise_for_status()
        results = resp.json()["data"]["result"]
        return {
            r["metric"].get("instance", ""): float(r["value"][1])
            for r in results
        }
    except Exception:
        return {}


async def fetch_range(
    client: httpx.AsyncClient, query: str, duration: str = "1h", points: int = 7
) -> dict[str, list[float]]:
    """Run a Prometheus range query and downsample to N points."""
    import time

    end = int(time.time())
    duration_secs = {"1h": 3600, "6h": 21600, "24h": 86400}.get(duration, 3600)
    start = end - duration_secs
    step = duration_secs // points

    try:
        resp = await client.get(
            f"{settings.prometheus_url}/api/v1/query_range",
            params={"query": query, "start": start, "end": end, "step": step},
            timeout=10,
        )
        resp.raise_for_status()
        results = resp.json()["data"]["result"]
        out = {}
        for r in results:
            instance = r["metric"].get("instance", "")
            values = [float(v[1]) for v in r["values"]]
            if len(values) > points:
                step_size = len(values) / points
                values = [values[int(i * step_size)] for i in range(points)]
            out[instance] = values
        return out
    except Exception:
        return {}
