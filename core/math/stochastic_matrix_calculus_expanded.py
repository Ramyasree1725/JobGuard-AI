"""
JobGuard Core Math - Stochastic Matrix Calculus & Markov Transition Matrices Expanded
Computes stationary probability distributions, fundamental matrices, and hitting times
for discrete-time Markov chains modeling victim progression through scam recruitment funnels.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


class StochasticMatrixCalculusExpanded:
    """Calculus and spectral analysis on right-stochastic transition probability matrices."""

    @staticmethod
    def power_method_stationary_distribution(
        transition_matrix: List[List[float]],
        num_iterations: int = 100
    ) -> List[float]:
        """Computes left eigenvector pi such that pi * P = pi using the power method."""
        n = len(transition_matrix)
        if n == 0:
            return []

        # Uniform initial distribution
        pi = [1.0 / n] * n

        for _ in range(num_iterations):
            next_pi = [0.0] * n
            for j in range(n):
                for i in range(n):
                    next_pi[j] += pi[i] * transition_matrix[i][j]
            pi = next_pi

        return pi

    @staticmethod
    def expected_absorption_time(
        q_transient_submatrix: List[List[float]],
        num_transient: int
    ) -> List[float]:
        """Computes expected steps to absorption from each transient state: t = (I - Q)^-1 * 1."""
        # Solves (I - Q) * t = 1 via Gauss-Jordan elimination
        n = num_transient
        aug = [[(1.0 if i == j else 0.0) - q_transient_submatrix[i][j] for j in range(n)] + [1.0] for i in range(n)]

        for i in range(n):
            pivot = aug[i][i]
            if abs(pivot) < 1e-9:
                pivot = 1e-9
            for j in range(n + 1):
                aug[i][j] /= pivot

            for k in range(n):
                if k != i:
                    factor = aug[k][i]
                    for j in range(n + 1):
                        aug[k][j] -= factor * aug[i][j]

        return [aug[i][n] for i in range(n)]
