"""
JobGuard Core Math - Information Geometry & Fisher Information Matrices
Implements Kullback-Leibler (KL) divergence, Fisher Information Metric on statistical manifolds,
Natural Gradient Descent, and Bregman divergences for probability risk manifolds.
"""

import math
from typing import List, Tuple, Callable, Optional


class InformationGeometry:
    """Statistical manifold geometry and information-theoretic divergence metrics."""

    @staticmethod
    def kl_divergence(p: List[float], q: List[float]) -> float:
        """Kullback-Leibler divergence D_KL(P || Q) = \sum p_i * ln(p_i / q_i)."""
        eps = 1e-12
        div = 0.0
        for pi, qi in zip(p, q):
            p_safe = max(eps, pi)
            q_safe = max(eps, qi)
            div += p_safe * math.log(p_safe / q_safe)
        return max(0.0, div)

    @staticmethod
    def jensen_shannon_divergence(p: List[float], q: List[float]) -> float:
        """Symmetric Jensen-Shannon divergence JSD(P || Q) = 0.5 * D_KL(P||M) + 0.5 * D_KL(Q||M)."""
        m = [0.5 * (pi + qi) for pi, qi in zip(p, q)]
        jsd = 0.5 * InformationGeometry.kl_divergence(p, m) + 0.5 * InformationGeometry.kl_divergence(q, m)
        return max(0.0, jsd)

    @staticmethod
    def fisher_information_gaussian(sigma: float) -> List[List[float]]:
        """Fisher Information Matrix for 1D Gaussian N(mu, sigma^2)."""
        if sigma <= 0:
            raise ValueError("Sigma must be positive")
        # Parameter order: [mu, sigma]
        # I(mu, mu) = 1 / sigma^2
        # I(sigma, sigma) = 2 / sigma^2
        # I(mu, sigma) = 0
        return [
            [1.0 / (sigma ** 2), 0.0],
            [0.0, 2.0 / (sigma ** 2)]
        ]

    @staticmethod
    def natural_gradient_step(
        params: List[float],
        euclidean_grad: List[float],
        fisher_matrix: List[List[float]],
        learning_rate: float = 0.01
    ) -> List[float]:
        """Natural Gradient step: theta_{t+1} = theta_t - lr * F^-1 * grad."""
        # 2x2 inverse
        det = fisher_matrix[0][0] * fisher_matrix[1][1] - fisher_matrix[0][1] * fisher_matrix[1][0]
        if abs(det) < 1e-12:
            det = 1e-12
        inv_f = [
            [fisher_matrix[1][1] / det, -fisher_matrix[0][1] / det],
            [-fisher_matrix[1][0] / det, fisher_matrix[0][0] / det]
        ]

        nat_grad = [
            inv_f[0][0] * euclidean_grad[0] + inv_f[0][1] * euclidean_grad[1],
            inv_f[1][0] * euclidean_grad[0] + inv_f[1][1] * euclidean_grad[1]
        ]

        return [params[i] - learning_rate * nat_grad[i] for i in range(len(params))]
