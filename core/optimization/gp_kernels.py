"""
Aetheris Optimization & Neural-Symbolic: Gaussian Process Covariance Kernels
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
from typing import List, Sequence, Optional
from core.math.vectors import VectorND


class BaseKernel:
    """Abstract Base Class for Covariance Kernels in Gaussian Process Regression."""
    def __call__(self, x1: VectorND, x2: VectorND) -> float:
        raise NotImplementedError

    def compute_gram_matrix(self, X: Sequence[VectorND]) -> List[List[float]]:
        """Computes K(X, X) symmetric positive semi-definite Gram matrix."""
        n = len(X)
        gram = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                val = self(X[i], X[j])
                gram[i][j] = val
                gram[j][i] = val
        return gram

    def compute_cross_covariance(self, X_train: Sequence[VectorND], X_star: Sequence[VectorND]) -> List[List[float]]:
        """Computes K(X_star, X_train) cross-covariance matrix."""
        m = len(X_star)
        n = len(X_train)
        k_cross = [[0.0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                k_cross[i][j] = self(X_star[i], X_train[j])
        return k_cross


class RBFKernel(BaseKernel):
    """
    Radial Basis Function (Squared Exponential) Kernel:
    k(x, x') = sigma_f^2 * exp( - ||x - x'||^2 / (2 * l^2) )
    """
    def __init__(self, length_scale: float = 1.0, variance: float = 1.0) -> None:
        self.l = max(1e-5, float(length_scale))
        self.var = max(1e-5, float(variance))

    def __call__(self, x1: VectorND, x2: VectorND) -> float:
        dist_sq = (x1 - x2).norm_sq()
        return self.var * math.exp(-0.5 * dist_sq / (self.l * self.l))


class Matern52Kernel(BaseKernel):
    """
    Matern 5/2 Covariance Kernel for twice-differentiable physical surfaces:
    k(r) = sigma_f^2 * (1 + sqrt(5)*r/l + 5*r^2/(3*l^2)) * exp(-sqrt(5)*r/l)
    """
    def __init__(self, length_scale: float = 1.0, variance: float = 1.0) -> None:
        self.l = max(1e-5, float(length_scale))
        self.var = max(1e-5, float(variance))
        self.sqrt5 = math.sqrt(5.0)

    def __call__(self, x1: VectorND, x2: VectorND) -> float:
        r = (x1 - x2).norm()
        scaled = self.sqrt5 * r / self.l
        poly = 1.0 + scaled + (5.0 * r * r) / (3.0 * self.l * self.l)
        return self.var * poly * math.exp(-scaled)


class PeriodicKernel(BaseKernel):
    """
    Periodic Kernel for cyclical research dynamics:
    k(x, x') = sigma_f^2 * exp( -2 * sin^2(pi * ||x - x'|| / p) / l^2 )
    """
    def __init__(self, period: float = 1.0, length_scale: float = 1.0, variance: float = 1.0) -> None:
        self.p = max(1e-5, float(period))
        self.l = max(1e-5, float(length_scale))
        self.var = max(1e-5, float(variance))

    def __call__(self, x1: VectorND, x2: VectorND) -> float:
        r = (x1 - x2).norm()
        sin_val = math.sin(math.pi * r / self.p)
        return self.var * math.exp(-2.0 * (sin_val * sin_val) / (self.l * self.l))
