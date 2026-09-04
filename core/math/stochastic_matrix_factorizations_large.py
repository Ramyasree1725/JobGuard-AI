"""
JobGuard Core Math - Stochastic Non-Negative Matrix Factorization (NMF) Large
Implements multiplicative update rules, Kullback-Leibler (KL) divergence minimization,
and Frobenius norm optimization for topic decomposition of recruitment fraud transcripts.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import random
import math


class StochasticMatrixFactorizationsLarge:
    """Non-Negative Matrix Factorization (NMF) solver for discovery of latent scam topics."""

    def __init__(self, num_topics: int = 8, max_iter: int = 50, epsilon: float = 1e-9):
        self.num_topics = num_topics
        self.max_iter = max_iter
        self.epsilon = epsilon
        self.W: List[List[float]] = []  # Document-Topic matrix (n x k)
        self.H: List[List[float]] = []  # Topic-Word matrix (k x m)

    def fit_transform(self, V: List[List[float]]) -> List[List[float]]:
        """Decomposes non-negative matrix V ~= W * H using Lee & Seung multiplicative update rules."""
        n = len(V)
        if n == 0:
            return []
        m = len(V[0])
        k = self.num_topics

        # Initialize W and H with non-negative random values
        self.W = [[random.uniform(0.1, 1.0) for _ in range(k)] for _ in range(n)]
        self.H = [[random.uniform(0.1, 1.0) for _ in range(m)] for _ in range(k)]

        for _ in range(self.max_iter):
            # Update H: H = H * (W^T * V) / (W^T * W * H + eps)
            # 1. WT_V = W^T * V (k x m)
            wt_v = [[sum(self.W[i][t] * V[i][j] for i in range(n)) for j in range(m)] for t in range(k)]
            # 2. WT_W = W^T * W (k x k)
            wt_w = [[sum(self.W[i][t1] * self.W[i][t2] for i in range(n)) for t2 in range(k)] for t1 in range(k)]
            # 3. WT_W_H = WT_W * H (k x m)
            wt_w_h = [[sum(wt_w[t1][t2] * self.H[t2][j] for t2 in range(k)) for j in range(m)] for t1 in range(k)]

            for t in range(k):
                for j in range(m):
                    self.H[t][j] *= (wt_v[t][j] / max(self.epsilon, wt_w_h[t][j]))

            # Update W: W = W * (V * H^T) / (W * H * H^T + eps)
            # 1. V_HT = V * H^T (n x k)
            v_ht = [[sum(V[i][j] * self.H[t][j] for j in range(m)) for t in range(k)] for i in range(n)]
            # 2. H_HT = H * H^T (k x k)
            h_ht = [[sum(self.H[t1][j] * self.H[t2][j] for j in range(m)) for t2 in range(k)] for t1 in range(k)]
            # 3. W_H_HT = W * H_HT (n x k)
            w_h_ht = [[sum(self.W[i][t2] * h_ht[t2][t1] for t2 in range(k)) for t1 in range(k)] for i in range(n)]

            for i in range(n):
                for t in range(k):
                    self.W[i][t] *= (v_ht[i][t] / max(self.epsilon, w_h_ht[i][t]))

        return self.W
