"""
JobGuard Core Distributed - Epidemic Gossip Dissemination Protocol
Implements anti-entropy rumor mongering with push-pull gossip rounds and membership tracking.
"""

import random
import time
from typing import List, Dict, Tuple, Set, Optional, Any


class GossipNode:
    """Epidemic Anti-Entropy Gossip Node."""

    def __init__(self, node_id: str, fanout: int = 3):
        self.node_id = node_id
        self.fanout = fanout
        self.knowledge_base: Dict[str, Tuple[Any, int]] = {}  # key -> (value, version)
        self.known_peers: Set[str] = set()

    def update_local(self, key: str, value: Any) -> None:
        """Update local state with incremented version."""
        curr_ver = self.knowledge_base.get(key, (None, 0))[1]
        self.knowledge_base[key] = (value, curr_ver + 1)

    def prepare_push_digest(self) -> Dict[str, int]:
        """Produce state version digest for gossip exchange."""
        return {k: ver for k, (val, ver) in self.knowledge_base.items()}

    def reconcile_pull_request(self, incoming_digest: Dict[str, int]) -> Dict[str, Tuple[Any, int]]:
        """Return updates that the sender is missing or has older versions of."""
        updates: Dict[str, Tuple[Any, int]] = {}
        for k, (val, ver) in self.knowledge_base.items():
            if k not in incoming_digest or incoming_digest[k] < ver:
                updates[k] = (val, ver)
        return updates

    def apply_updates(self, incoming_updates: Dict[str, Tuple[Any, int]]) -> None:
        for k, (val, ver) in incoming_updates.items():
            curr_ver = self.knowledge_base.get(k, (None, -1))[1]
            if ver > curr_ver:
                self.knowledge_base[k] = (val, ver)
