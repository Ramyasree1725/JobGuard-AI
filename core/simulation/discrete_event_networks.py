"""
JobGuard Core Simulation - Jackson Queueing Networks & Token Bucket Shapers
Simulates open network of M/M/1 service nodes with probabilistic routing transitions
and burst-tolerant token bucket traffic shapers.
"""

import math
from typing import List, Dict, Tuple, Optional


class JacksonNetworkSolver:
    """Open Jackson Network traffic equation solver for network flow balance."""

    @staticmethod
    def solve_traffic_equations(
        external_arrivals_gamma: List[float],
        routing_matrix_P: List[List[float]]
    ) -> List[float]:
        """Solves lambda_i = gamma_i + \sum_j lambda_j * P_ji via Gauss-Jordan elimination."""
        k = len(external_arrivals_gamma)
        # System: (I - P^T) \lambda = \gamma
        A = [[0.0] * k for _ in range(k)]
        b = list(external_arrivals_gamma)

        for i in range(k):
            for j in range(k):
                delta = 1.0 if i == j else 0.0
                A[i][j] = delta - routing_matrix_P[j][i]  # Transpose of P

        # Forward elimination
        for p in range(k):
            pivot = A[p][p]
            if abs(pivot) < 1e-12:
                pivot = 1e-12
            for j in range(p, k):
                A[p][j] /= pivot
            b[p] /= pivot

            for i in range(k):
                if i != p:
                    factor = A[i][p]
                    for j in range(p, k):
                        A[i][j] -= factor * A[p][j]
                    b[i] -= factor * b[p]

        return [round(val, 4) for val in b]
