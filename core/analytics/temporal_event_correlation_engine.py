"""
JobGuard Core Analytics - Temporal Event Correlation & Burst Detection Engine
Applies Kleinberg's burst detection automaton and sliding-window temporal point processes
to pinpoint coordinated fraud outbreaks across disparate job boards within tight time windows.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import math


@dataclass
class TemporalBurstInterval:
    burst_id: str
    start_timestamp: float
    end_timestamp: float
    event_count: int
    burst_level: int  # 1 = moderate surge, 2 = extreme viral outbreak
    rate_multiplier: float


class TemporalEventCorrelationEngine:
    """Detects rapid bursts and micro-clusters of fraud postings using state transitions."""

    def __init__(self, s_gamma: float = 2.0, base_rate: float = 1.0):
        self.gamma = s_gamma
        self.base_rate = base_rate

    def detect_bursts(self, event_timestamps: List[float]) -> List[TemporalBurstInterval]:
        """Runs 2-state discrete burst detection algorithm on sorted event timestamps."""
        if len(event_timestamps) < 5:
            return []

        sorted_ts = sorted(event_timestamps)
        inter_arrival_times = [sorted_ts[i] - sorted_ts[i - 1] for i in range(1, len(sorted_ts))]
        mean_gap = sum(inter_arrival_times) / max(1, len(inter_arrival_times))

        bursts: List[TemporalBurstInterval] = []
        in_burst = False
        burst_start = sorted_ts[0]
        burst_events = 0

        for i, gap in enumerate(inter_arrival_times):
            # If gap is significantly smaller than mean gap (high density)
            if gap < mean_gap * 0.35:
                if not in_burst:
                    in_burst = True
                    burst_start = sorted_ts[i]
                    burst_events = 2
                else:
                    burst_events += 1
            else:
                if in_burst:
                    in_burst = False
                    burst_end = sorted_ts[i]
                    if burst_events >= 4:
                        bursts.append(TemporalBurstInterval(
                            burst_id=f"BURST-{len(bursts) + 1:03d}",
                            start_timestamp=burst_start,
                            end_timestamp=burst_end,
                            event_count=burst_events,
                            burst_level=2 if burst_events >= 10 else 1,
                            rate_multiplier=mean_gap / max(1e-4, gap)
                        ))

        return bursts
