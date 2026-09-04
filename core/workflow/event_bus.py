"""
JobGuard Core Workflow - Asynchronous Pub/Sub Event Bus
Decouples domain events (ScamDetected, UserAlerted, ComplaintGenerated)
with topic matching, dead-letter queues, and thread-safe dispatchers.
"""

import time
import threading
from typing import Dict, List, Callable, Optional, Any, Set
from dataclasses import dataclass, field


@dataclass
class EventMessage:
    topic: str
    event_id: str
    payload: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    correlation_id: Optional[str] = None


@dataclass
class SubscriptionHandle:
    sub_id: str
    topic_pattern: str
    callback: Callable[[EventMessage], None]


class AsyncEventBus:
    """Thread-safe event bus with hierarchical topic wildcards (e.g., 'scam.*', 'audit.offer.#')."""

    def __init__(self):
        self._subscriptions: Dict[str, SubscriptionHandle] = {}
        self._dead_letter_queue: List[Tuple[EventMessage, str]] = []
        self._lock = threading.Lock()
        self._sub_counter = 0

    def subscribe(self, topic_pattern: str, callback: Callable[[EventMessage], None]) -> str:
        """Subscribe callback to topic pattern; returns subscription ID."""
        with self._lock:
            self._sub_counter += 1
            sub_id = f"SUB-{self._sub_counter:04d}"
            handle = SubscriptionHandle(sub_id=sub_id, topic_pattern=topic_pattern, callback=callback)
            self._subscriptions[sub_id] = handle
            return sub_id

    def unsubscribe(self, sub_id: str) -> bool:
        with self._lock:
            return self._subscriptions.pop(sub_id, None) is not None

    def publish(self, topic: str, payload: Dict[str, Any], correlation_id: Optional[str] = None) -> int:
        """Publish event message to all matching subscribers. Returns number of dispatched handlers."""
        event_id = f"EVT-{int(time.time()*1000)}-{hash(topic) % 10000}"
        msg = EventMessage(
            topic=topic,
            event_id=event_id,
            payload=payload,
            timestamp=time.time(),
            correlation_id=correlation_id
        )

        with self._lock:
            matching_handles = [
                h for h in self._subscriptions.values()
                if self._match_topic(h.topic_pattern, topic)
            ]

        dispatched = 0
        for handle in matching_handles:
            try:
                handle.callback(msg)
                dispatched += 1
            except Exception as ex:
                with self._lock:
                    self._dead_letter_queue.append((msg, str(ex)))

        return dispatched

    @staticmethod
    def _match_topic(pattern: str, topic: str) -> bool:
        """Match MQTT/AMQP-style topic patterns: '*' matches single word, '#' matches multi-word."""
        if pattern == "#" or pattern == topic:
            return True

        pat_parts = pattern.split(".")
        top_parts = topic.split(".")

        p_idx = 0
        t_idx = 0

        while p_idx < len(pat_parts) and t_idx < len(top_parts):
            p = pat_parts[p_idx]
            if p == "#":
                return True
            if p != "*" and p != top_parts[t_idx]:
                return False
            p_idx += 1
            t_idx += 1

        if p_idx < len(pat_parts) and pat_parts[p_idx] == "#":
            return True

        return p_idx == len(pat_parts) and t_idx == len(top_parts)

    def get_dead_letters(self) -> List[Tuple[EventMessage, str]]:
        with self._lock:
            return list(self._dead_letter_queue)
