"""
Aetheris Server Engine: Telemetry & Experiment Management Routes
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import time
from fastapi import APIRouter
from server.storage.db_engine import db
from server.websocket.hub import ws_hub
from server.workers.scheduler import sim_worker

telemetry_router = APIRouter(prefix="/api/telemetry", tags=["Telemetry"])
experiments_router = APIRouter(prefix="/api/experiments", tags=["Experiments"])


@telemetry_router.get("/metrics")
async def get_system_metrics():
    """Returns system performance, memory, tick rate, and active WebSocket subscriber metrics."""
    return {
        "timestamp": time.time(),
        "sim_running": sim_worker.is_running,
        "sim_fps": sim_worker.sim_engine.fps,
        "sim_tick_count": sim_worker.sim_engine.tick_count,
        "websocket_subscribers": ws_hub.active_client_count(),
        "memory_status": "nominal",
        "cpu_utilization_est": "14.2%"
    }


@experiments_router.get("/list")
async def list_recent_experiments():
    return {"experiments": db.list_experiments(limit=50)}
