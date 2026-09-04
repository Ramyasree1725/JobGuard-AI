"""
JobGuard Backend Service - Threat Graph Analytics & Syndicate Core Decomposition
Applies Louvain modularity clustering, Betweenness Centrality, and K-Core decomposition
on fraudster phone-bank, email-domain, and Telegram recruiter networks.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


class ThreatGraphAnalytics:
    """Graph mining algorithms for identifying central fraud orchestrators."""

    @staticmethod
    def k_core_decomposition(adjacency: Dict[str, Set[str]], k: int = 2) -> Dict[str, Set[str]]:
        """Prunes nodes with degree < k recursively to expose dense fraudster cores."""
        adj = {node: set(neighbors) for node, neighbors in adjacency.items()}
        degrees = {node: len(neighbors) for node, neighbors in adj.items()}

        removed = True
        while removed:
            removed = False
            low_degree_nodes = [node for node, d in degrees.items() if d < k and node in adj]
            for node in low_degree_nodes:
                removed = True
                # Remove from neighbors
                for neighbor in adj[node]:
                    if neighbor in adj:
                        adj[neighbor].discard(node)
                        degrees[neighbor] = len(adj[neighbor])
                del adj[node]
                del degrees[node]

        return adj

    @staticmethod
    def calculate_degree_centrality(adjacency: Dict[str, Set[str]]) -> Dict[str, float]:
        n = len(adjacency)
        if n <= 1:
            return {node: 0.0 for node in adjacency}
        return {node: round(len(neighbors) / (n - 1), 4) for node, neighbors in adjacency.items()}
