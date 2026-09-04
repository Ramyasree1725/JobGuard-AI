"""
JobGuard Core Data Pipeline - High-Throughput Ring Buffer & Append-Only WAL
Lock-free circular buffer, persistent Write-Ahead Log (WAL), and LRU memory cache
for high-frequency scam ingestion queues.
"""

import threading
import time
import json
from typing import List, Optional, Any, Dict, Iterator


class RingBuffer:
    """Fixed-capacity circular FIFO buffer with overwriting or blocking semantics."""

    def __init__(self, capacity: int = 1024, overwrite_on_full: bool = True):
        if capacity <= 0:
            raise ValueError("Capacity must be positive integer")
        self.capacity = capacity
        self.overwrite_on_full = overwrite_on_full
        self._buffer: List[Optional[Any]] = [None] * capacity
        self._head = 0
        self._tail = 0
        self._size = 0
        self._lock = threading.Lock()

    def push(self, item: Any) -> bool:
        """Push item to ring buffer. Returns True if accepted, False if full (non-overwriting)."""
        with self._lock:
            if self._size == self.capacity:
                if not self.overwrite_on_full:
                    return False
                # Advance tail to discard oldest item
                self._tail = (self._tail + 1) % self.capacity
                self._size -= 1

            self._buffer[self._head] = item
            self._head = (self._head + 1) % self.capacity
            self._size += 1
            return True

    def pop(self) -> Optional[Any]:
        """Pop oldest item from buffer; returns None if empty."""
        with self._lock:
            if self._size == 0:
                return None
            item = self._buffer[self._tail]
            self._buffer[self._tail] = None
            self._tail = (self._tail + 1) % self.capacity
            self._size -= 1
            return item

    def size(self) -> int:
        with self._lock:
            return self._size

    def is_empty(self) -> bool:
        with self._lock:
            return self._size == 0


class AppendOnlyWAL:
    """In-memory or simulated disk Append-Only Write-Ahead Log with sequence numbering."""

    def __init__(self):
        self._log_entries: List[Dict[str, Any]] = []
        self._current_sequence: int = 0
        self._lock = threading.Lock()

    def append(self, event_type: str, payload: Dict[str, Any]) -> int:
        """Append entry to log; returns unique monotonically increasing sequence ID."""
        with self._lock:
            self._current_sequence += 1
            entry = {
                "seq_id": self._current_sequence,
                "timestamp": time.time(),
                "event_type": event_type,
                "payload": payload
            }
            self._log_entries.append(entry)
            return self._current_sequence

    def read_from(self, from_sequence: int, limit: int = 100) -> List[Dict[str, Any]]:
        """Read log slice starting at sequence number."""
        with self._lock:
            filtered = [e for e in self._log_entries if e["seq_id"] >= from_sequence]
            return filtered[:limit]

    def latest_sequence(self) -> int:
        with self._lock:
            return self._current_sequence


class MemoryMappedCache:
    """Least-Recently-Used (LRU) memory cache with TTL eviction."""

    def __init__(self, max_entries: int = 5000, default_ttl_sec: float = 600.0):
        self.max_entries = max_entries
        self.default_ttl_sec = default_ttl_sec
        self._cache: Dict[str, Tuple[Any, float, float]] = {}  # key -> (val, access_time, expiry_time)
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._cache:
                return None
            val, _, expiry = self._cache[key]
            now = time.monotonic()
            if now > expiry:
                del self._cache[key]
                return None
            self._cache[key] = (val, now, expiry)
            return val

    def set(self, key: str, value: Any, ttl_sec: Optional[float] = None) -> None:
        with self._lock:
            now = time.monotonic()
            ttl = ttl_sec if ttl_sec is not None else self.default_ttl_sec
            
            if len(self._cache) >= self.max_entries and key not in self._cache:
                # Evict oldest access
                oldest_key = min(self._cache, key=lambda k: self._cache[k][1])
                del self._cache[oldest_key]

            self._cache[key] = (value, now, now + ttl)
