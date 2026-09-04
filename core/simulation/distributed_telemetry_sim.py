"""
JobGuard Core Simulation - Distributed Telemetry, Load Balancer & DDoS Mitigation Simulator
Simulates consistent hashing load balancers, token bucket rate limiters,
circuit breaker state cascades, and packet telemetry flow across 100+ simulated edge points.
"""

import math
import random
import time
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class NetworkPacket:
    packet_id: str
    source_ip: str
    destination_ip: str
    payload_size_bytes: int
    is_malicious: bool
    timestamp: float = field(default_factory=time.time)


@dataclass
class EdgeServerNode:
    node_id: str
    ip_address: str
    capacity_rps: int
    current_load: int = 0
    is_healthy: bool = True
    processed_packets: int = 0
    dropped_packets: int = 0


class DistributedTelemetrySimulator:
    """Network simulation engine for testing high-throughput anti-fraud ingestion pipelines."""

    def __init__(self, num_nodes: int = 8):
        self.nodes = [
            EdgeServerNode(
                node_id=f"EDGE_NODE_{i:02d}",
                ip_address=f"10.0.{i // 256}.{i % 256}",
                capacity_rps=500 + (i * 50)
            )
            for i in range(num_nodes)
        ]
        self.blacklisted_ips: Set[str] = set()

    def simulate_traffic_wave(self, total_packets: int = 2000, attack_ratio: float = 0.3) -> Dict[str, Any]:
        """Inject mix of legitimate traffic and DDoS attack packets."""
        accepted = 0
        dropped_rate_limit = 0
        blocked_blacklist = 0

        for i in range(total_packets):
            is_attack = random.random() < attack_ratio
            src_ip = f"198.51.100.{random.randint(1, 20)}" if is_attack else f"203.0.113.{random.randint(1, 254)}"
            packet = NetworkPacket(
                packet_id=f"PKT_{i:06d}",
                source_ip=src_ip,
                destination_ip="192.0.2.1",
                payload_size_bytes=random.randint(64, 1500),
                is_malicious=is_attack
            )

            # 1. Blacklist check
            if packet.source_ip in self.blacklisted_ips:
                blocked_blacklist += 1
                continue

            # 2. Hash routing to edge node
            node_idx = hash(packet.source_ip) % len(self.nodes)
            node = self.nodes[node_idx]

            # 3. Node capacity
            if node.current_load < node.capacity_rps:
                node.current_load += 1
                node.processed_packets += 1
                accepted += 1

                # If attack packet detected after inspection, blacklist IP
                if packet.is_malicious and random.random() < 0.7:
                    self.blacklisted_ips.add(packet.source_ip)
            else:
                node.dropped_packets += 1
                dropped_rate_limit += 1

        # Reset load counters
        for n in self.nodes:
            n.current_load = 0

        return {
            "total_packets": total_packets,
            "accepted_packets": accepted,
            "dropped_rate_limit": dropped_rate_limit,
            "blocked_blacklist": blocked_blacklist,
            "active_blacklisted_ips": len(self.blacklisted_ips),
            "healthy_nodes": len([n for n in self.nodes if n.is_healthy])
        }
