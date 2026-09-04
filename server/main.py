"""
Aetheris Server Engine: Master FastAPI Application & WebSocket Entrypoint
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from server.config import config
from server.websocket.hub import ws_hub
from server.workers.scheduler import sim_worker
from server.routes.simulations import router as sim_router
from server.routes.optimizations import router as opt_router
from server.routes.nlp_kg import (
    vision_router, nlp_router, kg_router, rec_router, consensus_router
)
from server.routes.telemetry import telemetry_router, experiments_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start background simulation worker
    await sim_worker.start()
    yield
    # Shutdown: Stop worker cleanly
    await sim_worker.stop()


app = FastAPI(
    title=config.APP_NAME,
    version=config.VERSION,
    description="Enterprise Multi-Disciplinary Autonomous Research & Simulation Web Platform",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(sim_router)
app.include_router(opt_router)
app.include_router(vision_router)
app.include_router(nlp_router)
app.include_router(kg_router)
app.include_router(rec_router)
app.include_router(consensus_router)
app.include_router(telemetry_router)
app.include_router(experiments_router)


# Real-time WebSocket Endpoint
@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    await ws_hub.connect(websocket)
    try:
        while True:
            # Keep-alive receive
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        await ws_hub.disconnect(websocket)
    except Exception:
        await ws_hub.disconnect(websocket)


@app.get("/")
async def root():
    return {
        "platform": config.APP_NAME,
        "version": config.VERSION,
        "status": "ONLINE",
        "docs_url": "/docs",
        "websocket_url": "/ws/telemetry"
    }
