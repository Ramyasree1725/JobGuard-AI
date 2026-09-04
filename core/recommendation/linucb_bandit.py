"""
Aetheris Recommendation & RL: Contextual LinUCB & Thompson Sampling Bandits
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
import random
from typing import List, Dict, Tuple, Sequence, Optional
from core.math.matrices import MatrixDense


class LinUCBArm:
    """Individual Arm in LinUCB with Ridge Regression state."""
    def __init__(self, arm_id: int, feature_dim: int, alpha: float = 1.0) -> None:
        self.arm_id = arm_id
        self.dim = feature_dim
        self.alpha = float(alpha)
        
        # A_a = I_d (feature_dim x feature_dim)
        self.A = MatrixDense(self.dim, self.dim)
        for i in range(self.dim):
            self.A[i][i] = 1.0
            
        # b_a = 0_d
        self.b = [0.0] * self.dim
        self.theta_hat = [0.0] * self.dim
        self.pull_count = 0

    def compute_ucb_score(self, context: Sequence[float]) -> float:
        """
        Computes Upper Confidence Bound score:
        p_{t, a} = theta_a^T * x_{t, a} + alpha * sqrt( x_{t, a}^T * A_a^-1 * x_{t, a} )
        """
        # theta_hat = A^-1 * b
        try:
            self.theta_hat = self.A.solve_linear_system_gaussian(self.b)
        except ValueError:
            pass

        # Expected reward: theta^T * x
        expected_reward = sum(self.theta_hat[i] * context[i] for i in range(self.dim))

        # Variance term: x^T * A^-1 * x
        try:
            a_inv_x = self.A.solve_linear_system_gaussian(list(context))
            variance_term = math.sqrt(max(0.0, sum(context[i] * a_inv_x[i] for i in range(self.dim))))
        except ValueError:
            variance_term = 1.0

        return expected_reward + self.alpha * variance_term

    def update(self, context: Sequence[float], reward: float) -> None:
        """
        A_a = A_a + x * x^T
        b_a = b_a + r * x
        """
        for r in range(self.dim):
            self.b[r] += reward * context[r]
            for c in range(self.dim):
                self.A[r][c] += context[r] * context[c]
        self.pull_count += 1


class LinUCBContextualBandit:
    """
    Contextual Multi-Armed Bandit using Disjoint Linear Upper Confidence Bound (Li et al.).
    Balancing exploration and exploitation across dynamic context vectors.
    """
    def __init__(self, num_arms: int, feature_dim: int, alpha: float = 1.0) -> None:
        self.num_arms = num_arms
        self.dim = feature_dim
        self.alpha = alpha
        self.arms = [LinUCBArm(i, feature_dim, alpha) for i in range(num_arms)]

    def select_arm(self, context: Sequence[float]) -> int:
        best_arm = 0
        best_score = -float('inf')

        for arm in self.arms:
            score = arm.compute_ucb_score(context)
            if score > best_score:
                best_score = score
                best_arm = arm.arm_id

        return best_arm

    def update_reward(self, arm_id: int, context: Sequence[float], reward: float) -> None:
        if 0 <= arm_id < self.num_arms:
            self.arms[arm_id].update(context, reward)


class ThompsonSamplingBandit:
    """Beta-Bernoulli Thompson Sampling Multi-Armed Bandit."""
    def __init__(self, num_arms: int, seed: Optional[int] = None) -> None:
        self.num_arms = num_arms
        self.alpha_params = [1.0] * num_arms # Success counts + prior
        self.beta_params = [1.0] * num_arms  # Failure counts + prior
        self.rng = random.Random(seed)

    def select_arm(self) -> int:
        samples = [
            self.rng.betavariate(self.alpha_params[i], self.beta_params[i])
            for i in range(self.num_arms)
        ]
        return max(range(self.num_arms), key=lambda i: samples[i])

    def update(self, arm_id: int, success: bool) -> None:
        if 0 <= arm_id < self.num_arms:
            if success:
                self.alpha_params[arm_id] += 1.0
            else:
                self.beta_params[arm_id] += 1.0
