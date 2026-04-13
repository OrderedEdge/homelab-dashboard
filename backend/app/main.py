from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.config import settings
from app.models import Service, ServiceUpdate
from app import services as svc


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Cosmos Dashboard API", lifespan=lifespan)


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "prometheus_url": settings.prometheus_url,
        "poll_interval": settings.poll_interval,
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
