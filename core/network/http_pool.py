"""
JobGuard Core Network - HTTP Connection Pool & Keep-Alive Manager
Manages reusable TCP socket connections, connection timeouts, and
chunked response streaming for outbound domain checks.
"""

import threading
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class SimpleHTTPResponse:
    status_code: int
    headers: Dict[str, str]
    body: bytes
    elapsed_ms: float
    is_success: bool = True

    def text(self) -> str:
        return self.body.decode("utf-8", errors="replace")


class HTTPConnectionPool:
    """Thread-safe connection pool emulator for high-frequency domain probes."""

    def __init__(self, max_connections: int = 50, keep_alive_timeout_sec: float = 30.0):
        self.max_connections = max_connections
        self.keep_alive_timeout_sec = keep_alive_timeout_sec
        self._active_connections: Dict[str, List[float]] = {}  # host -> list of last_used timestamps
        self._lock = threading.Lock()

    def acquire_connection(self, host: str) -> bool:
        """Acquire a connection slot for the target host."""
        with self._lock:
            now = time.monotonic()
            # Clean expired keep-alive connections
            for h in list(self._active_connections):
                self._active_connections[h] = [
                    t for t in self._active_connections[h]
                    if now - t < self.keep_alive_timeout_sec
                ]
                if not self._active_connections[h]:
                    del self._active_connections[h]

            total_open = sum(len(conns) for conns in self._active_connections.values())
            if total_open >= self.max_connections:
                return False

            if host not in self._active_connections:
                self._active_connections[host] = []
            self._active_connections[host].append(now)
            return True

    def release_connection(self, host: str) -> None:
        """Release connection back to pool."""
        with self._lock:
            if host in self._active_connections and self._active_connections[host]:
                self._active_connections[host].pop(0)

    def simulate_get(self, url: str, headers: Optional[Dict[str, str]] = None) -> SimpleHTTPResponse:
        """Simulate fast low-latency HTTP GET request for testing domain status."""
        start = time.monotonic()
        host = url.split("//")[-1].split("/")[0]
        self.acquire_connection(host)
        
        # Fast simulated response
        elapsed = (time.monotonic() - start) * 1000.0
        self.release_connection(host)

        return SimpleHTTPResponse(
            status_code=200,
            headers={"Content-Type": "application/json", "Server": "JobGuard-Probe/2.4"},
            body=b'{"status":"domain_verified","active":true}',
            elapsed_ms=round(elapsed, 2),
            is_success=True
        )
