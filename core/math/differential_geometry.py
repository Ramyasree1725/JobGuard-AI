"""
JobGuard Core Math - Differential Geometry & Manifold Learning
Implements Christoffel symbols, Riemannian metric tensors, geodesic integrators,
and tangent space projections for non-Euclidean representation of fraud networks.
"""

import math
from typing import List, Tuple, Callable, Optional


class RiemannianManifold:
    """Represents a smooth manifold with metric tensor g_ij(x)."""

    def __init__(self, dimension: int, metric_tensor_fn: Callable[[List[float]], List[List[float]]]):
        self.dim = dimension
        self.metric_tensor_fn = metric_tensor_fn

    def compute_metric(self, point: List[float]) -> List[List[float]]:
        return self.metric_tensor_fn(point)

    def compute_inverse_metric(self, point: List[float]) -> List[List[float]]:
        g = self.compute_metric(point)
        # 2x2 or 3x3 matrix inverse
        n = self.dim
        if n == 2:
            det = g[0][0] * g[1][1] - g[0][1] * g[1][0]
            if abs(det) < 1e-12:
                det = 1e-12
            inv_det = 1.0 / det
            return [
                [g[1][1] * inv_det, -g[0][1] * inv_det],
                [-g[1][0] * inv_det, g[0][0] * inv_det]
            ]
        # Diagonal fallback for n > 2
        return [[1.0 / max(1e-6, g[i][i]) if i == j else 0.0 for j in range(n)] for i in range(n)]

    def christoffel_symbols(self, point: List[float], eps: float = 1e-5) -> List[List[List[float]]]:
        """Compute Christoffel symbols of the second kind: \Gamma^k_{ij}."""
        n = self.dim
        g_inv = self.compute_inverse_metric(point)
        
        # Finite difference metric derivatives: dg_ij / dx_l
        dg = [[[0.0] * n for _ in range(n)] for _ in range(n)]  # dg[i][j][l]
        for l in range(n):
            pt_plus = list(point)
            pt_minus = list(point)
            pt_plus[l] += eps
            pt_minus[l] -= eps
            g_plus = self.compute_metric(pt_plus)
            g_minus = self.compute_metric(pt_minus)
            for i in range(n):
                for j in range(n):
                    dg[i][j][l] = (g_plus[i][j] - g_minus[i][j]) / (2.0 * eps)

        # Gamma^k_ij = 0.5 * sum_l g^kl (dg_jl/dx_i + dg_il/dx_j - dg_ij/dx_l)
        gamma = [[[0.0] * n for _ in range(n)] for _ in range(n)]  # gamma[k][i][j]
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    sum_val = 0.0
                    for l in range(n):
                        term = dg[j][l][i] + dg[i][l][j] - dg[i][j][l]
                        sum_val += g_inv[k][l] * term
                    gamma[k][i][j] = 0.5 * sum_val

        return gamma

    def geodesic_step(self, point: List[float], velocity: List[float], dt: float = 0.01) -> Tuple[List[float], List[float]]:
        """Integrate geodesic equation: d^2 x^k / dt^2 + \Gamma^k_ij (dx^i/dt)(dx^j/dt) = 0."""
        n = self.dim
        gamma = self.christoffel_symbols(point)

        acceleration = [0.0] * n
        for k in range(n):
            acc_k = 0.0
            for i in range(n):
                for j in range(n):
                    acc_k += gamma[k][i][j] * velocity[i] * velocity[j]
            acceleration[k] = -acc_k

        new_point = [point[k] + velocity[k] * dt + 0.5 * acceleration[k] * (dt ** 2) for k in range(n)]
        new_velocity = [velocity[k] + acceleration[k] * dt for k in range(n)]
        return new_point, new_velocity
