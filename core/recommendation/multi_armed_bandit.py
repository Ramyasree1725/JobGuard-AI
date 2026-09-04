"""
JobGuard Core Recommendation - Multi-Armed Bandit Algorithms
Implements Epsilon-Greedy, UCB1, and Thompson Sampling (Beta-Bernoulli) algorithms.
"""

import math
import random
from typing import List, Tuple, Optional


class ThompsonSamplingBandit:
    """Beta-Bernoulli Thompson Sampling Multi-Armed Bandit."""

    def __init__(self, num_arms: int):
        self.num_arms = num_arms
        self.alpha = [1.0] * num_arms  # Success counts + 1
        self.beta = [1.0] * num_arms   # Failure counts + 1

    def select_arm(self) -> int:
        """Draw sample from Beta distribution for each arm and select max."""
        samples = [random.betavariate(self.alpha[i], self.beta[i]) for i in range(self.num_arms)]
        return max(range(self.num_arms), key=lambda i: samples[i])

    def update(self, arm: int, reward: float) -> None:
        """Update Beta parameters based on reward (1 = positive feedback, 0 = negative)."""
        if reward > 0.5:
            self.alpha[arm] += 1.0
        else:
            self.beta[arm] += 1.0


class UCB1Bandit:
    """Upper Confidence Bound (UCB1) Multi-Armed Bandit."""

    def __init__(self, num_arms: int):
        self.num_arms = num_arms
        self.counts = [0] * num_arms
        self.values = [0.0] * num_arms
        self.total_pulls = 0

    def select_arm(self) -> int:
        for a in range(self.num_arms):
            if self.counts[a] == 0:
                return a

        ucb_values = [
            self.values[a] + math.sqrt(2.0 * math.log(self.total_pulls) / self.counts[a])
            for a in range(self.num_arms)
        ]
        return max(range(self.num_arms), key=lambda a: ucb_values[a])

    def update(self, arm: int, reward: float) -> None:
        self.total_pulls += 1
        self.counts[arm] += 1
        n = self.counts[arm]
        self.values[arm] = ((n - 1) * self.values[arm] + reward) / n
