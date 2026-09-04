"""
JobGuard Core Recommendation - LightGCN Graph Neural Collaborative Filtering
Implements neighborhood aggregation and multi-hop embedding propagation
over bipartite candidate-job verification graphs.
"""

from typing import List, Dict, Tuple, Optional


class LightGCNLayer:
    """Simplified Graph Convolution without non-linearities for fast recommendation."""

    def __init__(self, num_users: int, num_items: int, embed_dim: int = 16):
        self.num_users = num_users
        self.num_items = num_items
        self.embed_dim = embed_dim

    def propagate(
        self,
        user_embeddings: List[List[float]],
        item_embeddings: List[List[float]],
        adjacency: Dict[int, List[int]]  # user_id -> list of item_ids
    ) -> Tuple[List[List[float]], List[List[float]]]:
        """Aggregate 1-hop neighbor embeddings."""
        new_users = [[0.0] * self.embed_dim for _ in range(self.num_users)]
        new_items = [[0.0] * self.embed_dim for _ in range(self.num_items)]

        # User aggregation from items
        for u in range(self.num_users):
            items = adjacency.get(u, [])
            deg_u = len(items)
            if deg_u == 0:
                new_users[u] = list(user_embeddings[u])
                continue

            for i in items:
                scale = 1.0 / deg_u
                for f in range(self.embed_dim):
                    new_users[u][f] += scale * item_embeddings[i][f]

        return new_users, item_embeddings
