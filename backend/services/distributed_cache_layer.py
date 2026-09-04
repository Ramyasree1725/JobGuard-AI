"""
JobGuard Backend Service - Multi-Tier Distributed Cache & Invalidation Coordinator
Implements LRU Cache with TTL expiration, probabilistic early expiration (XFetch),
and consistent cache invalidation hooks for real-time threat intelligence queries.
"""

import time
import math
import random
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class CacheEntry:
    key: str
    value: Any
    created_at: float
    ttl_seconds: float
    compute_duration_seconds: float = 0.05


class DistributedCacheLayer:
    """Enterprise multi-tier caching layer with XFetch probabilistic early recomputation."""

    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        self.cache: Dict[str, CacheEntry] = {}
        self.access_order: List[str] = []

    def get(self, key: str, beta: float = 1.0) -> Tuple[Optional[Any], bool]:
        """Returns (cached_value, should_recompute_early)."""
        if key not in self.cache:
            return None, True

        entry = self.cache[key]
        now = time.time()
        time_left = (entry.created_at + entry.ttl_seconds) - now

        if time_left <= 0:
            # Expired
            del self.cache[key]
            self.access_order.remove(key)
            return None, True

        # Update LRU order
        self.access_order.remove(key)
        self.access_order.append(key)

        # XFetch: should recompute early if: -beta * delta * ln(rand()) > time_left
        rand_val = random.random()
        should_recompute = False
        if rand_val > 0:
            early_threshold = -beta * entry.compute_duration_seconds * math.log(rand_val)
            if early_threshold > time_left:
                should_recompute = True

        return entry.value, should_recompute

    def set(self, key: str, value: Any, ttl_seconds: float = 300.0, compute_duration: float = 0.05) -> None:
        now = time.time()
        if key in self.cache:
            self.access_order.remove(key)
        elif len(self.cache) >= self.capacity:
            # Evict LRU
            lru_key = self.access_order.pop(0)
            del self.cache[lru_key]

        self.cache[key] = CacheEntry(key, value, now, ttl_seconds, compute_duration)
        self.access_order.append(key)
