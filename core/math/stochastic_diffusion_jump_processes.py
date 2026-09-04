"""
JobGuard Core Math - Stochastic Jump-Diffusion (Merton Process) Engine
Models sudden discontinuous jumps in scam volume surges and viral phishing outbreaks
using compound Poisson processes integrated with continuous Geometric Brownian Motion.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import random
import math


class StochasticDiffusionJumpProcesses:
    """Merton jump-diffusion stochastic differential equation simulator."""

    def __init__(
        self,
        mu_drift: float = 0.05,
        sigma_volatility: float = 0.20,
        lambda_jump_intensity: float = 0.50,
        jump_mean_mu: float = 0.15,
        jump_std_delta: float = 0.10
    ):
        self.mu = mu_drift
        self.sigma = sigma_volatility
        self.lambda_j = lambda_jump_intensity
        self.jump_mu = jump_mean_mu
        self.jump_std = jump_std_delta

    def simulate_path(self, initial_value: float = 100.0, time_steps: int = 50, dt: float = 0.1) -> List[float]:
        """Simulates one stochastic path: dS/S = (mu - lambda*k)dt + sigma*dW + dJ."""
        k_compensator = math.exp(self.jump_mu + 0.5 * (self.jump_std ** 2)) - 1.0
        drift_term = (self.mu - self.lambda_j * k_compensator - 0.5 * (self.sigma ** 2)) * dt

        path = [initial_value]
        current = initial_value

        for _ in range(time_steps):
            # Brownian motion increment
            z = random.gauss(0.0, 1.0)
            diffusion = self.sigma * math.sqrt(dt) * z

            # Poisson jump component
            num_jumps = 0
            p_jump = self.lambda_j * dt
            if random.random() < p_jump:
                num_jumps = 1

            jump_factor = 0.0
            for _ in range(num_jumps):
                jump_factor += random.gauss(self.jump_mu, self.jump_std)

            current = current * math.exp(drift_term + diffusion + jump_factor)
            path.append(max(0.0, current))

        return path
