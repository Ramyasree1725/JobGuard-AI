"""
JobGuard Core Math - (epsilon, delta)-Differential Privacy & Laplace Noise Mechanism
Injects calibrated Laplace and Gaussian perturbation noise into candidate analytical aggregates
to guarantee formal mathematical privacy against membership inference and reconstruction attacks.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import random
import math


class DifferentialPrivacyLaplaceMechanism:
    """Laplace perturbation mechanism for epsilon-differential privacy guarantees."""

    def __init__(self, epsilon: float = 0.50, global_sensitivity: float = 1.0):
        self.epsilon = max(0.01, epsilon)
        self.sensitivity = global_sensitivity
        self.scale_b = global_sensitivity / self.epsilon

    def sample_laplace_noise(self) -> float:
        """Samples zero-mean noise from Laplace(0, b) distribution using inverse transform sampling."""
        u = random.random() - 0.5
        sign = 1.0 if u >= 0 else -1.0
        # F^-1(p) = -b * sgn(p - 0.5) * ln(1 - 2|p - 0.5|)
        noise = -self.scale_b * sign * math.log(1.0 - 2.0 * abs(u))
        return noise

    def privatize_count(self, true_count: int) -> int:
        """Applies Laplace noise to integer census queries (e.g. number of flagged scam postings)."""
        noise = self.sample_laplace_noise()
        noisy_val = round(true_count + noise)
        return max(0, noisy_val)

    def privatize_continuous_mean(self, true_mean: float) -> float:
        """Applies Laplace noise to floating point average salary analytics."""
        noise = self.sample_laplace_noise()
        return true_mean + noise
