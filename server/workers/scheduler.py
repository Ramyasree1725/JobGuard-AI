"""
Aetheris Server Engine: Background Async Task Scheduler & Simulation Loop Worker
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import asyncio
import time
from typing import Dict, Any, Optional
from core.simulation.engine import SimulationEngine
from server.websocket.hub import ws_hub
from server.config import config


class BackgroundSimulationWorker:
    """
    Asynchronous 60Hz Simulation Background Loop.
    Steps the physical and multi-agent simulation engine and streams frames to WebSockets.
    """
    def __init__(self) -> None:
        self.sim_engine = SimulationEngine(fps=config.SIMULATION_TICK_RATE_HZ)
        self.is_running = False
        self.task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        if self.is_running:
            return
        self.is_running = True
        self.task = asyncio.create_task(self._run_loop())

    async def stop(self) -> None:
        self.is_running = False
        if self.task is not None:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            self.task = None

    async def _run_loop(self) -> None:
        dt = 1.0 / float(config.SIMULATION_TICK_RATE_HZ)
        last_broadcast = time.time()

        while self.is_running:
            start_t = time.time()
            telemetry = self.sim_engine.step()

            # Throttle WebSocket broadcasts to ~30Hz for bandwidth efficiency
            now = time.time()
            if now - last_broadcast >= config.WEBSOCKET_BROADCAST_INTERVAL_SEC:
                last_broadcast = now
                await ws_hub.broadcast({
                    "event": "TELEMETRY_FRAME",
                    "data": telemetry
                })

            elapsed = time.time() - start_t
            sleep_time = max(0.001, dt - elapsed)
            await asyncio.sleep(sleep_time)


sim_worker = BackgroundSimulationWorker()
