# Homelab Dashboard

Showcase-quality infrastructure dashboard for a multi-host Proxmox homelab. Live metrics from Prometheus, service health monitoring, and one-click access to all services.

## Architecture

```
React/Vite (TypeScript + Tailwind) → FastAPI (Python 3.12) → Prometheus
```

- **Frontend:** React SPA with fleet overview, service cards with sparklines, host drill-down tabs, search and filtering
- **Backend:** FastAPI aggregates Prometheus, Docker, and service registry data on a 30-second poll cycle
- **MCP:** FastMCP tools for Claude Code integration (add/remove/update services)
- **Deploy:** Docker Compose (nginx + FastAPI) via GitHub Actions CI

## Features

- Fleet health summary (uptime %, service count, alerts)
- Quick-access bar for pinned services
- Filterable service grid with status dots and inline sparklines
- Host drill-down tabs (Cosmos, Zeus, NUC, Titan, Forge)
- Search by name, filter by host/status, sort by name/CT/status
- Docker container views per host
- MCP server for Claude Code management

## Stack

| Layer | Tech |
|---|---|
| Frontend | React 18, Vite, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python 3.12, FastMCP |
| Metrics | Prometheus |
| Deploy | Docker Compose, nginx, GitHub Actions |

## Quick Start

Development:
```bash
# Backend
cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000 &

# Frontend
cd frontend && npm install && npm run dev
```

Production:
```bash
docker compose up -d
```

## Infrastructure

Monitors 5 Proxmox hosts, 40+ containers, and 70+ services across:

| Host | Role |
|---|---|
| Cosmos | Primary Proxmox (18 CTs) |
| Zeus | Secondary Proxmox (9 CTs) |
| NUC | Tertiary Proxmox (10 CTs) |
| Titan | Bare-metal GPU/AI workstation |
| Forge | GCP cloud (web hosting) |

## Licence

MIT
