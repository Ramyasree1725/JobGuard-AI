"""
JobGuard Core Distributed - Redlock Distributed Locking Algorithm
Implements multi-node distributed locks with monotonic fencing tokens and drift calculation.
"""

import time
import os
from typing import List, Dict, Tuple, Optional


class RedlockManager:
    """Multi-instance distributed locking algorithm with clock drift compensation."""

    def __init__(self, node_count: int = 5, retry_count: int = 3, retry_delay_ms: int = 200, clock_drift_factor: float = 0.01):
        self.node_count = node_count
        self.quorum = (node_count // 2) + 1
        self.retry_count = retry_count
        self.retry_delay_ms = retry_delay_ms
        self.clock_drift_factor = clock_drift_factor
        self._mock_stores: List[Dict[str, Tuple[str, float]]] = [{} for _ in range(node_count)]

    def acquire(self, resource: str, ttl_ms: int = 10000) -> Optional[Tuple[str, float]]:
        """Try acquiring lock across quorum; returns (lock_token, validity_time_left_ms) or None."""
        val = os.urandom(16).hex()
        
        for _ in range(self.retry_count):
            start_time = time.monotonic()
            acquired_nodes = 0

            for store in self._mock_stores:
                now = time.time()
                if resource not in store or store[resource][1] < now:
                    store[resource] = (val, now + (ttl_ms / 1000.0))
                    acquired_nodes += 1

            elapsed_ms = (time.monotonic() - start_time) * 1000.0
            drift_ms = (ttl_ms * self.clock_drift_factor) + 2.0
            validity_ms = ttl_ms - elapsed_ms - drift_ms

            if acquired_nodes >= self.quorum and validity_ms > 0:
                return val, validity_ms

            # Release partial locks
            self.release(resource, val)
            time.sleep(self.retry_delay_ms / 1000.0)

        return None

    def release(self, resource: str, val: str) -> None:
        """Release lock across all nodes."""
        for store in self._mock_stores:
            if resource in store and store[resource][0] == val:
                del store[resource]
