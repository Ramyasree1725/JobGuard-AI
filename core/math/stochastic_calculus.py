"""
JobGuard Core Math - Stochastic Calculus & Ito Process Simulation
Implements Geometric Brownian Motion (GBM), Ornstein-Uhlenbeck mean-reverting processes,
and Euler-Maruyama numerical integration for stochastic salary and risk models.
"""

import math
import random
from typing import List, Tuple, Optional


class StochasticCalculus:
    """Stochastic differential equation (SDE) integrators."""

    @staticmethod
    def geometric_brownian_motion(
        s0: float,
        mu: float,
        sigma: float,
        t_final: float = 1.0,
        steps: int = 100
    ) -> List[Tuple[float, float]]:
        """Simulate dS_t = mu S_t dt + sigma S_t dW_t using exact exponential solution."""
        dt = t_final / steps
        trajectory = [(0.0, s0)]
        curr_s = s0

        for step in range(1, steps + 1):
            t = step * dt
            z = random.gauss(0.0, 1.0)
            # S_{t+dt} = S_t * exp((mu - 0.5*sigma^2)*dt + sigma*sqrt(dt)*Z)
            curr_s = curr_s * math.exp((mu - 0.5 * sigma ** 2) * dt + sigma * math.sqrt(dt) * z)
            trajectory.append((round(t, 4), round(curr_s, 2)))

        return trajectory

    @staticmethod
    def ornstein_uhlenbeck_process(
        x0: float,
        theta: float,  # Mean reversion speed
        mu: float,     # Long-term mean
        sigma: float,  # Volatility
        t_final: float = 1.0,
        steps: int = 100
    ) -> List[Tuple[float, float]]:
        """Simulate mean-reverting dX_t = theta (mu - X_t) dt + sigma dW_t."""
        dt = t_final / steps
        trajectory = [(0.0, x0)]
        curr_x = x0

        for step in range(1, steps + 1):
            t = step * dt
            z = random.gauss(0.0, 1.0)
            # Euler-Maruyama discretization
            curr_x = curr_x + theta * (mu - curr_x) * dt + sigma * math.sqrt(dt) * z
            trajectory.append((round(t, 4), round(curr_x, 3)))

        return trajectory
