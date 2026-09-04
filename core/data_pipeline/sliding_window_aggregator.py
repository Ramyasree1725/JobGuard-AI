"""
JobGuard Core Data Pipeline - Sliding Window Metric Aggregator
Maintains time-based tumbling and sliding windows for continuous stream telemetry,
calculating real-time mean, variance, quantile sketches, and velocity surges.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import collections
import time
import math


@dataclass
class WindowMetricSummary:
    window_start_sec: float
    window_end_sec: float
    sample_count: int
    mean_val: float
    std_dev: float
    p95_val: float
    surge_velocity_ratio: float


class SlidingWindowAggregator:
    """Computes streaming window aggregations over telemetry metrics."""

    def __init__(self, window_size_seconds: float = 60.0, slide_interval_seconds: float = 10.0):
        self.window_size = window_size_seconds
        self.slide_interval = slide_interval_seconds
        self.events: collections.deque[Tuple[float, float]] = collections.deque()  # (timestamp, value)

    def record_datapoint(self, value: float, timestamp: Optional[float] = None) -> None:
        """Records a new numeric metric with timestamp."""
        ts = timestamp or time.time()
        self.events.append((ts, value))

        # Evict data older than window size
        cutoff = ts - self.window_size
        while self.events and self.events[0][0] < cutoff:
            self.events.popleft()

    def compute_summary(self) -> WindowMetricSummary:
        """Computes statistical metrics over current sliding window."""
        now = time.time()
        cutoff = now - self.window_size
        valid_vals = [v for ts, v in self.events if ts >= cutoff]

        if not valid_vals:
            return WindowMetricSummary(
                window_start_sec=cutoff,
                window_end_sec=now,
                sample_count=0,
                mean_val=0.0,
                std_dev=0.0,
                p95_val=0.0,
                surge_velocity_ratio=1.0
            )

        n = len(valid_vals)
        mean_v = sum(valid_vals) / n
        var = sum((x - mean_v) ** 2 for x in valid_vals) / n
        std = math.sqrt(var)

        sorted_vals = sorted(valid_vals)
        p95_idx = min(n - 1, int(0.95 * n))
        p95 = sorted_vals[p95_idx]

        # Velocity ratio: recent half vs older half
        half_cutoff = now - (self.window_size / 2.0)
        recent_count = sum(1 for ts, _ in self.events if ts >= half_cutoff)
        older_count = n - recent_count
        ratio = (recent_count / max(1, older_count))

        return WindowMetricSummary(
            window_start_sec=cutoff,
            window_end_sec=now,
            sample_count=n,
            mean_val=mean_v,
            std_dev=std,
            p95_val=p95,
            surge_velocity_ratio=ratio
        )
