"""
JobGuard Core Distributed - Multi-Protocol Consensus Verification Suite
Implements Single-Decree Paxos, Multi-Paxos, Viewstamped Replication (VR),
and Chandy-Lamport Global Distributed State Snapshotting.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class PaxosProposal:
    proposal_number: int
    value: Any


class PaxosAcceptor:
    """Paxos Acceptor node enforcing promise invariants."""

    def __init__(self, acceptor_id: str):
        self.acceptor_id = acceptor_id
        self.min_proposal: int = 0
        self.accepted_proposal: Optional[int] = None
        self.accepted_value: Optional[Any] = None

    def receive_prepare(self, proposal_num: int) -> Tuple[bool, Optional[int], Optional[Any]]:
        """Phase 1b: Promise not to accept proposals lower than proposal_num."""
        if proposal_num > self.min_proposal:
            self.min_proposal = proposal_num
            return True, self.accepted_proposal, self.accepted_value
        return False, None, None

    def receive_accept(self, proposal_num: int, value: Any) -> bool:
        """Phase 2b: Accept value if proposal_num >= min_proposal."""
        if proposal_num >= self.min_proposal:
            self.min_proposal = proposal_num
            self.accepted_proposal = proposal_num
            self.accepted_value = value
            return True
        return False


class PaxosProposer:
    """Paxos Proposer coordinating consensus round across quorum."""

    def __init__(self, proposer_id: str, acceptors: List[PaxosAcceptor]):
        self.proposer_id = proposer_id
        self.acceptors = acceptors
        self.quorum_size = (len(acceptors) // 2) + 1
        self.proposal_counter = 0

    def propose(self, proposed_value: Any) -> Tuple[bool, Any]:
        self.proposal_counter += 1
        n = self.proposal_counter

        # Phase 1: Prepare
        promises = [a.receive_prepare(n) for a in self.acceptors]
        successful_promises = [p for p in promises if p[0]]

        if len(successful_promises) < self.quorum_size:
            return False, None  # Failed quorum

        # Select value with highest accepted proposal number if any
        highest_n = -1
        v = proposed_value
        for _, acc_n, acc_v in successful_promises:
            if acc_n is not None and acc_n > highest_n:
                highest_n = acc_n
                v = acc_v

        # Phase 2: Accept
        accepts = [a.receive_accept(n, v) for a in self.acceptors]
        successful_accepts = [acc for acc in accepts if acc]

        if len(successful_accepts) >= self.quorum_size:
            return True, v

        return False, None
