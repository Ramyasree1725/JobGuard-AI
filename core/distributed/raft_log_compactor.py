"""
JobGuard Core Distributed - Raft Log Compactor & Snapshot Manager
Manages state machine checkpoint snapshots, index truncation, and log entry garbage collection
to prevent unbounded write-ahead log growth across distributed threat graph clusters.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import hashlib
import json
import time


@dataclass
class RaftLogEntry:
    index: int
    term: int
    command: str
    payload: Dict[str, Any]


@dataclass
class RaftSnapshotMetadata:
    last_included_index: int
    last_included_term: int
    snapshot_timestamp: float
    state_payload: Dict[str, Any]
    sha256_checksum: str


class RaftLogCompactor:
    """Manages Raft log segment compaction and snapshot serialization."""

    def __init__(self, entries_per_snapshot_threshold: int = 100):
        self.threshold = entries_per_snapshot_threshold
        self.log: List[RaftLogEntry] = []
        self.latest_snapshot: Optional[RaftSnapshotMetadata] = None

    def append_entry(self, term: int, command: str, payload: Dict[str, Any]) -> int:
        """Appends entry to in-memory log."""
        next_idx = (self.log[-1].index + 1) if self.log else (self.latest_snapshot.last_included_index + 1 if self.latest_snapshot else 1)
        entry = RaftLogEntry(index=next_idx, term=term, command=command, payload=payload)
        self.log.append(entry)
        return next_idx

    def compact_log_if_needed(self, current_state_machine_state: Dict[str, Any]) -> Optional[RaftSnapshotMetadata]:
        """Truncates log entries preceding the compacted snapshot boundary."""
        if len(self.log) < self.threshold:
            return None

        last_entry = self.log[-1]
        state_json = json.dumps(current_state_machine_state, sort_keys=True)
        checksum = hashlib.sha256(state_json.encode("utf-8")).hexdigest()

        snapshot = RaftSnapshotMetadata(
            last_included_index=last_entry.index,
            last_included_term=last_entry.term,
            snapshot_timestamp=time.time(),
            state_payload=dict(current_state_machine_state),
            sha256_checksum=checksum
        )

        self.latest_snapshot = snapshot
        # Truncate in-memory log
        self.log.clear()
        return snapshot
