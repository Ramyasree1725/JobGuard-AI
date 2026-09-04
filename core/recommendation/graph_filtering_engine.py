"""
JobGuard Core Recommendation - PinSage & Random Walk Graph Filtering Engine
Simulates localized random walks with restart (RWR) and neighborhood aggregation
over bipartite job-applicant and company-recruiter verification graphs.
"""

import math
import random
from typing import List, Dict, Tuple, Set, Optional


class RandomWalkWithRestart:
    """Random Walk with Restart (RWR) personalized PageRank score accumulator."""

    def __init__(self, adjacency: Dict[str, List[str]], restart_prob: float = 0.15):
        self.adj = adjacency
        self.c = restart_prob

    def compute_proximity(self, source_node: str, num_walks: int = 500, walk_length: int = 15) -> Dict[str, float]:
        """Runs random walks with restart from source_node to measure structural affinity."""
        visit_counts: Dict[str, int] = {}
        total_visits = 0

        for _ in range(num_walks):
            curr = source_node
            for _ in range(walk_length):
                # Chance of restart
                if random.random() < self.c or curr not in self.adj or not self.adj[curr]:
                    curr = source_node
                else:
                    curr = random.choice(self.adj[curr])

                visit_counts[curr] = visit_counts.get(curr, 0) + 1
                total_visits += 1

        return {node: round(cnt / total_visits, 5) for node, cnt in visit_counts.items()}
