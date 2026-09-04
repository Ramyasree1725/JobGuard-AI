"""
JobGuard Backend Service - Scam Graph Database Storage & Fast Traversals
In-memory directed property graph store with path search, shortest distance,
and fraudulent subgraph export for analyst investigations.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class GraphNode:
    id: str
    labels: List[str]
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphRelationship:
    id: str
    source_id: str
    target_id: str
    rel_type: str
    properties: Dict[str, Any] = field(default_factory=dict)


class PropertyGraphStore:
    """Indexed property graph store for fraud ring investigation."""

    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.relationships: Dict[str, GraphRelationship] = {}
        self._out_edges: Dict[str, List[str]] = {}  # node_id -> list of rel_ids
        self._in_edges: Dict[str, List[str]] = {}

    def create_node(self, node_id: str, labels: List[str], properties: Optional[Dict[str, Any]] = None) -> GraphNode:
        node = GraphNode(id=node_id, labels=labels, properties=properties or {})
        self.nodes[node_id] = node
        if node_id not in self._out_edges:
            self._out_edges[node_id] = []
        if node_id not in self._in_edges:
            self._in_edges[node_id] = []
        return node

    def create_relationship(self, rel_id: str, source_id: str, target_id: str, rel_type: str, properties: Optional[Dict[str, Any]] = None) -> GraphRelationship:
        rel = GraphRelationship(id=rel_id, source_id=source_id, target_id=target_id, rel_type=rel_type, properties=properties or {})
        self.relationships[rel_id] = rel
        self._out_edges[source_id].append(rel_id)
        self._in_edges[target_id].append(rel_id)
        return rel

    def shortest_path(self, start_node_id: str, end_node_id: str) -> Optional[List[str]]:
        """BFS shortest path finding node sequence."""
        if start_node_id not in self.nodes or end_node_id not in self.nodes:
            return None
        if start_node_id == end_node_id:
            return [start_node_id]

        visited: Set[str] = {start_node_id}
        queue: List[Tuple[str, List[str]]] = [(start_node_id, [start_node_id])]

        while queue:
            curr, path = queue.pop(0)
            for rel_id in self._out_edges.get(curr, []):
                rel = self.relationships[rel_id]
                target = rel.target_id
                if target == end_node_id:
                    return path + [target]
                if target not in visited:
                    visited.add(target)
                    queue.append((target, path + [target]))

        return None
