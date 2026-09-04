"""
JobGuard Core Distributed - Consistent Hash Ring with Virtual Replicas (Ketama)
Minimizes key redistribution during horizontal scaling of threat detection cache nodes.
"""

import hashlib
import bisect
from typing import List, Dict, Tuple, Optional


class ConsistentHashRing:
    """Consistent Hash Ring with configurable virtual replica nodes."""

    def __init__(self, virtual_nodes: int = 100):
        self.v_nodes = virtual_nodes
        self.ring: List[int] = []
        self.node_map: Dict[int, str] = {}
        self.nodes: Set[str] = set()

    def _hash(self, key: str) -> int:
        raw = hashlib.md5(key.encode("utf-8")).hexdigest()
        return int(raw, 16)

    def add_node(self, node: str) -> None:
        self.nodes.add(node)
        for i in range(self.v_nodes):
            v_key = f"{node}#VN{i}"
            h = self._hash(v_key)
            self.ring.append(h)
            self.node_map[h] = node

        self.ring.sort()

    def remove_node(self, node: str) -> None:
        if node not in self.nodes:
            return
        self.nodes.remove(node)
        for i in range(self.v_nodes):
            v_key = f"{node}#VN{i}"
            h = self._hash(v_key)
            if h in self.node_map:
                del self.node_map[h]

        self.ring = sorted(self.node_map.keys())

    def get_node(self, key: str) -> Optional[str]:
        if not self.ring:
            return None
        h = self._hash(key)
        idx = bisect.bisect_right(self.ring, h)
        if idx == len(self.ring):
            idx = 0
        return self.node_map[self.ring[idx]]
