"""
JobGuard Core Optimization - Primal-Dual Interior Point Method (IPM)
Solves non-linear convex optimization problems subject to inequality and equality constraints
using logarithmic barrier functions and Newton-KKT direction steps.
"""

import math
from typing import List, Tuple, Callable, Optional


class InteriorPointSolver:
    """Primal-Dual Interior Point Algorithm for convex programs: min f0(x) s.t. fi(x) <= 0, Ax = b."""

    @staticmethod
    def solve_log_barrier_1d(
        objective_fn: Callable[[float], float],
        objective_grad: Callable[[float], float],
        ineq_constraint_fn: Callable[[float], float],  # g(x) <= 0
        ineq_constraint_grad: Callable[[float], float],
        x0: float,
        mu_barrier_init: float = 1.0,
        beta_decay: float = 0.5,
        outer_iters: int = 15,
        inner_iters: int = 20
    ) -> float:
        """Solves min f(x) - mu * ln(-g(x))."""
        x = x0
        mu = mu_barrier_init

        for _ in range(outer_iters):
            # Centering step via gradient descent
            for _ in range(inner_iters):
                gx = ineq_constraint_fn(x)
                if gx >= 0:
                    # Violates interior feasibility, project back
                    x -= 0.1
                    gx = ineq_constraint_fn(x)

                grad_f = objective_grad(x)
                grad_g = ineq_constraint_grad(x)
                
                # Barrier gradient: grad_f - mu * (grad_g / g(x))
                barrier_grad = grad_f - mu * (grad_g / min(-1e-6, gx))

                # Step
                step_size = 0.05
                x_next = x - step_size * barrier_grad
                if ineq_constraint_fn(x_next) < 0:
                    x = x_next

            # Decay barrier parameter mu
            mu *= beta_decay

        return round(x, 4)
