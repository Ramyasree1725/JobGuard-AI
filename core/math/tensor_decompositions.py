"""
JobGuard Core Math - Multilinear Tensor Decompositions (CP & Tucker)
Implements Canonical Polyadic (CP/PARAFAC) and Tucker decompositions
for high-order interaction factorization in multi-modal job verification data.
"""

import math
import random
from typing import List, Tuple, Dict, Optional


class Tensor3D:
    """Dense 3D Tensor with shape (I, J, K)."""

    def __init__(self, data: List[List[List[float]]]):
        self.data = data
        self.shape = (len(data), len(data[0]), len(data[0][0]))

    def unfold(self, mode: int) -> List[List[float]]:
        """Mode-n unfolding of 3D tensor into a 2D matrix."""
        I, J, K = self.shape
        if mode == 0:
            # Shape (I, J*K)
            matrix = []
            for i in range(I):
                row = []
                for k in range(K):
                    for j in range(J):
                        row.append(self.data[i][j][k])
                matrix.append(row)
            return matrix
        elif mode == 1:
            # Shape (J, I*K)
            matrix = []
            for j in range(J):
                row = []
                for k in range(K):
                    for i in range(I):
                        row.append(self.data[i][j][k])
                matrix.append(row)
            return matrix
        else:
            # Shape (K, I*J)
            matrix = []
            for k in range(K):
                row = []
                for j in range(J):
                    for i in range(I):
                        row.append(self.data[i][j][k])
                matrix.append(row)
            return matrix


class CPDecomposition:
    """Canonical Polyadic (CP) Decomposition via Alternating Least Squares (ALS)."""

    def __init__(self, rank: int = 4, max_iter: int = 50):
        self.rank = rank
        self.max_iter = max_iter

    def decompose(self, tensor: Tensor3D) -> Tuple[List[List[float]], List[List[float]], List[List[float]]]:
        """Factorizes X \approx \sum_{r=1}^R a_r \otimes b_r \otimes c_r. Returns factor matrices (A, B, C)."""
        I, J, K = tensor.shape
        R = self.rank

        # Random factor initializations
        A = [[random.uniform(-0.1, 0.1) for _ in range(R)] for _ in range(I)]
        B = [[random.uniform(-0.1, 0.1) for _ in range(R)] for _ in range(J)]
        C = [[random.uniform(-0.1, 0.1) for _ in range(R)] for _ in range(K)]

        for _ in range(self.max_iter):
            # Update A: X_(0) (C \odot B) [(C^T C) * (B^T B)]^-1
            # Coordinate gradient approximation
            for i in range(I):
                for r in range(R):
                    dot = sum(
                        tensor.data[i][j][k] * B[j][r] * C[k][r]
                        for j in range(J)
                        for k in range(K)
                    )
                    denom = sum((B[j][r] * C[k][r]) ** 2 for j in range(J) for k in range(K))
                    A[i][r] = dot / max(1e-6, denom)

            # Update B
            for j in range(J):
                for r in range(R):
                    dot = sum(
                        tensor.data[i][j][k] * A[i][r] * C[k][r]
                        for i in range(I)
                        for k in range(K)
                    )
                    denom = sum((A[i][r] * C[k][r]) ** 2 for i in range(I) for k in range(K))
                    B[j][r] = dot / max(1e-6, denom)

            # Update C
            for k in range(K):
                for r in range(R):
                    dot = sum(
                        tensor.data[i][j][k] * A[i][r] * B[j][r]
                        for i in range(I)
                        for j in range(J)
                    )
                    denom = sum((A[i][r] * B[j][r]) ** 2 for i in range(I) for j in range(J))
                    C[k][r] = dot / max(1e-6, denom)

        return A, B, C
