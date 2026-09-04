"""
JobGuard Core Knowledge - Temporal Knowledge Graph & Time-Varying Relations
Represents quadruples (Subject, Predicate, Object, [t_start, t_end])
for tracking campaign lifespans, domain expiration cycles, and syndicate rotation.
"""

from typing import Dict, List, Tuple, Optional, Any, Set, Iterator
from dataclasses import dataclass, field
import time


@dataclass(frozen=True)
class TemporalInterval:
    start_time: float
    end_time: float  # float('inf') for open-ended valid relations

    def contains(self, timestamp: float) -> bool:
        return self.start_time <= timestamp <= self.end_time

    def overlaps(self, other: "TemporalInterval") -> bool:
        return max(self.start_time, other.start_time) <= min(self.end_time, other.end_time)


@dataclass(frozen=True)
class TemporalQuadruple:
    subject: str
    predicate: str
    object: str
    interval: TemporalInterval

    def is_valid_at(self, t: float) -> bool:
        return self.interval.contains(t)


class TemporalKnowledgeGraph:
    """Multi-snapshot temporal knowledge graph with point-in-time point queries."""

    def __init__(self):
        self._quads: List[TemporalQuadruple] = []
        self._entity_intervals: Dict[str, List[TemporalInterval]] = {}

    def add_temporal_fact(
        self,
        subject: str,
        predicate: str,
        obj: str,
        start_time: float,
        end_time: float = float("inf")
    ) -> TemporalQuadruple:
        """Register a fact with valid temporal interval."""
        interval = TemporalInterval(start_time, end_time)
        quad = TemporalQuadruple(subject, predicate, obj, interval)
        self._quads.append(quad)

        if subject not in self._entity_intervals:
            self._entity_intervals[subject] = []
        self._entity_intervals[subject].append(interval)

        return quad

    def snapshot_at(self, timestamp: float) -> List[Tuple[str, str, str]]:
        """Extract a static knowledge graph snapshot at a specific point in time."""
        return [
            (q.subject, q.predicate, q.object)
            for q in self._quads
            if q.is_valid_at(timestamp)
        ]

    def query_entity_history(self, entity_id: str) -> List[TemporalQuadruple]:
        """Query all facts associated with entity across chronological history."""
        matches = [
            q for q in self._quads
            if q.subject == entity_id or q.object == entity_id
        ]
        matches.sort(key=lambda q: q.interval.start_time)
        return matches

    def detect_temporal_anomalies(self, entity_id: str, max_lifespan_sec: float = 86400.0 * 14) -> List[str]:
        """Detect ephemeral entities created and abandoned rapidly (typical for throwaway scam infrastructure)."""
        history = self.query_entity_history(entity_id)
        if not history:
            return []

        anomalies = []
        t_first = min(q.interval.start_time for q in history)
        t_last = max(q.interval.start_time for q in history)
        lifespan = t_last - t_first

        if 0 < lifespan < max_lifespan_sec and len(history) > 10:
            anomalies.append(
                f"Entity '{entity_id}' exhibited high burst activity ({len(history)} events) across short lifespan ({lifespan / 86400.0:.1f} days)"
            )

        return anomalies
