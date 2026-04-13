from typing import Optional

from fastmcp import FastMCP

from app.models import Service, ServiceUpdate
from app import services as svc
from app.poller import cache

mcp = FastMCP(
    "Cosmos Dashboard",
    instructions=(
        "MCP server for the Cosmos homelab dashboard. "
        "Use these tools to add, remove, or update services shown on the dashboard. "
        "After making changes, remind the user to update Notion."
    ),
)


def list_services() -> str:
    """List all services currently displayed on the dashboard."""
    services = svc.list_services()
    lines = []
    for s in services:
        lines.append(
            f"CT {s.ct:>3}  {s.name:25s}  {s.ip:18s}  host={s.host}  cat={s.category}  pinned={s.pinned}"
        )
    return f"{len(services)} services:\n" + "\n".join(lines)


def add_service(
    name: str,
    instance: str,
    ct: int,
    ip: str,
    host: str,
    category: str,
    link: Optional[str] = None,
    link_label: Optional[str] = None,
    pinned: bool = False,
) -> str:
    """Add a new service to the dashboard.

    Args:
        name: Display name (e.g. 'Grafana')
        instance: Prometheus instance label (ip:port)
        ct: Proxmox CT/VM ID
        ip: IP address of the container
        host: Host name (cosmos, zeus, nuc, titan, forge)
        category: One of: monitoring, security, media, network, storage, web, infra, iot
        link: Optional URL to the service UI
        link_label: Optional label for the link
        pinned: Show in quick-access row (default False)
    """
    service = Service(
        name=name, instance=instance, ct=ct, ip=ip, host=host,
        category=category, link=link, linkLabel=link_label, pinned=pinned,
    )
    try:
        svc.add_service(service)
        return f"Added '{name}' (CT {ct}, {ip}, host={host}). Visible on next poll cycle."
    except ValueError as e:
        return f"Error: {e}"


def remove_service(name: str) -> str:
    """Remove a service from the dashboard by exact name."""
    try:
        svc.remove_service(name)
        remaining = len(svc.list_services())
        return f"Removed '{name}'. {remaining} services remain."
    except ValueError as e:
        return f"Error: {e}"


def update_service(
    name: str,
    new_name: Optional[str] = None,
    instance: Optional[str] = None,
    ct: Optional[int] = None,
    ip: Optional[str] = None,
    host: Optional[str] = None,
    link: Optional[str] = None,
    link_label: Optional[str] = None,
    category: Optional[str] = None,
    pinned: Optional[bool] = None,
) -> str:
    """Update an existing service on the dashboard."""
    update = ServiceUpdate(
        name=new_name, instance=instance, ct=ct, ip=ip, host=host,
        link=link, linkLabel=link_label, category=category, pinned=pinned,
    )
    try:
        result = svc.update_service(name, update)
        return f"Updated '{result.name}'. Visible on next poll cycle."
    except ValueError as e:
        return f"Error: {e}"


def get_dashboard_status() -> str:
    """Get full dashboard state — all services with Prometheus health status."""
    lines = []
    up_count = 0
    for s in cache.services:
        status = s.get("status", "unknown")
        if status == "up":
            up_count += 1
        lines.append(
            f"CT {s.get('ct', '?'):>3}  {s['name']:25s}  {s['ip']:18s}  "
            f"health={status:8s}  host={s.get('host', '?')}"
        )

    total = len(cache.services)
    header = f"Dashboard: {up_count}/{total} services UP\n"
    header += "-" * 80 + "\n"
    return header + "\n".join(lines) if lines else "No services configured."


# Register plain functions as MCP tools
mcp.tool()(list_services)
mcp.tool()(add_service)
mcp.tool()(remove_service)
mcp.tool()(update_service)
mcp.tool()(get_dashboard_status)
