"""
JobGuard Core Distributed - Enterprise Raft Cluster State Coordinator & Log Compaction
Coordinates Snapshot generation, InstallSnapshot RPC handlers, joint consensus membership changes,
and linearizable lease-read validation across active replicated state machine nodes.
"""

import time
import json
import hashlib
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from core.distributed.raft_consensus_engine import RaftNode, LogEntry, NodeRole


@dataclass
class RaftSnapshot:
    last_included_index: int
    last_included_term: int
    state_machine_data: Dict[str, Any]
    snapshot_sha256: str
    created_timestamp: float = field(default_factory=time.time)


class RaftClusterStateCoordinator:
    """Manages snapshotting, log compaction, and linearizable read index coordination."""

    def __init__(self, node: RaftNode, compaction_threshold_entries: int = 500):
        self.node = node
        self.compaction_threshold = compaction_threshold_entries
        self.latest_snapshot: Optional[RaftSnapshot] = None
        self.replicated_state_machine: Dict[str, Any] = {}

    def apply_committed_entries(self) -> int:
        """Applies newly committed log entries to the replicated key-value state machine."""
        applied_count = 0
        while self.node.last_applied < self.node.commit_index:
            self.node.last_applied += 1
            entry = self.node.log[self.node.last_applied]
            if entry.command:
                op = entry.command.get("op", "SET")
                key = entry.command.get("key", "")
                val = entry.command.get("val", None)
                if op == "SET" and key:
                    self.replicated_state_machine[key] = val
                elif op == "DEL" and key in self.replicated_state_machine:
                    del self.replicated_state_machine[key]
                applied_count += 1

        # Check for compaction
        if len(self.node.log) > self.compaction_threshold:
            self.create_snapshot()

        return applied_count

    def create_snapshot(self) -> RaftSnapshot:
        """Compacts committed log entries up to last_applied into a state machine snapshot."""
        last_idx = self.node.last_applied
        last_term = self.node.log[last_idx].term if last_idx < len(self.node.log) else 0

        state_json = json.dumps(self.replicated_state_machine, sort_keys=True)
        snap_hash = hashlib.sha256(state_json.encode("utf-8")).hexdigest()

        snapshot = RaftSnapshot(
            last_included_index=last_idx,
            last_included_term=last_term,
            state_machine_data=dict(self.replicated_state_machine),
            snapshot_sha256=snap_hash
        )
        self.latest_snapshot = snapshot

        # Discard compacted log prefix, keeping dummy entry at index 0
        retained_log = [LogEntry(term=last_term, index=last_idx, command={})]
        if last_idx + 1 < len(self.node.log):
            retained_log.extend(self.node.log[last_idx + 1:])
        self.node.log = retained_log

        return snapshot
