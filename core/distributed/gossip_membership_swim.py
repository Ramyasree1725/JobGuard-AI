"""
JobGuard Core Distributed - SWIM Process Group Membership Protocol
Structured Weakly-Consistent Infection-Style Process Group Membership Protocol (SWIM)
with suspicion mechanism and indirect ping-req probes.
"""

import time
import random
import enum
from typing import List, Dict, Tuple, Set, Optional, Any
from dataclasses import dataclass, field


class MemberState(enum.Enum):
    ALIVE = "ALIVE"
    SUSPECT = "SUSPECT"
    DEAD = "DEAD"


@dataclass
class MemberRecord:
    node_id: str
    ip_address: str
    port: int
    state: MemberState = MemberState.ALIVE
    incarnation: int = 0
    last_heard_timestamp: float = field(default_factory=time.time)


class SWIMMembershipProtocol:
    """SWIM cluster failure detector and gossip dissemination."""

    def __init__(self, local_node_id: str, ping_req_k: int = 3, suspicion_timeout_sec: float = 5.0):
        self.local_id = local_node_id
        self.k_probes = ping_req_k
        self.suspicion_timeout = suspicion_timeout_sec
        self.members: Dict[str, MemberRecord] = {}

    def add_member(self, node_id: str, ip: str, port: int) -> None:
        self.members[node_id] = MemberRecord(node_id, ip, port)

    def ping_round(self) -> Dict[str, Any]:
        """Execute one SWIM protocol probe cycle."""
        eligible_peers = [m for m in self.members.values() if m.node_id != self.local_id and m.state != MemberState.DEAD]
        if not eligible_peers:
            return {"status": "NO_PEERS"}

        target = random.choice(eligible_peers)
        now = time.time()

        # Simulated ping response
        direct_ack = (random.random() < 0.85)
        if direct_ack:
            target.state = MemberState.ALIVE
            target.last_heard_timestamp = now
            return {"status": "DIRECT_ACK", "target": target.node_id}

        # Indirect ping-req via k peers
        indirect_ack = (random.random() < 0.6)
        if indirect_ack:
            target.state = MemberState.ALIVE
            target.last_heard_timestamp = now
            return {"status": "INDIRECT_ACK", "target": target.node_id}

        # Enter suspicion state
        target.state = MemberState.SUSPECT
        return {"status": "SUSPECT_DECLARED", "target": target.node_id}
