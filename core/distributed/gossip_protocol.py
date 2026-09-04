"""
Aetheris Distributed Consensus: Anti-Entropy Peer-to-Peer Gossip Protocol
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import random
from typing import List, Dict, Any, Optional, Set


class GossipMessage:
    __slots__ = ('message_id', 'origin_peer', 'topic', 'data', 'hop_count')

    def __init__(self, msg_id: str, origin: str, topic: str, data: Any, hops: int = 0) -> None:
        self.message_id = msg_id
        self.origin_peer = origin
        self.topic = topic
        self.data = data
        self.hop_count = hops


class GossipPeerNode:
    """
    Decentralized Anti-Entropy Epidemic Gossip Dissemination Node.
    Ensures probabilistic eventual consistency across distributed edge nodes.
    """
    def __init__(self, peer_id: str, fanout: int = 3, max_hops: int = 6, seed: Optional[int] = None) -> None:
        self.peer_id = peer_id
        self.fanout = fanout
        self.max_hops = max_hops
        self.rng = random.Random(seed)

        self.neighbors: Set[str] = set()
        self.seen_messages: Set[str] = set()
        self.state_table: Dict[str, Any] = {}

    def add_neighbor(self, peer_id: str) -> None:
        if peer_id != self.peer_id:
            self.neighbors.add(peer_id)

    def publish_state(self, key: str, value: Any) -> GossipMessage:
        self.state_table[key] = value
        msg_id = f"{self.peer_id}_{key}_{random.randint(1000, 9999)}"
        self.seen_messages.add(msg_id)
        return GossipMessage(msg_id, self.peer_id, key, value, hops=0)

    def receive_gossip(self, msg: GossipMessage) -> Optional[List[Tuple[str, GossipMessage]]]:
        """
        Processes incoming gossip message and selects fanout neighbors to forward.
        """
        if msg.message_id in self.seen_messages or msg.hop_count >= self.max_hops:
            return None

        self.seen_messages.add(msg.message_id)
        self.state_table[msg.topic] = msg.data

        # Forward to random fanout neighbors
        available = list(self.neighbors - {msg.origin_peer})
        if not available:
            return None

        selected = self.rng.sample(available, min(self.fanout, len(available)))
        forward_msg = GossipMessage(msg.message_id, msg.origin_peer, msg.topic, msg.data, msg.hop_count + 1)
        return [(peer, forward_msg) for peer in selected]
