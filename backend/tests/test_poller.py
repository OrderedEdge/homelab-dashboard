from app.poller import DashboardCache, cache


def test_cache_initialises_empty():
    c = DashboardCache()
    assert c.fleet == {}
    assert c.hosts == {}
    assert c.services == []
    assert c.updated_at == ""


def test_global_cache_exists():
    assert isinstance(cache, DashboardCache)
