from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings


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
