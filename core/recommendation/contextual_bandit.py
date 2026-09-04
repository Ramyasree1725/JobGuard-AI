"""
JobGuard Core Recommendation - LinUCB & Thompson Sampling Contextual Bandits
Balances exploration and exploitation for dynamic UI alert ranking and verification advice.
"""

import math
import random
from typing import List, Dict, Tuple, Optional


class LinUCBBandit:
    """Disjoint Linear Upper Confidence Bound (LinUCB) contextual bandit."""

    def __init__(self, num_arms: int, feature_dim: int, alpha: float = 1.0):
        self.num_arms = num_arms
        self.d = feature_dim
        self.alpha = alpha

        # A_a = I_d, b_a = 0_d for each arm
        self.A = [[[1.0 if i == j else 0.0 for j in range(self.d)] for i in range(self.d)] for _ in range(num_arms)]
        self.b = [[0.0] * self.d for _ in range(num_arms)]

    def select_arm(self, context_vector: List[float]) -> int:
        best_arm = 0
        max_ucb = -float("inf")

        for a in range(self.num_arms):
            # Theta_a = A_a^-1 * b_a (diagonal inverse approximation)
            theta_a = [self.b[a][i] / max(1e-4, self.A[a][i][i]) for i in range(self.d)]
            
            # Expected reward = x^T theta_a
            expected_reward = sum(context_vector[i] * theta_a[i] for i in range(self.d))
            
            # Variance = sqrt(x^T A_a^-1 x)
            variance = math.sqrt(sum((context_vector[i] ** 2) / max(1e-4, self.A[a][i][i]) for i in range(self.d)))
            
            ucb = expected_reward + self.alpha * variance

            if ucb > max_ucb:
                max_ucb = ucb
                best_arm = a

        return best_arm

    def update(self, chosen_arm: int, context_vector: List[float], reward: float) -> None:
        """Update covariance matrix and response vector."""
        a = chosen_arm
        for i in range(self.d):
            self.A[a][i][i] += context_vector[i] ** 2
            self.b[a][i] += reward * context_vector[i]
