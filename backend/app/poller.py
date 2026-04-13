import asyncio
import logging
import time
from dataclasses import dataclass, field

import httpx

from app.config import settings
from app.prometheus import HOSTS, fetch_instant, fetch_range, fetch_targets
from app.services import list_services

logger = logging.getLogger(__name__)


@dataclass
class DashboardCache:
    fleet: dict = field(default_factory=dict)
    hosts: dict = field(default_factory=dict)
    services: list = field(default_factory=list)
    updated_at: str = ""


cache = DashboardCache()


async def poll_once():
    """Run one poll cycle: fetch all data and update the cache."""
    async with httpx.AsyncClient() as client:
        health_map = await fetch_targets(client)

        cpu_query = '100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
        host_cpu = await fetch_instant(client, cpu_query)

        ram_query = '100 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100)'
        host_ram = await fetch_instant(client, ram_query)

        disk_query = '100 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"} * 100)'
        host_disk = await fetch_instant(client, disk_query)

        sparkline_query = '100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
        cpu_sparklines = await fetch_range(client, sparkline_query, "1h", 7)

        ram_sparkline_query = '100 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100)'
        ram_sparklines = await fetch_range(client, ram_sparkline_query, "1h", 7)

    hosts = {}
    for name, ip in HOSTS.items():
        instance_9100 = f"{ip}:9100"
        hosts[name] = {
            "status": health_map.get(instance_9100, "unknown"),
            "cpu_pct": round(host_cpu.get(instance_9100, 0), 1),
            "ram_pct": round(host_ram.get(instance_9100, 0), 1),
            "disk_pct": round(host_disk.get(instance_9100, 0), 1),
            "cpu_sparkline": [round(v, 1) for v in cpu_sparklines.get(instance_9100, [])],
            "ram_sparkline": [round(v, 1) for v in ram_sparklines.get(instance_9100, [])],
        }

    services_raw = list_services()
    services_out = []
    up_count = 0
    for svc in services_raw:
        status = health_map.get(svc.instance, "unknown")
        if status == "up":
            up_count += 1
        cpu = host_cpu.get(svc.instance, None)
        services_out.append({
            **svc.model_dump(),
            "status": status,
            "cpu_pct": round(cpu, 1) if cpu is not None else None,
            "cpu_sparkline": [round(v, 1) for v in cpu_sparklines.get(svc.instance, [])],
        })

    total = len(services_raw)
    cache.fleet = {
        "uptime_pct": round(up_count / total * 100, 1) if total else 0,
        "total_services": total,
        "alerts": total - up_count,
        "hosts": len(HOSTS),
    }
    cache.hosts = hosts
    cache.services = services_out
    cache.updated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


async def poll_loop():
    """Background task: poll every N seconds."""
    while True:
        try:
            await poll_once()
            logger.info("Poll cycle complete: %d services", len(cache.services))
        except Exception as e:
            logger.exception("Poll error: %s", e)
        await asyncio.sleep(settings.poll_interval)
