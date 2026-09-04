"""
JobGuard Core Distributed - Chord Distributed Hash Table (DHT) Protocol
Implements consistent hashing, finger table lookups, and stabilized ring topologies
for decentralized blacklist and scam signature storage.
"""

import hashlib
from typing import Dict, List, Tuple, Optional, Any


class ChordNode:
    """Chord DHT node with m-bit identifier space (default m=16, 65536 nodes)."""

    def __init__(self, node_ip: str, m: int = 16):
        self.node_ip = node_ip
        self.m = m
        self.id = self._hash(node_ip)
        self.finger_table: List[Tuple[int, "ChordNode"]] = []  # (start, node)
        self.predecessor: Optional["ChordNode"] = None
        self.successor: "ChordNode" = self
        self.data_store: Dict[str, Any] = {}

    def _hash(self, key: str) -> int:
        raw_hash = hashlib.sha1(key.encode("utf-8")).hexdigest()
        return int(raw_hash, 16) % (1 << self.m)

    def find_successor(self, key_id: int) -> "ChordNode":
        """Find the immediate successor node responsible for key_id."""
        if self._in_interval(key_id, self.id, self.successor.id, right_inclusive=True):
            return self.successor
        
        closest = self.closest_preceding_node(key_id)
        if closest == self:
            return self.successor
        return closest.find_successor(key_id)

    def closest_preceding_node(self, key_id: int) -> "ChordNode":
        for _, node in reversed(self.finger_table):
            if self._in_interval(node.id, self.id, key_id):
                return node
        return self

    def _in_interval(self, val: int, start: int, end: int, right_inclusive: bool = False) -> bool:
        if start < end:
            return (start < val <= end) if right_inclusive else (start < val < end)
        else:
            return (val > start or val <= end) if right_inclusive else (val > start or val < end)

    def put(self, key: str, value: Any) -> None:
        key_id = self._hash(key)
        responsible_node = self.find_successor(key_id)
        responsible_node.data_store[key] = value

    def get(self, key: str) -> Optional[Any]:
        key_id = self._hash(key)
        responsible_node = self.find_successor(key_id)
        return responsible_node.data_store.get(key)
