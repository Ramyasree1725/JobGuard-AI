"""
JobGuard Backend Service - Threat Network Graph Analysis Engine
Constructs multi-relational graphs of scam syndicates, shared UPI IDs,
burner WhatsApp numbers, and disposable hosting providers.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class ThreatNode:
    node_id: str
    node_type: str  # "entity", "phone", "domain", "upi_id", "email"
    risk_score: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ThreatEdge:
    source_id: str
    target_id: str
    relation_type: str  # "USES_DOMAIN", "COLLECTS_VIA_UPI", "COMMUNICATES_ON"
    weight: float = 1.0


class ThreatNetworkGraph:
    """Multi-relational graph store with connected component clustering."""

    def __init__(self):
        self.nodes: Dict[str, ThreatNode] = {}
        self.edges: List[ThreatEdge] = []
        self._adjacency: Dict[str, Set[str]] = {}

    def add_node(self, node: ThreatNode) -> None:
        self.nodes[node.node_id] = node
        if node.node_id not in self._adjacency:
            self._adjacency[node.node_id] = set()

    def add_edge(self, edge: ThreatEdge) -> None:
        self.edges.append(edge)
        self.add_node(ThreatNode(edge.source_id, "entity", 50.0)) if edge.source_id not in self.nodes else None
        self.add_node(ThreatNode(edge.target_id, "entity", 50.0)) if edge.target_id not in self.nodes else None
        self._adjacency[edge.source_id].add(edge.target_id)
        self._adjacency[edge.target_id].add(edge.source_id)

    def find_connected_syndicates(self) -> List[List[str]]:
        """Find all disjoint fraud syndicate clusters using BFS."""
        visited: Set[str] = set()
        clusters: List[List[str]] = []

        for node_id in self.nodes:
            if node_id not in visited:
                cluster = []
                queue = [node_id]
                visited.add(node_id)

                while queue:
                    curr = queue.pop(0)
                    cluster.append(curr)
                    for neighbor in self._adjacency.get(curr, set()):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                
                clusters.append(cluster)

        clusters.sort(key=len, reverse=True)
        return clusters

    def calculate_cluster_risk(self, cluster_nodes: List[str]) -> float:
        """Compute aggregate risk for a connected cluster."""
        scores = [self.nodes[nid].risk_score for nid in cluster_nodes if nid in self.nodes]
        return round(max(scores) if scores else 0.0, 1)
