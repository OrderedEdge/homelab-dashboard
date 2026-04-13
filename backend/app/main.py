import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.config import settings
from app.models import Service, ServiceUpdate
from app import services as svc
from app.poller import cache, poll_loop


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(poll_loop())
    yield
    task.cancel()


app = FastAPI(title="Cosmos Dashboard API", lifespan=lifespan)


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "prometheus_url": settings.prometheus_url,
        "poll_interval": settings.poll_interval,
    }


@app.get("/api/status")
async def api_status():
    return {
        "fleet": cache.fleet,
        "hosts": cache.hosts,
        "services": cache.services,
        "updated_at": cache.updated_at,
    }


@app.get("/api/host/{name}")
async def api_host(name: str):
    if name not in cache.hosts:
        raise HTTPException(status_code=404, detail=f"Host '{name}' not found")
    host_services = [s for s in cache.services if s.get("host") == name]
    return {
        "host": cache.hosts[name],
        "services": host_services,
    }


@app.get("/api/services")
async def api_list_services():
    return svc.list_services()


@app.post("/api/services", status_code=201)
async def api_add_service(service: Service):
    try:
        return svc.add_service(service)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.patch("/api/services/{name}")
async def api_update_service(name: str, update: ServiceUpdate):
    try:
        return svc.update_service(name, update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/api/services/{name}", status_code=204)
async def api_remove_service(name: str):
    try:
        svc.remove_service(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
