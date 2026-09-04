"""
JobGuard Core Distributed - Vector Clock & Lamport Timestamp Synchronization
Implements causality tracking, concurrent event detection, and partial ordering
for decentralized threat verification nodes.
"""

from typing import Dict, List, Tuple, Optional


class VectorClock:
    """Vector clock representation for distributed causality tracking."""

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.clock: Dict[str, int] = {node_id: 0}

    def increment(self) -> None:
        """Increment local clock counter on event occurrence."""
        self.clock[self.node_id] = self.clock.get(self.node_id, 0) + 1

    def send_event(self) -> Dict[str, int]:
        """Prepare clock state to attach to outbound network message."""
        self.increment()
        return dict(self.clock)

    def receive_event(self, incoming_clock: Dict[str, int]) -> None:
        """Merge incoming vector clock and advance local timestamp."""
        all_nodes = set(self.clock.keys()).union(incoming_clock.keys())
        for n in all_nodes:
            self.clock[n] = max(self.clock.get(n, 0), incoming_clock.get(n, 0))
        self.increment()

    @staticmethod
    def compare(v1: Dict[str, int], v2: Dict[str, int]) -> str:
        """Compare two vector clocks. Returns 'EQUALS', 'HAPPENED_BEFORE', 'HAPPENED_AFTER', or 'CONCURRENT'."""
        all_nodes = set(v1.keys()).union(v2.keys())
        less_or_equal = True
        greater_or_equal = True

        for n in all_nodes:
            c1 = v1.get(n, 0)
            c2 = v2.get(n, 0)
            if c1 > c2:
                less_or_equal = False
            if c1 < c2:
                greater_or_equal = False

        if less_or_equal and greater_or_equal:
            return "EQUALS"
        if less_or_equal:
            return "HAPPENED_BEFORE"
        if greater_or_equal:
            return "HAPPENED_AFTER"
        return "CONCURRENT"
