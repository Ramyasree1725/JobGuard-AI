"""
JobGuard Core Knowledge - Node2Vec & Random Walk Graph Embedding Engine
Generates dense vector representations for nodes in the threat graph
using second-order biased random walks and Skip-Gram negative sampling.
"""

import math
import random
from typing import Dict, List, Set, Tuple, Optional


class BiasedRandomWalker:
    """Node2Vec biased random walk generator with return (p) and in-out (q) hyper-parameters."""

    def __init__(self, adjacency_list: Dict[str, List[str]], p: float = 1.0, q: float = 1.0):
        self.adj = adjacency_list
        self.p = p  # Return parameter
        self.q = q  # In-out parameter

    def walk(self, start_node: str, walk_length: int = 10) -> List[str]:
        """Generate a single biased random walk starting at start_node."""
        walk = [start_node]
        if start_node not in self.adj or not self.adj[start_node]:
            return walk

        curr = start_node
        prev = None

        for _ in range(walk_length - 1):
            neighbors = self.adj.get(curr, [])
            if not neighbors:
                break

            if prev is None:
                # First step: uniform transition
                next_node = random.choice(neighbors)
            else:
                # Second-order transition probabilities
                weights = []
                prev_neighbors = set(self.adj.get(prev, []))

                for x in neighbors:
                    if x == prev:
                        # d_tx = 0
                        weights.append(1.0 / self.p)
                    elif x in prev_neighbors:
                        # d_tx = 1
                        weights.append(1.0)
                    else:
                        # d_tx = 2
                        weights.append(1.0 / self.q)

                total_w = sum(weights)
                probs = [w / total_w for w in weights]
                
                # Sample next node
                r = random.random()
                cum = 0.0
                next_node = neighbors[-1]
                for n_idx, p_val in enumerate(probs):
                    cum += p_val
                    if r <= cum:
                        next_node = neighbors[n_idx]
                        break

            walk.append(next_node)
            prev = curr
            curr = next_node

        return walk


class GraphEmbeddingSkipGram:
    """Word2Vec Skip-Gram with Negative Sampling for Node2Vec walks."""

    def __init__(self, embed_dim: int = 32, lr: float = 0.025, negative_samples: int = 5):
        self.d = embed_dim
        self.lr = lr
        self.k = negative_samples
        self.node_embeddings: Dict[str, List[float]] = {}
        self.context_embeddings: Dict[str, List[float]] = {}

    def fit(self, walks: List[List[str]], window_size: int = 3, epochs: int = 5) -> "GraphEmbeddingSkipGram":
        all_nodes = list(set(n for w in walks for n in w))
        if not all_nodes:
            return self

        # Initialize embeddings
        for node in all_nodes:
            self.node_embeddings[node] = [random.uniform(-0.1, 0.1) for _ in range(self.d)]
            self.context_embeddings[node] = [random.uniform(-0.1, 0.1) for _ in range(self.d)]

        # Training loop
        for epoch in range(epochs):
            for walk in walks:
                for pos, target in enumerate(walk):
                    start = max(0, pos - window_size)
                    end = min(len(walk), pos + window_size + 1)
                    
                    for ctx_pos in range(start, end):
                        if ctx_pos == pos:
                            continue
                        context = walk[ctx_pos]
                        self._train_pair(target, context, all_nodes)

        return self

    def _sigmoid(self, z: float) -> float:
        return 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, z))))

    def _train_pair(self, target: str, context: str, all_nodes: List[str]) -> None:
        v_target = self.node_embeddings[target]
        v_context = self.context_embeddings[context]

        # Positive update: sigmoid(v_ctx . v_target)
        dot_pos = sum(c * t for c, t in zip(v_context, v_target))
        sig_pos = self._sigmoid(dot_pos)
        grad_pos = (1.0 - sig_pos) * self.lr

        # Negative samples
        neg_samples = [random.choice(all_nodes) for _ in range(self.k)]

        # Update target vector accumulator
        grad_target = [grad_pos * c for c in v_context]

        # Update context vector
        for f in range(self.d):
            self.context_embeddings[context][f] += grad_pos * v_target[f]

        for neg in neg_samples:
            v_neg = self.context_embeddings[neg]
            dot_neg = sum(n * t for n, t in zip(v_neg, v_target))
            sig_neg = self._sigmoid(dot_neg)
            grad_neg = -sig_neg * self.lr

            for f in range(self.d):
                grad_target[f] += grad_neg * v_neg[f]
                self.context_embeddings[neg][f] += grad_neg * v_target[f]

        for f in range(self.d):
            self.node_embeddings[target][f] += grad_target[f]

    def get_embedding(self, node: str) -> List[float]:
        return self.node_embeddings.get(node, [0.0] * self.d)
