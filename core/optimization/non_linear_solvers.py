"""
JobGuard Core Optimization - Newton-Raphson & Levenberg-Marquardt Solvers
Non-linear least squares curve fitting and root finding algorithms.
"""

import math
from typing import List, Tuple, Callable, Optional


class NonLinearSolvers:
    """Non-linear equations and least squares regression solvers."""

    @staticmethod
    def newton_raphson_root_1d(
        f: Callable[[float], float],
        df: Callable[[float], float],
        x0: float,
        max_iter: int = 50,
        tol: float = 1e-7
    ) -> Tuple[float, int]:
        """Finds root of f(x) = 0 using Newton-Raphson iteration: x_{n+1} = x_n - f(x_n)/f'(x_n)."""
        x = x0
        for i in range(max_iter):
            fx = f(x)
            if abs(fx) < tol:
                return x, i
            dfx = df(x)
            if abs(dfx) < 1e-12:
                break
            x = x - fx / dfx

        return x, max_iter

    @staticmethod
    def levenberg_marquardt_2d(
        residual_fn: Callable[[List[float]], List[float]],
        jacobian_fn: Callable[[List[float]], List[List[float]]],
        initial_params: List[float],
        lambda_init: float = 0.01,
        max_iter: int = 50
    ) -> List[float]:
        """Damped Gauss-Newton / Levenberg-Marquardt non-linear least squares optimizer."""
        p = list(initial_params)
        lam = lambda_init

        for _ in range(max_iter):
            r = residual_fn(p)
            J = jacobian_fn(p)
            # Normal equations: (J^T J + lambda * diag(J^T J)) delta = -J^T r
            m = len(J)
            n = len(p)

            # J^T J
            jtj = [[sum(J[k][i] * J[k][j] for k in range(m)) for j in range(n)] for i in range(n)]
            jtr = [sum(J[k][i] * r[k] for k in range(m)) for i in range(n)]

            # Damping diagonal
            for i in range(n):
                jtj[i][i] += lam * (jtj[i][i] + 1e-4)

            # 2x2 solve
            if n == 2:
                det = jtj[0][0] * jtj[1][1] - jtj[0][1] * jtj[1][0]
                if abs(det) > 1e-12:
                    delta0 = (-jtr[0] * jtj[1][1] + jtr[1] * jtj[0][1]) / det
                    delta1 = (jtr[0] * jtj[1][0] - jtr[1] * jtj[0][0]) / det
                    p[0] += delta0
                    p[1] += delta1

        return [round(val, 4) for val in p]
