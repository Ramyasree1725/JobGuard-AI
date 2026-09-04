"""
Aetheris Distributed Consensus: Raft Finite State Machine & Consensus Log
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import random
from typing import List, Dict, Any, Optional


class LogEntry:
    __slots__ = ('term', 'index', 'command', 'entry_hash')

    def __init__(self, term: int, index: int, command: Dict[str, Any]) -> None:
        self.term = term
        self.index = index
        self.command = command
        self.entry_hash = str(hash((term, index, str(command))))


class RaftNodeFSM:
    """
    Raft Consensus State Machine Node.
    Roles: LEADER, FOLLOWER, CANDIDATE
    Handles leader election timeouts, term increment, heartbeat broadcasting, and log replication.
    """
    FOLLOWER = "FOLLOWER"
    CANDIDATE = "CANDIDATE"
    LEADER = "LEADER"

    def __init__(self, node_id: str, peers: List[str], seed: Optional[int] = None) -> None:
        self.node_id = node_id
        self.peers = list(peers)
        self.rng = random.Random(seed)

        # Persistent state
        self.current_term = 0
        self.voted_for: Optional[str] = None
        self.log: List[LogEntry] = []

        # Volatile state
        self.state = self.FOLLOWER
        self.commit_index = 0
        self.last_applied = 0
        self.votes_received = 0

        # Randomized election timeout ticks (150-300ms equivalent)
        self.election_timeout = self.rng.randint(15, 30)
        self.ticks_since_heartbeat = 0

    def tick(self) -> Optional[Dict[str, Any]]:
        """Advances consensus timer by 1 tick."""
        self.ticks_since_heartbeat += 1

        if self.state == self.FOLLOWER:
            if self.ticks_since_heartbeat >= self.election_timeout:
                return self._start_election()
        elif self.state == self.CANDIDATE:
            if self.ticks_since_heartbeat >= self.election_timeout:
                return self._start_election()
        elif self.state == self.LEADER:
            # Send periodic heartbeats
            if self.ticks_since_heartbeat >= 5:
                self.ticks_since_heartbeat = 0
                return {"type": "HEARTBEAT", "term": self.current_term, "leader_id": self.node_id}

        return None

    def _start_election(self) -> Dict[str, Any]:
        self.state = self.CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id
        self.votes_received = 1
        self.ticks_since_heartbeat = 0
        self.election_timeout = self.rng.randint(15, 30)

        return {
            "type": "REQUEST_VOTE",
            "term": self.current_term,
            "candidate_id": self.node_id,
            "last_log_index": len(self.log),
            "last_log_term": self.log[-1].term if self.log else 0
        }

    def receive_vote(self, from_peer: str, granted: bool) -> bool:
        if self.state == self.CANDIDATE and granted:
            self.votes_received += 1
            total_nodes = len(self.peers) + 1
            if self.votes_received > (total_nodes // 2):
                self.state = self.LEADER
                return True
        return False

    def append_command(self, command: Dict[str, Any]) -> LogEntry:
        if self.state != self.LEADER:
            raise RuntimeError("Only leader can append commands")
        entry = LogEntry(self.current_term, len(self.log) + 1, command)
        self.log.append(entry)
        return entry
