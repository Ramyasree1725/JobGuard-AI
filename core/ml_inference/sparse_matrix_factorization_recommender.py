"""
JobGuard Core ML Inference - Alternating Least Squares (ALS) Sparse Matrix Factorization
Decomposes high-dimensional sparse candidate-job interaction matrices into low-rank
latent feature representations with L2 Tikhonov regularization.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import random
import math


class SparseMatrixFactorizationRecommender:
    """Alternating Least Squares (ALS) solver for sparse latent factor collaborative filtering."""

    def __init__(self, num_factors: int = 16, reg_lambda: float = 0.05, num_iterations: int = 10):
        self.num_factors = num_factors
        self.reg_lambda = reg_lambda
        self.num_iterations = num_iterations
        self.user_factors: Dict[int, List[float]] = {}
        self.item_factors: Dict[int, List[float]] = {}

    def fit(self, ratings: List[Tuple[int, int, float]]) -> "SparseMatrixFactorizationRecommender":
        """Fits latent factor vectors U and V using coordinate descent."""
        users = set(u for u, i, r in ratings)
        items = set(i for u, i, r in ratings)

        # Initialize factors randomly
        for u in users:
            self.user_factors[u] = [random.uniform(-0.1, 0.1) for _ in range(self.num_factors)]
        for i in items:
            self.item_factors[i] = [random.uniform(-0.1, 0.1) for _ in range(self.num_factors)]

        # Group ratings
        user_ratings: Dict[int, List[Tuple[int, float]]] = {}
        item_ratings: Dict[int, List[Tuple[int, float]]] = {}

        for u, i, r in ratings:
            user_ratings.setdefault(u, []).append((i, r))
            item_ratings.setdefault(i, []).append((u, r))

        for _ in range(self.num_iterations):
            # Optimize user factors
            for u, i_list in user_ratings.items():
                for f in range(self.num_factors):
                    num = sum((r - sum(self.user_factors[u][k] * self.item_factors[i][k] for k in range(self.num_factors) if k != f)) * self.item_factors[i][f] for i, r in i_list)
                    denom = sum(self.item_factors[i][f] ** 2 for i, _ in i_list) + self.reg_lambda
                    self.user_factors[u][f] = num / max(1e-6, denom)

            # Optimize item factors
            for i, u_list in item_ratings.items():
                for f in range(self.num_factors):
                    num = sum((r - sum(self.user_factors[u][k] * self.item_factors[i][k] for k in range(self.num_factors) if k != f)) * self.user_factors[u][f] for u, r in u_list)
                    denom = sum(self.user_factors[u][f] ** 2 for u, _ in u_list) + self.reg_lambda
                    self.item_factors[i][f] = num / max(1e-6, denom)

        return self

    def predict(self, user_id: int, item_id: int) -> float:
        """Predicts affinity dot product between user and job item."""
        u_vec = self.user_factors.get(user_id)
        i_vec = self.item_factors.get(item_id)
        if not u_vec or not i_vec:
            return 0.50
        return sum(u * i for u, i in zip(u_vec, i_vec))
