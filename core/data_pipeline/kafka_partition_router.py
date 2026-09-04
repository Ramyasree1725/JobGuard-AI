"""
JobGuard Core Data Pipeline - Distributed Partition Router & Sharding Key Engine
Computes consistent hash partition routing, virtual node tokens, murmur3 hashing,
and dynamic partition rebalancing for high-throughput fraud telemetry streaming.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import hashlib
import bisect


@dataclass
class StreamPartition:
    partition_id: int
    leader_broker_id: str
    assigned_replicas: List[str]
    current_high_watermark: int = 0
    is_in_sync: bool = True


class KafkaPartitionRouter:
    """Computes deterministic partition assignment using consistent hashing with virtual nodes."""

    def __init__(self, partition_count: int = 16, virtual_replicas: int = 100):
        self.partition_count = partition_count
        self.virtual_replicas = virtual_replicas
        self.ring: List[Tuple[int, int]] = []  # (hash_token, partition_id)
        self.partitions: Dict[int, StreamPartition] = {}
        self._build_ring()

    def _build_ring(self) -> None:
        """Initializes the virtual token ring for partitions."""
        self.ring.clear()
        for p_id in range(self.partition_count):
            self.partitions[p_id] = StreamPartition(
                partition_id=p_id,
                leader_broker_id=f"broker-node-{p_id % 3}",
                assigned_replicas=[f"broker-node-{p_id % 3}", f"broker-node-{(p_id + 1) % 3}"]
            )
            for v in range(self.virtual_replicas):
                token_str = f"partition-{p_id}-vnode-{v}"
                token_hash = int(hashlib.md5(token_str.encode()).hexdigest()[:8], 16)
                self.ring.append((token_hash, p_id))

        self.ring.sort()

    def route_key(self, routing_key: str) -> int:
        """Maps a business key (e.g., candidate_id, company_name) to target partition ID."""
        if not routing_key:
            return 0

        key_hash = int(hashlib.md5(routing_key.encode()).hexdigest()[:8], 16)
        
        # Binary search on token ring
        tokens = [t[0] for t in self.ring]
        idx = bisect.bisect_right(tokens, key_hash)
        if idx == len(self.ring):
            idx = 0

        return self.ring[idx][1]

    def get_partition_metadata(self, partition_id: int) -> Optional[StreamPartition]:
        return self.partitions.get(partition_id)
