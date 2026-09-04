"""
JobGuard Core Math - Stochastic Matrix Calculus & Markov Transition Algebra
Implements Stationary Distribution Solvers, Fundamental Matrix Computation,
Absorbing Markov Chains, Mean First Passage Times, and PageRank Power Iteration.
"""

import math
from typing import List, Tuple, Optional


class StochasticMatrixCalculus:
    """Matrix algebra for stochastic transition matrices and Markov decision processes."""

    @staticmethod
    def is_stochastic_matrix(P: List[List[float]], tol: float = 1e-5) -> bool:
        """Verifies that all entries are non-negative and every row sums to 1.0."""
        n = len(P)
        for row in P:
            if len(row) != n:
                return False
            if any(val < -tol for val in row):
                return False
            if abs(sum(row) - 1.0) > tol:
                return False
        return True

    @staticmethod
    def stationary_distribution_power(P: List[List[float]], max_iter: int = 200, tol: float = 1e-8) -> List[float]:
        """Calculates stationary distribution vector pi = pi P via power iteration."""
        n = len(P)
        pi = [1.0 / n] * n

        for _ in range(max_iter):
            next_pi = [0.0] * n
            for j in range(n):
                for i in range(n):
                    next_pi[j] += pi[i] * P[i][j]

            # Normalize
            total = sum(next_pi)
            if total > 0:
                next_pi = [v / total for v in next_pi]

            diff = sum(abs(next_pi[k] - pi[k]) for k in range(n))
            pi = next_pi
            if diff < tol:
                break

        return [round(val, 6) for val in pi]

    @staticmethod
    def fundamental_matrix_absorbing(
        Q_transient: List[List[float]]
    ) -> List[List[float]]:
        """Calculates Fundamental Matrix N = (I - Q)^-1 for absorbing Markov chains."""
        t = len(Q_transient)
        # Form (I - Q)
        A = [[0.0] * t for _ in range(t)]
        for i in range(t):
            for j in range(t):
                delta = 1.0 if i == j else 0.0
                A[i][j] = delta - Q_transient[i][j]

        # Gauss-Jordan matrix inversion
        augmented = [[A[i][j] for j in range(t)] + [1.0 if i == j else 0.0 for j in range(t)] for i in range(t)]

        for p in range(t):
            pivot = augmented[p][p]
            if abs(pivot) < 1e-12:
                pivot = 1e-12
            for j in range(2 * t):
                augmented[p][j] /= pivot

            for i in range(t):
                if i != p:
                    factor = augmented[i][p]
                    for j in range(2 * t):
                        augmented[i][j] -= factor * augmented[p][j]

        # Extract inverse
        N = [[augmented[i][t + j] for j in range(t)] for i in range(t)]
        return [[round(val, 5) for val in row] for row in N]
