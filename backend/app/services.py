import json
from pathlib import Path

from app.config import settings
from app.models import Service, ServiceUpdate


def _file() -> Path:
    return Path(settings.services_file)


def list_services() -> list[Service]:
    path = _file()
    if not path.exists():
        return []
    data = json.loads(path.read_text())
    return [Service(**s) for s in data]


def get_service(name: str) -> Service | None:
    for s in list_services():
        if s.name == name:
            return s
    return None


def add_service(service: Service) -> Service:
    services = list_services()
    if any(s.name == service.name for s in services):
        raise ValueError(f"Service '{service.name}' already exists")
    services.append(service)
    _write(services)
    return service


def update_service(name: str, update: ServiceUpdate) -> Service:
    services = list_services()
    for i, s in enumerate(services):
        if s.name == name:
            updated = s.model_copy(update=update.model_dump(exclude_none=True))
            if update.name and update.name != name:
                updated.name = update.name
            services[i] = updated
            _write(services)
            return updated
    raise ValueError(f"Service '{name}' not found")


def remove_service(name: str) -> bool:
    services = list_services()
    filtered = [s for s in services if s.name != name]
    if len(filtered) == len(services):
        raise ValueError(f"Service '{name}' not found")
    _write(filtered)
    return True


def _write(services: list[Service]) -> None:
    data = [s.model_dump() for s in services]
    _file().write_text(json.dumps(data, indent=2) + "\n")
