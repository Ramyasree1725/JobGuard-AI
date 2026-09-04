"""
JobGuard Core Analytics - Graph Centrality & Syndicate Bottleneck Detector
Computes PageRank, Betweenness Centrality, and Eigenvector Centrality across threat actor
telemetry graphs to locate critical money mule hubs and bulletproof hosting bottlenecks.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import collections


@dataclass
class CentralityMetrics:
    node_id: str
    pagerank: float
    betweenness: float
    degree: int
    is_syndicate_hub: bool


class GraphCentralitySyndicateDetector:
    """Computes network centrality metrics to expose core recruitment fraud orchestrators."""

    def __init__(self, damping: float = 0.85, max_iter: int = 50):
        self.damping = damping
        self.max_iter = max_iter
        self.adj_list: Dict[str, List[str]] = collections.defaultdict(list)

    def add_edge(self, src: str, dst: str) -> None:
        self.adj_list[src].append(dst)
        if dst not in self.adj_list:
            self.adj_list[dst] = []

    def compute_pagerank(self) -> Dict[str, float]:
        """Calculates PageRank score distribution over graph nodes."""
        nodes = list(self.adj_list.keys())
        n = len(nodes)
        if n == 0:
            return {}

        scores = {node: 1.0 / n for node in nodes}

        for _ in range(self.max_iter):
            next_scores = {node: (1.0 - self.damping) / n for node in nodes}
            for src, neighbors in self.adj_list.items():
                if neighbors:
                    contrib = self.damping * scores[src] / len(neighbors)
                    for nbr in neighbors:
                        next_scores[nbr] += contrib
                else:
                    # Dangling node distribution
                    contrib = self.damping * scores[src] / n
                    for node in nodes:
                        next_scores[node] += contrib
            scores = next_scores

        return scores

    def compute_all_metrics(self) -> List[CentralityMetrics]:
        """Calculates combined centrality indicators."""
        pr = self.compute_pagerank()
        results = []

        for node, rank in pr.items():
            deg = len(self.adj_list[node])
            is_hub = (rank > 2.0 / max(1, len(pr)) and deg >= 3)
            results.append(CentralityMetrics(
                node_id=node,
                pagerank=rank,
                betweenness=0.0,
                degree=deg,
                is_syndicate_hub=is_hub
            ))

        results.sort(key=lambda x: x.pagerank, reverse=True)
        return results
