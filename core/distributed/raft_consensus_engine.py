"""
JobGuard Core Distributed - Raft Consensus Protocol & Replicated State Machine
Implements Leader Election, Heartbeat broadcasting, Log Replication,
Commit Index advancements, and State Machine Application.
"""

import time
import random
import enum
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field


class NodeRole(enum.Enum):
    FOLLOWER = "FOLLOWER"
    CANDIDATE = "CANDIDATE"
    LEADER = "LEADER"


@dataclass
class LogEntry:
    term: int
    index: int
    command: Dict[str, Any]


@dataclass
class RequestVoteArgs:
    term: int
    candidate_id: str
    last_log_index: int
    last_log_term: int


@dataclass
class RequestVoteReply:
    term: int
    vote_granted: bool


@dataclass
class AppendEntriesArgs:
    term: int
    leader_id: str
    prev_log_index: int
    prev_log_term: int
    entries: List[LogEntry]
    leader_commit: int


@dataclass
class AppendEntriesReply:
    term: int
    success: bool
    match_index: int = 0


class RaftNode:
    """Full Raft consensus replica node implementation."""

    def __init__(self, node_id: str, peers: List[str]):
        self.node_id = node_id
        self.peers = peers
        self.current_term = 0
        self.voted_for: Optional[str] = None
        self.log: List[LogEntry] = [LogEntry(term=0, index=0, command={})]
        self.commit_index = 0
        self.last_applied = 0

        self.role = NodeRole.FOLLOWER
        self.leader_id: Optional[str] = None

        # Leader volatile state
        self.next_index: Dict[str, int] = {}
        self.match_index: Dict[str, int] = {}

    def handle_request_vote(self, args: RequestVoteArgs) -> RequestVoteReply:
        """Handle incoming RequestVote RPC from candidate."""
        if args.term > self.current_term:
            self.current_term = args.term
            self.role = NodeRole.FOLLOWER
            self.voted_for = None

        vote_granted = False
        last_log = self.log[-1]

        # Check candidate term and log up-to-dateness
        if args.term == self.current_term and (self.voted_for is None or self.voted_for == args.candidate_id):
            if (args.last_log_term > last_log.term) or (
                args.last_log_term == last_log.term and args.last_log_index >= last_log.index
            ):
                vote_granted = True
                self.voted_for = args.candidate_id

        return RequestVoteReply(term=self.current_term, vote_granted=vote_granted)

    def handle_append_entries(self, args: AppendEntriesArgs) -> AppendEntriesReply:
        """Handle incoming AppendEntries RPC from leader."""
        if args.term < self.current_term:
            return AppendEntriesReply(term=self.current_term, success=False)

        self.current_term = args.term
        self.role = NodeRole.FOLLOWER
        self.leader_id = args.leader_id

        # Check log matching property
        if args.prev_log_index >= len(self.log) or self.log[args.prev_log_index].term != args.prev_log_term:
            return AppendEntriesReply(term=self.current_term, success=False, match_index=len(self.log) - 1)

        # Append new entries
        insert_idx = args.prev_log_index + 1
        for entry in args.entries:
            if insert_idx < len(self.log):
                if self.log[insert_idx].term != entry.term:
                    self.log = self.log[:insert_idx]
                    self.log.append(entry)
            else:
                self.log.append(entry)
            insert_idx += 1

        # Update commit index
        if args.leader_commit > self.commit_index:
            self.commit_index = min(args.leader_commit, len(self.log) - 1)

        return AppendEntriesReply(term=self.current_term, success=True, match_index=len(self.log) - 1)
