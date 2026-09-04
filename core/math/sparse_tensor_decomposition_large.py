"""
JobGuard Core Math - Canonical Polyadic (CP/PARAFAC) Tensor Decomposition Large
Decomposes 3-way multi-relational threat tensors (Recruiter x Organization x Scam Type)
into rank-R factor matrices using Alternating Least Squares (ALS) optimization.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import random
import math


class SparseTensorDecompositionLarge:
    """Canonical Polyadic (CP) Tensor Factorization for 3rd-order sparse threat tensors."""

    def __init__(self, rank: int = 4, max_iter: int = 30, lambda_reg: float = 0.01):
        self.rank = rank
        self.max_iter = max_iter
        self.reg = lambda_reg
        self.A: List[List[float]] = []  # Mode-1 factor (I x R)
        self.B: List[List[float]] = []  # Mode-2 factor (J x R)
        self.C: List[List[float]] = []  # Mode-3 factor (K x R)

    def fit(self, non_zero_entries: List[Tuple[int, int, int, float]], shape: Tuple[int, int, int]) -> "SparseTensorDecompositionLarge":
        """Fits CP decomposition: X_ijk ~= sum_r A_ir * B_jr * C_kr."""
        dim_i, dim_j, dim_k = shape
        r = self.rank

        # Initialize factor matrices
        self.A = [[random.uniform(0.1, 0.5) for _ in range(r)] for _ in range(dim_i)]
        self.B = [[random.uniform(0.1, 0.5) for _ in range(r)] for _ in range(dim_j)]
        self.C = [[random.uniform(0.1, 0.5) for _ in range(r)] for _ in range(dim_k)]

        for _ in range(self.max_iter):
            # Update Mode-1 Factor A
            for i in range(dim_i):
                relevant = [e for e in non_zero_entries if e[0] == i]
                for rank_idx in range(r):
                    num = sum((val - sum(self.A[i][t] * self.B[j][t] * self.C[k][t] for t in range(r) if t != rank_idx)) * self.B[j][rank_idx] * self.C[k][rank_idx] for _, j, k, val in relevant)
                    denom = sum((self.B[j][rank_idx] * self.C[k][rank_idx]) ** 2 for _, j, k, _ in relevant) + self.reg
                    self.A[i][rank_idx] = num / max(1e-6, denom)

            # Update Mode-2 Factor B
            for j in range(dim_j):
                relevant = [e for e in non_zero_entries if e[1] == j]
                for rank_idx in range(r):
                    num = sum((val - sum(self.A[i][t] * self.B[j][t] * self.C[k][t] for t in range(r) if t != rank_idx)) * self.A[i][rank_idx] * self.C[k][rank_idx] for i, _, k, val in relevant)
                    denom = sum((self.A[i][rank_idx] * self.C[k][rank_idx]) ** 2 for i, _, k, _ in relevant) + self.reg
                    self.B[j][rank_idx] = num / max(1e-6, denom)

            # Update Mode-3 Factor C
            for k in range(dim_k):
                relevant = [e for e in non_zero_entries if e[2] == k]
                for rank_idx in range(r):
                    num = sum((val - sum(self.A[i][t] * self.B[j][t] * self.C[k][t] for t in range(r) if t != rank_idx)) * self.A[i][rank_idx] * self.B[j][rank_idx] for i, j, _, val in relevant)
                    denom = sum((self.A[i][rank_idx] * self.B[j][rank_idx]) ** 2 for i, j, _, _ in relevant) + self.reg
                    self.C[k][rank_idx] = num / max(1e-6, denom)

        return self

    def predict(self, i: int, j: int, k: int) -> float:
        """Predicts estimated threat intensity tensor value X_ijk."""
        return sum(self.A[i][r] * self.B[j][r] * self.C[k][r] for r in range(self.rank))
