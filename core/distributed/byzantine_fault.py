"""
JobGuard Core Distributed - Practical Byzantine Fault Tolerance (PBFT) Engine
Simulates 3f+1 state consensus with Pre-Prepare, Prepare, Commit, and View-Change
phases to protect multi-node verification ledgers from malicious validator collusion.
"""

import hashlib
import time
import enum
from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


class PBFTPhase(enum.Enum):
    PRE_PREPARE = "PRE_PREPARE"
    PREPARE = "PREPARE"
    COMMIT = "COMMIT"
    COMMITTED = "COMMITTED"
    VIEW_CHANGE = "VIEW_CHANGE"


@dataclass
class PBFTMessage:
    msg_type: PBFTPhase
    view_number: int
    sequence_number: int
    digest: str
    node_id: str
    signature: str = ""


class PBFTNode:
    """PBFT replica node with vote quorum evaluation."""

    def __init__(self, node_id: str, total_nodes: int, is_primary: bool = False):
        self.node_id = node_id
        self.total_nodes = total_nodes
        self.f = (total_nodes - 1) // 3  # Max tolerable Byzantine nodes
        self.is_primary = is_primary
        self.current_view = 0
        self.sequence_number = 0

        # Quorum tracking: (view, seq, digest) -> set of node_ids
        self.prepare_votes: Dict[Tuple[int, int, str], Set[str]] = {}
        self.commit_votes: Dict[Tuple[int, int, str], Set[str]] = {}
        self.committed_log: List[Tuple[int, str]] = []

    def handle_pre_prepare(self, msg: PBFTMessage) -> Optional[PBFTMessage]:
        """Validate pre-prepare from primary and broadcast prepare message."""
        if msg.view_number != self.current_view:
            return None

        # Cast prepare vote
        key = (msg.view_number, msg.sequence_number, msg.digest)
        if key not in self.prepare_votes:
            self.prepare_votes[key] = set()
        self.prepare_votes[key].add(self.node_id)

        return PBFTMessage(
            msg_type=PBFTPhase.PREPARE,
            view_number=msg.view_number,
            sequence_number=msg.sequence_number,
            digest=msg.digest,
            node_id=self.node_id
        )

    def handle_prepare(self, msg: PBFTMessage) -> Optional[PBFTMessage]:
        """Record prepare vote; if 2f+1 quorum achieved, broadcast commit."""
        key = (msg.view_number, msg.sequence_number, msg.digest)
        if key not in self.prepare_votes:
            self.prepare_votes[key] = set()
        self.prepare_votes[key].add(msg.node_id)

        # Check 2f + 1 quorum for prepare phase
        if len(self.prepare_votes[key]) >= (2 * self.f + 1):
            if key not in self.commit_votes:
                self.commit_votes[key] = set()
            self.commit_votes[key].add(self.node_id)

            return PBFTMessage(
                msg_type=PBFTPhase.COMMIT,
                view_number=msg.view_number,
                sequence_number=msg.sequence_number,
                digest=msg.digest,
                node_id=self.node_id
            )
        return None

    def handle_commit(self, msg: PBFTMessage) -> bool:
        """Record commit vote; if 2f+1 quorum achieved, commit to state machine."""
        key = (msg.view_number, msg.sequence_number, msg.digest)
        if key not in self.commit_votes:
            self.commit_votes[key] = set()
        self.commit_votes[key].add(msg.node_id)

        if len(self.commit_votes[key]) >= (2 * self.f + 1):
            if (msg.sequence_number, msg.digest) not in self.committed_log:
                self.committed_log.append((msg.sequence_number, msg.digest))
                return True
        return False
