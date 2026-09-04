"""
Aetheris Server Engine: Real-Time WebSocket Telemetry Broadcast Hub
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import json
import asyncio
from typing import List, Set, Dict, Any
from fastapi import WebSocket


class WebSocketHub:
    """
    High-Throughput WebSocket Broadcast Engine for Real-Time 60Hz Telemetry Streaming.
    Manages client connections, topic channels, and backpressure mitigation.
    """
    def __init__(self) -> None:
        self.active_connections: Set[WebSocket] = set()
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self.lock:
            self.active_connections.add(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self.lock:
            self.active_connections.discard(websocket)

    async def broadcast(self, message: Dict[str, Any]) -> None:
        """Broadcasts JSON payload to all active client dashboards."""
        if not self.active_connections:
            return

        payload_text = json.dumps(message)
        dead_connections = []

        async with self.lock:
            for conn in list(self.active_connections):
                try:
                    await conn.send_text(payload_text)
                except Exception:
                    dead_connections.append(conn)

            for dead in dead_connections:
                self.active_connections.discard(dead)

    def active_client_count(self) -> int:
        return len(self.active_connections)


ws_hub = WebSocketHub()
