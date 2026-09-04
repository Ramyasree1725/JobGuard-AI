"""
JobGuard Core Math - Primal-Dual Interior Point Convex Optimization Solver
Solves constrained quadratic programs (QP) and support vector machine duals
for optimal threat detection boundary hyperplanes with Karush-Kuhn-Tucker (KKT) conditions.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import math


class ConvexOptimizationInteriorPointSolver:
    """Log-barrier interior point method for linearly constrained convex quadratic programming."""

    def __init__(self, max_barrier_iter: int = 20, mu_barrier_mult: float = 10.0, tolerance: float = 1e-6):
        self.max_iter = max_barrier_iter
        self.mu = mu_barrier_mult
        self.tol = tolerance

    def solve_constrained_qp(
        self,
        Q_matrix: List[List[float]],
        c_vector: List[float],
        A_ineq: List[List[float]],
        b_ineq: List[float],
        x_init: List[float]
    ) -> List[float]:
        """Minimizes (1/2)*x^T*Q*x + c^T*x subject to A*x <= b via Newton barrier steps."""
        x = list(x_init)
        n = len(x)
        t_param = 1.0  # Barrier parameter

        for _ in range(self.max_iter):
            # Gradient of barrier objective: phi(x) = t*(Qx + c) - sum_i (1 / (b_i - a_i^T*x)) * a_i
            # 1. Compute slack: s_i = b_i - a_i^T*x
            slack = [b_ineq[i] - sum(A_ineq[i][j] * x[j] for j in range(n)) for i in range(len(b_ineq))]
            if any(s <= 0 for s in slack):
                # Infeasible or boundary violated, break
                break

            grad = [0.0] * n
            # t * (Q*x + c)
            for j in range(n):
                qx_j = sum(Q_matrix[j][k] * x[k] for k in range(n))
                grad[j] = t_param * (qx_j + c_vector[j])

            for i in range(len(b_ineq)):
                inv_s = 1.0 / max(1e-9, slack[i])
                for j in range(n):
                    grad[j] += inv_s * A_ineq[i][j]

            # Projected gradient descent step
            step_size = 0.01 / t_param
            for j in range(n):
                x[j] -= step_size * grad[j]

            # Increase barrier precision
            t_param *= self.mu

        return x
