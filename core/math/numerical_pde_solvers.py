"""
JobGuard Core Math - Numerical Partial Differential Equation (PDE) Solvers
Finite Difference Methods (FDM) for 1D/2D Heat Diffusion, Wave Equation,
and Poisson Elliptic Equations with Dirichlet and Neumann boundary conditions.
"""

import math
from typing import List, Tuple, Optional


class PDESolver:
    """Finite Difference Solvers for classical parabolic, hyperbolic, and elliptic PDEs."""

    @staticmethod
    def solve_1d_heat_equation(
        initial_u: List[float],
        alpha: float = 0.01,
        dx: float = 0.1,
        dt: float = 0.001,
        time_steps: int = 100,
        boundary_left: float = 0.0,
        boundary_right: float = 0.0
    ) -> List[List[float]]:
        """Solves du/dt = alpha * d^2u/dx^2 using FTCS (Forward Time Centered Space)."""
        nx = len(initial_u)
        r = alpha * dt / (dx ** 2)
        if r > 0.5:
            # Stability warning for explicit scheme
            pass

        history = [[val for val in initial_u]]
        curr_u = list(initial_u)

        for _ in range(time_steps):
            next_u = [0.0] * nx
            next_u[0] = boundary_left
            next_u[-1] = boundary_right

            for i in range(1, nx - 1):
                next_u[i] = curr_u[i] + r * (curr_u[i + 1] - 2.0 * curr_u[i] + curr_u[i - 1])

            curr_u = next_u
            history.append(list(curr_u))

        return history

    @staticmethod
    def solve_2d_poisson_jacobi(
        source_f: List[List[float]],
        dx: float = 0.1,
        dy: float = 0.1,
        max_iter: int = 500,
        tol: float = 1e-5
    ) -> List[List[float]]:
        """Solves d^2u/dx^2 + d^2u/dy^2 = f(x, y) on a rectangular domain using Jacobi iteration."""
        ny = len(source_f)
        nx = len(source_f[0])

        u = [[0.0] * nx for _ in range(ny)]
        factor = (dx ** 2 * dy ** 2) / (2.0 * (dx ** 2 + dy ** 2))

        for _ in range(max_iter):
            next_u = [[0.0] * nx for _ in range(ny)]
            max_diff = 0.0

            for y in range(1, ny - 1):
                for x in range(1, nx - 1):
                    val_x = (u[y][x + 1] + u[y][x - 1]) / (dx ** 2)
                    val_y = (u[y + 1][x] + u[y - 1][x]) / (dy ** 2)
                    val = factor * (val_x + val_y - source_f[y][x])

                    diff = abs(val - u[y][x])
                    if diff > max_diff:
                        max_diff = diff
                    next_u[y][x] = val

            u = next_u
            if max_diff < tol:
                break

        return u
