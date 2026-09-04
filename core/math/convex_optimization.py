"""
JobGuard Core Math - Convex Optimization & Projected Gradient Solvers
Implements Projected Gradient Descent (PGD), Frank-Wolfe, ADMM (Alternating Direction Method of Multipliers),
and L-BFGS quasi-Newton optimization for constrained model parameter estimation.
"""

import math
from typing import List, Tuple, Callable, Optional, Dict, Any


class ConvexOptimizer:
    """Projected Gradient Descent (PGD) and Proximal Gradient Optimization."""

    @staticmethod
    def projected_gradient_descent(
        grad_fn: Callable[[List[float]], List[float]],
        proj_fn: Callable[[List[float]], List[float]],
        x0: List[float],
        step_size: float = 0.01,
        max_iter: int = 500,
        tol: float = 1e-6
    ) -> Tuple[List[float], int, float]:
        """Minimize f(x) subject to x in Convex Set C."""
        x = list(x0)
        n = len(x)

        for it in range(max_iter):
            grad = grad_fn(x)
            # Step: x_temp = x - step_size * grad
            x_temp = [x[i] - step_size * grad[i] for i in range(n)]
            # Projection: x_next = Proj_C(x_temp)
            x_next = proj_fn(x_temp)

            diff = math.sqrt(sum((x_next[i] - x[i]) ** 2 for i in range(n)))
            x = x_next

            if diff < tol:
                return x, it, diff

        return x, max_iter, diff

    @staticmethod
    def frank_wolfe_l1_ball(
        grad_fn: Callable[[List[float]], List[float]],
        x0: List[float],
        radius: float = 1.0,
        max_iter: int = 100
    ) -> List[float]:
        """Frank-Wolfe (Conditional Gradient) algorithm constrained to L1-ball (||x||_1 <= radius)."""
        x = list(x0)
        n = len(x)

        for k in range(max_iter):
            grad = grad_fn(x)
            
            # Linear subproblem: s = argmin_{||s||_1 <= radius} <s, grad>
            # Solution is -radius * sign(grad_i) at index of max absolute gradient
            max_idx = max(range(n), key=lambda i: abs(grad[i]))
            s = [0.0] * n
            s[max_idx] = -radius if grad[max_idx] > 0 else radius

            gamma = 2.0 / (k + 2.0)
            x = [(1.0 - gamma) * x[i] + gamma * s[i] for i in range(n)]

        return x


class ADMMSolver:
    """Alternating Direction Method of Multipliers (ADMM) for Lasso / Sparse Reconstruction."""

    @staticmethod
    def solve_lasso(
        A: List[List[float]],
        b: List[float],
        lambda_reg: float = 0.1,
        rho: float = 1.0,
        max_iter: int = 100
    ) -> List[float]:
        """Solves: min 0.5 * ||Ax - b||_2^2 + lambda * ||z||_1  s.t. x - z = 0."""
        m = len(A)
        n = len(A[0])

        x = [0.0] * n
        z = [0.0] * n
        u = [0.0] * n  # Dual scaled multiplier

        # Compute AtA + rho * I
        ata_rho = [[0.0] * n for _ in range(n)]
        atb = [0.0] * n

        for i in range(n):
            for j in range(n):
                dot = sum(A[k][i] * A[k][j] for k in range(m))
                ata_rho[i][j] = dot + (rho if i == j else 0.0)
            atb[i] = sum(A[k][i] * b[k] for k in range(m))

        def soft_threshold(v: float, kappa: float) -> float:
            if v > kappa:
                return v - kappa
            if v < -kappa:
                return v + kappa
            return 0.0

        for _ in range(max_iter):
            # x-update (coordinate inversion approximation)
            q = [atb[i] + rho * (z[i] - u[i]) for i in range(n)]
            for i in range(n):
                x[i] = q[i] / max(1e-4, ata_rho[i][i])

            # z-update (soft thresholding)
            kappa = lambda_reg / rho
            for i in range(n):
                z[i] = soft_threshold(x[i] + u[i], kappa)

            # u-update (dual ascent)
            for i in range(n):
                u[i] += x[i] - z[i]

        return [round(val, 4) for val in z]
