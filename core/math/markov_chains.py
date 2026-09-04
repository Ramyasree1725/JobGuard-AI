"""
JobGuard Core Math - Discrete-Time Markov Chains & Stationary Distributions
Computes state transition probabilities, ergodic stationary distributions,
absorbing state absorption probabilities, and hitting times.
"""

from typing import List, Tuple, Dict, Optional


class MarkovChain:
    """Discrete-time finite state Markov Chain analyzer."""

    def __init__(self, states: List[str], transition_matrix: List[List[float]]):
        self.states = states
        self.state_to_idx = {s: i for i, s in enumerate(states)}
        self.P = transition_matrix  # n x n row-stochastic matrix
        self._validate_stochastic()

    def _validate_stochastic(self) -> None:
        n = len(self.states)
        for i, row in enumerate(self.P):
            if len(row) != n:
                raise ValueError(f"Row {i} dimension mismatch: expected {n}, got {len(row)}")
            row_sum = sum(row)
            if abs(row_sum - 1.0) > 1e-4:
                raise ValueError(f"Row {i} does not sum to 1.0 (sums to {row_sum})")

    def step(self, state_dist: List[float]) -> List[float]:
        """Compute next state distribution: \pi_{t+1} = \pi_t * P."""
        n = len(self.states)
        next_dist = [0.0] * n
        for j in range(n):
            next_dist[j] = sum(state_dist[i] * self.P[i][j] for i in range(n))
        return next_dist

    def stationary_distribution(self, max_iter: int = 1000, tol: float = 1e-7) -> List[float]:
        """Compute steady-state stationary distribution via power iteration."""
        n = len(self.states)
        dist = [1.0 / n] * n

        for _ in range(max_iter):
            next_d = self.step(dist)
            diff = sum(abs(next_d[i] - dist[i]) for i in range(n))
            dist = next_d
            if diff < tol:
                break

        return [round(p, 5) for p in dist]
