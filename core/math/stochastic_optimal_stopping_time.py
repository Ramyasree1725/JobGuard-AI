"""
JobGuard Core Math - Stochastic Optimal Stopping Time & Snell Envelope Engine
Computes dynamic optimal stopping boundaries (Secretary Problem / American Option Formulation)
for determining the exact optimal point to terminate scam campaign telemetry collection.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import math


class StochasticOptimalStoppingTime:
    """Snell envelope backward induction solver for optimal forensic intervention timing."""

    def __init__(self, discount_factor_gamma: float = 0.95):
        self.gamma = discount_factor_gamma

    def compute_snell_envelope(self, payoff_grid: List[List[float]], transition_probs: List[List[List[float]]]) -> List[List[float]]:
        """Computes Snell envelope backward induction: U_t = max(X_t, gamma * E[U_{t+1} | S_t])."""
        num_steps = len(payoff_grid)
        if num_steps == 0:
            return []

        num_states = len(payoff_grid[0])
        u_envelope = [[0.0] * num_states for _ in range(num_steps)]

        # Terminal boundary condition
        for s in range(num_states):
            u_envelope[num_steps - 1][s] = payoff_grid[num_steps - 1][s]

        # Backward induction
        for t in range(num_steps - 2, -1, -1):
            for s in range(num_states):
                immediate_payoff = payoff_grid[t][s]
                expected_continuation = sum(
                    transition_probs[t][s][next_s] * u_envelope[t + 1][next_s]
                    for next_s in range(num_states)
                ) if t < len(transition_probs) else 0.0

                u_envelope[t][s] = max(immediate_payoff, self.gamma * expected_continuation)

        return u_envelope

    def should_intervene_now(self, current_payoff: float, expected_continuation_value: float) -> bool:
        """Determines if the optimal stopping rule triggers immediate intervention."""
        return current_payoff >= (self.gamma * expected_continuation_value)
