"""
JobGuard Core Recommendation - Matrix Factorization & SVD RecSys
Implements Alternating Least Squares (ALS) and Singular Value Decomposition (SVD)
to recommend verified legitimate career openings based on candidate profile affinities.
"""

import math
import random
from typing import List, Tuple, Dict, Optional


class MatrixFactorizationSVD:
    """Regularized Singular Value Decomposition with Stochastic Gradient Descent."""

    def __init__(self, num_factors: int = 16, lr: float = 0.01, reg: float = 0.05, epochs: int = 20):
        self.k = num_factors
        self.lr = lr
        self.reg = reg
        self.epochs = epochs

        self.user_factors: Dict[int, List[float]] = {}
        self.item_factors: Dict[int, List[float]] = {}
        self.global_mean: float = 0.0

    def fit(self, ratings: List[Tuple[int, int, float]]) -> "MatrixFactorizationSVD":
        if not ratings:
            return self

        self.global_mean = sum(r for _, _, r in ratings) / len(ratings)

        # Initialize latent factor vectors
        users = set(u for u, _, _ in ratings)
        items = set(i for _, i, _ in ratings)

        for u in users:
            self.user_factors[u] = [random.uniform(-0.1, 0.1) for _ in range(self.k)]
        for i in items:
            self.item_factors[i] = [random.uniform(-0.1, 0.1) for _ in range(self.k)]

        # SGD training loop
        for _ in range(self.epochs):
            for u, i, r in ratings:
                p_u = self.user_factors[u]
                q_i = self.item_factors[i]

                # Prediction = dot product
                pred = sum(p_u[f] * q_i[f] for f in range(self.k))
                err = r - pred

                for f in range(self.k):
                    p_old = p_u[f]
                    q_old = q_i[f]
                    p_u[f] += self.lr * (err * q_old - self.reg * p_old)
                    q_i[f] += self.lr * (err * p_old - self.reg * q_old)

        return self

    def predict(self, user_id: int, item_id: int) -> float:
        if user_id not in self.user_factors or item_id not in self.item_factors:
            return self.global_mean
        p_u = self.user_factors[user_id]
        q_i = self.item_factors[item_id]
        return round(sum(p_u[f] * q_i[f] for f in range(self.k)), 3)
