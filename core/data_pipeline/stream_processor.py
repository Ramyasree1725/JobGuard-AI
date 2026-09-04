"""
JobGuard Core Data Pipeline - Stream Processor & Event Windowing
Implements tumbling, sliding, and session windows over high-volume telemetry events,
with watermark tracking, out-of-order event handling, and real-time aggregations.
"""

import time
import math
import threading
from typing import Dict, List, Optional, Callable, Any, Tuple
from dataclasses import dataclass, field


@dataclass
class EventRecord:
    event_id: str
    event_type: str
    timestamp: float
    payload: Dict[str, Any]
    source: str = "telemetry_collector"


@dataclass
class WindowAggregate:
    window_start: float
    window_end: float
    event_count: int
    metrics: Dict[str, float]
    metadata: Dict[str, Any] = field(default_factory=dict)


class TumblingWindow:
    """Fixed-size, non-overlapping temporal event aggregation window."""

    def __init__(self, window_size_sec: float, aggregator_fn: Optional[Callable[[List[EventRecord]], Dict[str, float]]] = None):
        self.window_size_sec = window_size_sec
        self.aggregator_fn = aggregator_fn or self._default_aggregator
        self._windows: Dict[int, List[EventRecord]] = {}
        self._lock = threading.Lock()

    @staticmethod
    def _default_aggregator(events: List[EventRecord]) -> Dict[str, float]:
        return {"count": float(len(events))}

    def add_event(self, event: EventRecord) -> None:
        window_idx = int(event.timestamp // self.window_size_sec)
        with self._lock:
            if window_idx not in self._windows:
                self._windows[window_idx] = []
            self._windows[window_idx].append(event)

    def trigger_completed_windows(self, current_time: float, max_lateness_sec: float = 5.0) -> List[WindowAggregate]:
        """Finalize and purge windows older than current watermark."""
        cutoff_idx = int((current_time - max_lateness_sec) // self.window_size_sec)
        aggregates: List[WindowAggregate] = []

        with self._lock:
            expired_indices = [idx for idx in self._windows if idx < cutoff_idx]
            for idx in sorted(expired_indices):
                events = self._windows.pop(idx)
                w_start = idx * self.window_size_sec
                w_end = w_start + self.window_size_sec
                metrics = self.aggregator_fn(events)
                aggregates.append(WindowAggregate(
                    window_start=w_start,
                    window_end=w_end,
                    event_count=len(events),
                    metrics=metrics
                ))

        return aggregates


class SlidingWindow:
    """Sliding temporal window with configurable slide step and window length."""

    def __init__(self, length_sec: float, slide_sec: float):
        self.length_sec = length_sec
        self.slide_sec = slide_sec
        self._events: List[EventRecord] = []
        self._last_evaluated_slide: float = 0.0
        self._lock = threading.Lock()

    def add_event(self, event: EventRecord) -> None:
        with self._lock:
            self._events.append(event)

    def evaluate_slides(self, current_time: float) -> List[WindowAggregate]:
        """Compute metrics for all elapsed slides up to current_time."""
        aggregates: List[WindowAggregate] = []
        if self._last_evaluated_slide == 0.0:
            self._last_evaluated_slide = (current_time // self.slide_sec) * self.slide_sec

        with self._lock:
            # Purge events older than current_time - length_sec
            purge_cutoff = current_time - (self.length_sec * 2.0)
            self._events = [e for e in self._events if e.timestamp > purge_cutoff]

            next_slide = self._last_evaluated_slide + self.slide_sec
            while next_slide <= current_time:
                w_start = next_slide - self.length_sec
                w_end = next_slide
                
                # Filter events in [w_start, w_end]
                window_events = [e for e in self._events if w_start <= e.timestamp <= w_end]
                
                # Compute statistics
                risk_scores = [float(e.payload.get("risk_score", 0.0)) for e in window_events if "risk_score" in e.payload]
                avg_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0.0
                max_risk = max(risk_scores) if risk_scores else 0.0

                aggregates.append(WindowAggregate(
                    window_start=w_start,
                    window_end=w_end,
                    event_count=len(window_events),
                    metrics={
                        "count": float(len(window_events)),
                        "avg_risk_score": round(avg_risk, 2),
                        "max_risk_score": round(max_risk, 2),
                        "throughput_eps": round(len(window_events) / self.length_sec, 2)
                    }
                ))

                self._last_evaluated_slide = next_slide
                next_slide += self.slide_sec

        return aggregates


class StreamProcessor:
    """Master stream processing pipeline with real-time anomaly dispatching."""

    def __init__(self, watermark_delay_sec: float = 2.0):
        self.watermark_delay_sec = watermark_delay_sec
        self.tumbling_1m = TumblingWindow(window_size_sec=60.0)
        self.sliding_5m = SlidingWindow(length_sec=300.0, slide_sec=10.0)
        self._handlers: List[Callable[[WindowAggregate], None]] = []

    def register_aggregate_handler(self, handler: Callable[[WindowAggregate], None]) -> None:
        self._handlers.append(handler)

    def ingest_event(self, event: EventRecord) -> None:
        """Ingest event into all active window pipelines."""
        self.tumbling_1m.add_event(event)
        self.sliding_5m.add_event(event)

    def tick(self, now: Optional[float] = None) -> List[WindowAggregate]:
        """Periodic clock trigger to materialize window aggregates and notify handlers."""
        current_time = now if now is not None else time.time()
        
        t_aggs = self.tumbling_1m.trigger_completed_windows(current_time, max_lateness_sec=self.watermark_delay_sec)
        s_aggs = self.sliding_5m.evaluate_slides(current_time)
        
        all_aggs = t_aggs + s_aggs
        for agg in all_aggs:
            for handler in self._handlers:
                try:
                    handler(agg)
                except Exception as e:
                    pass  # isolate handler failures
                    
        return all_aggs
