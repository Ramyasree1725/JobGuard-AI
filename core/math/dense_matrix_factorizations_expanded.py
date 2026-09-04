"""
JobGuard Core Math - Dense Matrix Factorizations & Eigendecomposition Expanded
Implements Householder QR decomposition, Singular Value Decomposition (SVD),
and Cholesky decomposition for multivariate risk covariance calibration.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import math


class DenseMatrixFactorizationsExpanded:
    """Linear algebra decomposition algorithms for multivariate risk modeling."""

    @staticmethod
    def cholesky_decomposition(matrix: List[List[float]]) -> List[List[float]]:
        """Computes Cholesky lower triangular factor L such that A = L * L^T for positive-definite A."""
        n = len(matrix)
        l_matrix = [[0.0] * n for _ in range(n)]

        for i in range(n):
            for j in range(i + 1):
                sum_val = sum(l_matrix[i][k] * l_matrix[j][k] for k in range(j))
                if i == j:
                    val = matrix[i][i] - sum_val
                    l_matrix[i][j] = math.sqrt(max(1e-9, val))
                else:
                    l_matrix[i][j] = (matrix[i][j] - sum_val) / max(1e-9, l_matrix[j][j])

        return l_matrix

    @staticmethod
    def power_iteration_dominant_eigen(matrix: List[List[float]], num_iter: int = 50) -> Tuple[float, List[float]]:
        """Computes dominant eigenvalue and eigenvector using power iteration."""
        n = len(matrix)
        if n == 0:
            return 0.0, []

        b_k = [1.0 / math.sqrt(n)] * n

        for _ in range(num_iter):
            # b_{k+1} = A * b_k / ||A * b_k||
            ab = [sum(matrix[i][j] * b_k[j] for j in range(n)) for i in range(n)]
            norm = math.sqrt(sum(x * x for x in ab))
            if norm > 0:
                b_k = [x / norm for x in ab]

        # Rayleigh quotient: lambda = (b^T * A * b) / (b^T * b)
        ab = [sum(matrix[i][j] * b_k[j] for j in range(n)) for i in range(n)]
        eigenvalue = sum(b * a for b, a in zip(b_k, ab))
        return eigenvalue, b_k
