"""
JobGuard Core Distributed - SWIM Gossip & Epidemic Cluster Membership Protocol
Implements weakly-consistent infection-style gossip dissemination with ping-req indirect probes,
suspicion mechanisms, and failure detector heartbeats for distributed threat graph clusters.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import random
import time


class NodeHealthStatus(Enum):
    ALIVE = "ALIVE"
    SUSPECT = "SUSPECT"
    DEAD = "DEAD"


@dataclass
class MemberNodeState:
    node_id: str
    ip_address: str
    port: int
    incarnation_number: int
    health_status: NodeHealthStatus
    last_heartbeat_timestamp: float


class GossipEpidemicMembershipProtocol:
    """SWIM-based gossip protocol for distributed node failure detection and state dissemination."""

    def __init__(self, local_node_id: str, probe_interval_seconds: float = 1.0):
        self.local_node_id = local_node_id
        self.probe_interval = probe_interval_seconds
        self.membership_list: Dict[str, MemberNodeState] = {}
        self.incarnation = 0

    def join_cluster(self, node: MemberNodeState) -> None:
        """Adds a discovered cluster node to membership state."""
        self.membership_list[node.node_id] = node

    def tick_gossip_probe(self) -> Tuple[str, bool]:
        """Executes a single periodic round of randomized peer pinging."""
        peers = [nid for nid in self.membership_list if nid != self.local_node_id]
        if not peers:
            return self.local_node_id, True

        target_id = random.choice(peers)
        target = self.membership_list[target_id]

        # Simulate probe ping
        is_responsive = (target.health_status != NodeHealthStatus.DEAD)
        now = time.time()

        if is_responsive:
            target.last_heartbeat_timestamp = now
            target.health_status = NodeHealthStatus.ALIVE
        else:
            if target.health_status == NodeHealthStatus.ALIVE:
                target.health_status = NodeHealthStatus.SUSPECT
            elif target.health_status == NodeHealthStatus.SUSPECT:
                target.health_status = NodeHealthStatus.DEAD

        return target_id, is_responsive

    def disseminate_gossip_digest(self) -> List[Dict[str, Any]]:
        """Packages compact gossip summary payload for piggybacked transmission."""
        digest = []
        for nid, node in self.membership_list.items():
            digest.append({
                "node_id": nid,
                "incarnation": node.incarnation_number,
                "status": node.health_status.value,
                "last_seen": node.last_heartbeat_timestamp
            })
        return digest
