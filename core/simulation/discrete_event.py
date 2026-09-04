"""
JobGuard Core Simulation - Discrete Event Simulation (DES) Engine
Models asynchronous queues, priority job schedulers, and recruiter candidate processing.
"""

import heapq
from typing import List, Tuple, Callable, Optional, Any, Dict
from dataclasses import dataclass, field


@dataclass(order=True)
class Event:
    event_time: float
    priority: int
    event_id: str = field(compare=False)
    callback: Callable[["DiscreteEventSimulator"], None] = field(compare=False)
    context: Dict[str, Any] = field(default_factory=dict, compare=False)


class DiscreteEventSimulator:
    """Discrete Event Simulator managing priority event queue and virtual simulation clock."""

    def __init__(self, start_time: float = 0.0):
        self.current_time = start_time
        self._event_queue: List[Event] = []
        self._event_counter = 0
        self.metrics: Dict[str, Any] = {}

    def schedule(self, delay: float, callback: Callable[["DiscreteEventSimulator"], None], priority: int = 10, context: Optional[Dict[str, Any]] = None) -> str:
        """Schedule future event to occur at current_time + delay."""
        self._event_counter += 1
        e_id = f"EVT-{self._event_counter:06d}"
        event = Event(
            event_time=self.current_time + max(0.0, delay),
            priority=priority,
            event_id=e_id,
            callback=callback,
            context=context or {}
        )
        heapq.heappush(self._event_queue, event)
        return e_id

    def run_until(self, end_time: float) -> int:
        """Advance simulation clock and dispatch events until end_time."""
        dispatched = 0
        while self._event_queue and self._event_queue[0].event_time <= end_time:
            event = heapq.heappop(self._event_queue)
            self.current_time = event.event_time
            event.callback(self)
            dispatched += 1

        self.current_time = end_time
        return dispatched
