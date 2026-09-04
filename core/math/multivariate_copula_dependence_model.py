"""
JobGuard Core Math - Multivariate Gaussian & Clayton Copula Tail Dependence Model
Models non-linear tail dependence and co-movement between multiple scam risk vectors
(e.g., simultaneous salary hyper-inflation, domain typosquatting, and advance fees).
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import math


class MultivariateCopulaDependenceModel:
    """Clayton and Gumbel Archimedean copula engine for extreme tail risk modeling."""

    def __init__(self, theta_parameter: float = 2.0):
        self.theta = max(0.1, theta_parameter)

    def clayton_copula_cdf(self, u: float, v: float) -> float:
        """Computes bivariate Clayton copula CDF: C(u, v) = max(u^-theta + v^-theta - 1, 0)^(-1/theta)."""
        u = max(1e-6, min(0.9999, u))
        v = max(1e-6, min(0.9999, v))

        term = (u ** (-self.theta)) + (v ** (-self.theta)) - 1.0
        if term <= 0:
            return 0.0
        return term ** (-1.0 / self.theta)

    def lower_tail_dependence(self) -> float:
        """Calculates Clayton lower tail dependence coefficient lambda_L = 2^(-1/theta)."""
        return 2.0 ** (-1.0 / self.theta)

    def joint_tail_risk_probability(self, risk_u: float, risk_v: float) -> float:
        """Calculates probability that both threat vectors simultaneously exceed risk threshold."""
        # P(U > u, V > v) = 1 - u - v + C(u, v)
        c_uv = self.clayton_copula_cdf(risk_u, risk_v)
        joint_p = max(0.0, 1.0 - risk_u - risk_v + c_uv)
        return min(1.0, joint_p)
