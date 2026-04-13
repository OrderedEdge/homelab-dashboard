from typing import Optional

from pydantic import BaseModel


class Service(BaseModel):
    name: str
    host: str
    ct: int
    ip: str
    instance: str
    link: Optional[str] = None
    linkLabel: Optional[str] = None
    category: str
    pinned: bool = False


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    host: Optional[str] = None
    ct: Optional[int] = None
    ip: Optional[str] = None
    instance: Optional[str] = None
    link: Optional[str] = None
    linkLabel: Optional[str] = None
    category: Optional[str] = None
    pinned: Optional[bool] = None


class ServiceWithStatus(Service):
    status: str = "unknown"
    cpu_pct: Optional[float] = None
    ram_mb: Optional[float] = None
    cpu_sparkline: list[float] = []
