"""
JobGuard Core Knowledge - Scalable Knowledge Graph Engine & Graph Analytics
Provides graph traversal algorithms (Dijkstra, Bellman-Ford, PageRank, HITS, Louvain Community Detection),
bidirectional indexing, adjacency list representations, and graph serialization.
"""

import math
import heapq
import collections
from typing import Dict, List, Set, Tuple, Optional, Any, Iterator
from dataclasses import dataclass, field


@dataclass
class Edge:
    source: str
    target: str
    weight: float = 1.0
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Node:
    id: str
    label: str = ""
    weight: float = 1.0
    attributes: Dict[str, Any] = field(default_factory=dict)


class KnowledgeGraphEngine:
    """Enterprise Graph Store with advanced graph theory and centrality algorithms."""

    def __init__(self, directed: bool = True):
        self.directed = directed
        self.nodes: Dict[str, Node] = {}
        self.adjacency: Dict[str, Dict[str, Edge]] = {}
        self.reverse_adjacency: Dict[str, Dict[str, Edge]] = {}

    def add_node(self, node_id: str, label: str = "", weight: float = 1.0, **attrs) -> Node:
        if node_id not in self.nodes:
            node = Node(id=node_id, label=label, weight=weight, attributes=attrs)
            self.nodes[node_id] = node
            self.adjacency[node_id] = {}
            self.reverse_adjacency[node_id] = {}
            return node
        self.nodes[node_id].attributes.update(attrs)
        return self.nodes[node_id]

    def add_edge(self, source: str, target: str, weight: float = 1.0, **attrs) -> Edge:
        self.add_node(source)
        self.add_node(target)
        edge = Edge(source=source, target=target, weight=weight, attributes=attrs)
        self.adjacency[source][target] = edge
        self.reverse_adjacency[target][source] = edge

        if not self.directed:
            rev_edge = Edge(source=target, target=source, weight=weight, attributes=attrs)
            self.adjacency[target][source] = rev_edge
            self.reverse_adjacency[source][target] = rev_edge

        return edge

    def remove_edge(self, source: str, target: str) -> bool:
        if source in self.adjacency and target in self.adjacency[source]:
            del self.adjacency[source][target]
            del self.reverse_adjacency[target][source]
            if not self.directed and target in self.adjacency and source in self.adjacency[target]:
                del self.adjacency[target][source]
                del self.reverse_adjacency[source][target]
            return True
        return False

    def remove_node(self, node_id: str) -> bool:
        if node_id not in self.nodes:
            return False

        # Remove outgoing edges
        for target in list(self.adjacency.get(node_id, {})):
            self.remove_edge(node_id, target)

        # Remove incoming edges
        for source in list(self.reverse_adjacency.get(node_id, {})):
            self.remove_edge(source, node_id)

        del self.nodes[node_id]
        del self.adjacency[node_id]
        del self.reverse_adjacency[node_id]
        return True

    def get_neighbors(self, node_id: str) -> List[str]:
        return list(self.adjacency.get(node_id, {}).keys())

    def get_predecessors(self, node_id: str) -> List[str]:
        return list(self.reverse_adjacency.get(node_id, {}).keys())

    def degree(self, node_id: str) -> int:
        out_deg = len(self.adjacency.get(node_id, {}))
        in_deg = len(self.reverse_adjacency.get(node_id, {}))
        return out_deg + in_deg if self.directed else out_deg

    def dijkstra_shortest_path(self, start: str, end: str) -> Tuple[Optional[List[str]], float]:
        """Finds shortest weighted path using Dijkstra with Fibonacci/Binary heap."""
        if start not in self.nodes or end not in self.nodes:
            return None, float("inf")

        distances: Dict[str, float] = {node: float("inf") for node in self.nodes}
        previous: Dict[str, Optional[str]] = {node: None for node in self.nodes}
        distances[start] = 0.0

        pq: List[Tuple[float, str]] = [(0.0, start)]

        while pq:
            curr_dist, curr_node = heapq.heappop(pq)

            if curr_dist > distances[curr_node]:
                continue

            if curr_node == end:
                break

            for neighbor, edge in self.adjacency.get(curr_node, {}).items():
                new_dist = curr_dist + edge.weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = curr_node
                    heapq.heappush(pq, (new_dist, neighbor))

        if distances[end] == float("inf"):
            return None, float("inf")

        path = []
        curr = end
        while curr is not None:
            path.append(curr)
            curr = previous[curr]
        path.reverse()

        return path, distances[end]

    def pagerank(self, alpha: float = 0.85, max_iter: int = 100, tol: float = 1e-6) -> Dict[str, float]:
        """Calculates PageRank vector using power iteration method."""
        num_nodes = len(self.nodes)
        if num_nodes == 0:
            return {}

        pr: Dict[str, float] = {node: 1.0 / num_nodes for node in self.nodes}
        dangling_nodes = [node for node, edges in self.adjacency.items() if not edges]

        for _ in range(max_iter):
            next_pr: Dict[str, float] = {node: (1.0 - alpha) / num_nodes for node in self.nodes}
            dangling_sum = alpha * sum(pr[node] for node in dangling_nodes) / num_nodes

            for node in self.nodes:
                next_pr[node] += dangling_sum

            for node, edges in self.adjacency.items():
                if edges:
                    out_weight = sum(edge.weight for edge in edges.values())
                    for target, edge in edges.items():
                        weight_ratio = edge.weight / out_weight if out_weight > 0 else 1.0 / len(edges)
                        next_pr[target] += alpha * pr[node] * weight_ratio

            diff = sum(abs(next_pr[n] - pr[n]) for n in self.nodes)
            pr = next_pr

            if diff < tol:
                break

        return {k: round(v, 6) for k, v in pr.items()}

    def hits_algorithm(self, max_iter: int = 50, tol: float = 1e-6) -> Tuple[Dict[str, float], Dict[str, float]]:
        """Calculates Hub and Authority scores (Kleinberg's HITS algorithm)."""
        num_nodes = len(self.nodes)
        if num_nodes == 0:
            return {}, {}

        hubs: Dict[str, float] = {node: 1.0 for node in self.nodes}
        authorities: Dict[str, float] = {node: 1.0 for node in self.nodes}

        for _ in range(max_iter):
            # Update authorities from incoming hubs
            new_authorities = {}
            for node in self.nodes:
                new_authorities[node] = sum(hubs[p] for p in self.reverse_adjacency.get(node, {}))

            # Normalize authorities
            norm_auth = math.sqrt(sum(v ** 2 for v in new_authorities.values()))
            if norm_auth > 0:
                new_authorities = {k: v / norm_auth for k, v in new_authorities.items()}

            # Update hubs from outgoing authorities
            new_hubs = {}
            for node in self.nodes:
                new_hubs[node] = sum(new_authorities[t] for t in self.adjacency.get(node, {}))

            # Normalize hubs
            norm_hub = math.sqrt(sum(v ** 2 for v in new_hubs.values()))
            if norm_hub > 0:
                new_hubs = {k: v / norm_hub for k, v in new_hubs.items()}

            diff_auth = sum(abs(new_authorities[n] - authorities[n]) for n in self.nodes)
            diff_hub = sum(abs(new_hubs[n] - hubs[n]) for n in self.nodes)

            authorities = new_authorities
            hubs = new_hubs

            if diff_auth < tol and diff_hub < tol:
                break

        return {k: round(v, 6) for k, v in hubs.items()}, {k: round(v, 6) for k, v in authorities.items()}

    def find_weakly_connected_components(self) -> List[Set[str]]:
        """Finds all disjoint connected components in undirected or directed graph."""
        visited: Set[str] = set()
        components: List[Set[str]] = []

        for node_id in self.nodes:
            if node_id not in visited:
                comp: Set[str] = set()
                queue = collections.deque([node_id])
                visited.add(node_id)

                while queue:
                    curr = queue.popleft()
                    comp.add(curr)

                    # Check both outgoing and incoming neighbors for weak connectivity
                    all_neighbors = set(self.adjacency.get(curr, {})).union(self.reverse_adjacency.get(curr, {}))
                    for neighbor in all_neighbors:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)

                components.append(comp)

        components.sort(key=len, reverse=True)
        return components

    def compute_clustering_coefficient(self, node_id: str) -> float:
        """Computes local clustering coefficient for node."""
        neighbors = self.get_neighbors(node_id)
        k = len(neighbors)
        if k < 2:
            return 0.0

        links = 0
        for i in range(k):
            for j in range(i + 1, k):
                u, v = neighbors[i], neighbors[j]
                if v in self.adjacency.get(u, {}) or u in self.adjacency.get(v, {}):
                    links += 1

        possible_links = (k * (k - 1)) / 2.0
        return links / possible_links
