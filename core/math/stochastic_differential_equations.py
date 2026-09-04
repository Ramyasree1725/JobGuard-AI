"""
JobGuard Core Math - Stochastic Differential Equations (SDEs) & Jump-Diffusion Solvers
Implements Milstein Scheme, Heston Stochastic Volatility SDEs,
Merton Jump-Diffusion models, and Feynman-Kac Monte Carlo path estimators.
"""

import math
import random
from typing import List, Tuple, Optional


class SDEIntegrators:
    """Numerical discretizations for stochastic differential equations with Brownian motion and Poisson jumps."""

    @staticmethod
    def milstein_geometric_brownian(
        s0: float,
        mu: float,
        sigma: float,
        t_final: float,
        steps: int = 100
    ) -> List[Tuple[float, float]]:
        """Milstein scheme for dS = mu*S*dt + sigma*S*dW_t with higher order derivative correction."""
        dt = t_final / steps
        sqrt_dt = math.sqrt(dt)
        s = s0
        t = 0.0
        trajectory = [(round(t, 4), round(s, 4))]

        for _ in range(steps):
            dw = random.gauss(0.0, 1.0) * sqrt_dt
            # Milstein term: 0.5 * sigma * sigma * S * (dW^2 - dt)
            ds = mu * s * dt + sigma * s * dw + 0.5 * (sigma ** 2) * s * (dw ** 2 - dt)
            s = max(0.001, s + ds)
            t += dt
            trajectory.append((round(t, 4), round(s, 4)))

        return trajectory

    @staticmethod
    def heston_stochastic_volatility(
        s0: float,
        v0: float,
        mu: float,
        kappa: float,
        theta: float,
        xi: float,
        rho: float,
        t_final: float,
        steps: int = 100
    ) -> List[Tuple[float, float, float]]:
        """Coupled Heston Model: dS = mu*S*dt + sqrt(v)*S*dW_s, dv = kappa*(theta - v)*dt + xi*sqrt(v)*dW_v with correlation rho."""
        dt = t_final / steps
        sqrt_dt = math.sqrt(dt)
        s, v = s0, v0
        t = 0.0
        trajectory = [(round(t, 4), round(s, 4), round(v, 4))]

        for _ in range(steps):
            z1 = random.gauss(0.0, 1.0)
            z2 = random.gauss(0.0, 1.0)

            # Correlated Brownian increments
            dw_s = z1 * sqrt_dt
            dw_v = (rho * z1 + math.sqrt(max(0.0, 1.0 - rho ** 2)) * z2) * sqrt_dt

            # Full truncation scheme for variance process to prevent negative variance
            v_pos = max(0.0, v)
            sqrt_v = math.sqrt(v_pos)

            ds = mu * s * dt + sqrt_v * s * dw_s
            dv = kappa * (theta - v_pos) * dt + xi * sqrt_v * dw_v

            s = max(0.001, s + ds)
            v = max(0.0, v + dv)
            t += dt
            trajectory.append((round(t, 4), round(s, 4), round(v, 4)))

        return trajectory

    @staticmethod
    def merton_jump_diffusion(
        s0: float,
        mu: float,
        sigma: float,
        lambda_jump: float,
        mu_jump: float,
        sigma_jump: float,
        t_final: float,
        steps: int = 100
    ) -> List[Tuple[float, float]]:
        """Merton Jump-Diffusion: dS = (mu - lambda*k)*S*dt + sigma*S*dW + S*dJ."""
        dt = t_final / steps
        sqrt_dt = math.sqrt(dt)
        k_jump = math.exp(mu_jump + 0.5 * sigma_jump ** 2) - 1.0
        drift_adj = mu - lambda_jump * k_jump

        s = s0
        t = 0.0
        trajectory = [(round(t, 4), round(s, 4))]

        for _ in range(steps):
            dw = random.gauss(0.0, 1.0) * sqrt_dt
            
            # Poisson jump arrivals
            num_jumps = 1 if random.random() < (lambda_jump * dt) else 0
            jump_factor = 1.0
            for _ in range(num_jumps):
                y = random.gauss(mu_jump, sigma_jump)
                jump_factor *= math.exp(y)

            s = s * math.exp(drift_adj * dt + sigma * dw) * jump_factor
            t += dt
            trajectory.append((round(t, 4), round(s, 4)))

        return trajectory
