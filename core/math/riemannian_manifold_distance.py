"""
JobGuard Core Math - Riemannian Manifold & Hyperbolic Geodesic Distance Engine
Computes Poincaré ball hyperbolic distance and Fisher Information Metric (FIM) geodesics
for non-Euclidean hierarchical clustering of recruitment threat taxonomies.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import math


class RiemannianManifoldDistance:
    """Computes hyperbolic and information geometric distances on Riemannian manifolds."""

    def __init__(self, curvature_c: float = 1.0):
        self.c = curvature_c  # Negative curvature constant of Poincaré ball

    def poincare_norm_sq(self, u: List[float]) -> float:
        """Computes Euclidean squared norm ||u||^2."""
        return sum(x * x for x in u)

    def poincare_distance(self, u: List[float], v: List[float]) -> float:
        """Computes exact geodesic distance between two points in the Poincaré Ball Model.
        
        d_H(u, v) = arcosh(1 + 2 * ||u - v||^2 / ((1 - ||u||^2)(1 - ||v||^2)))
        """
        norm_u_sq = self.poincare_norm_sq(u)
        norm_v_sq = self.poincare_norm_sq(v)

        # Boundary clamping to prevent numerical overflow near Poincaré horizon
        norm_u_sq = min(0.9999, norm_u_sq)
        norm_v_sq = min(0.9999, norm_v_sq)

        diff_sq = sum((x - y) ** 2 for x, y in zip(u, v))

        alpha = 1.0 - norm_u_sq
        beta = 1.0 - norm_v_sq

        gamma = 1.0 + 2.0 * (diff_sq / max(1e-8, alpha * beta))
        gamma = max(1.0, gamma)

        # arcosh(x) = ln(x + sqrt(x^2 - 1))
        arcosh_val = math.log(gamma + math.sqrt(gamma * gamma - 1.0))
        return arcosh_val / math.sqrt(self.c)

    def fisher_rao_gaussian_distance(self, mu1: float, sigma1: float, mu2: float, sigma2: float) -> float:
        """Computes Fisher-Rao Riemannian metric distance on the manifold of Univariate Normal Distributions.
        
        This space is isometric to the Hyperbolic Upper Half-Plane H^2.
        """
        s1 = max(1e-6, sigma1)
        s2 = max(1e-6, sigma2)

        numerator = (mu1 - mu2) ** 2 + 2.0 * (s1 - s2) ** 2
        denominator = 2.0 * s1 * s2

        delta = math.sqrt(numerator / denominator)
        # Hyperbolic distance formula in H^2
        dist = math.sqrt(2.0) * math.log(delta + math.sqrt(delta * delta + 1.0))
        return dist
