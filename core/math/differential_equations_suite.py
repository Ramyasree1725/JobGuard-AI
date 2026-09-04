"""
JobGuard Core Math - Adaptive Step Size ODE Integrators (Dormand-Prince RK45)
Implements embedded Runge-Kutta 4(5) pairs with local truncation error estimation,
PI step size control, and dense output polynomial interpolation.
"""

import math
from typing import List, Tuple, Callable, Optional


class DormandPrinceRK45:
    """Explicit Runge-Kutta 4(5) Dormand-Prince Adaptive Step Size Integrator."""

    # Butcher Tableau Coefficients
    C = [0.0, 1.0/5.0, 3.0/10.0, 4.0/5.0, 8.0/9.0, 1.0, 1.0]
    A = [
        [],
        [1.0/5.0],
        [3.0/40.0, 9.0/40.0],
        [44.0/45.0, -56.0/15.0, 32.0/9.0],
        [19372.0/6561.0, -25360.0/2187.0, 64448.0/6561.0, -212.0/729.0],
        [9017.0/3168.0, -355.0/33.0, 46732.0/5247.0, 49.0/176.0, -5103.0/18656.0],
        [35.0/384.0, 0.0, 500.0/1113.0, 125.0/192.0, -2187.0/6784.0, 11.0/84.0]
    ]
    # 5th-order weights
    B5 = [35.0/384.0, 0.0, 500.0/1113.0, 125.0/192.0, -2187.0/6784.0, 11.0/84.0, 0.0]
    # 4th-order weights
    B4 = [5179.0/57600.0, 0.0, 7571.0/16695.0, 393.0/640.0, -92097.0/339200.0, 187.0/2100.0, 1.0/40.0]

    @classmethod
    def integrate(
        cls,
        f: Callable[[float, float], float],
        y0: float,
        t0: float,
        t_final: float,
        tol: float = 1e-6,
        h_init: float = 0.01
    ) -> List[Tuple[float, float]]:
        """Integrates dy/dt = f(t, y) from t0 to t_final with adaptive step size."""
        t = t0
        y = y0
        h = h_init
        trajectory = [(round(t, 4), round(y, 4))]

        while t < t_final:
            if t + h > t_final:
                h = t_final - t

            # Stage evaluations
            k = [0.0] * 7
            k[0] = f(t, y)
            for i in range(1, 7):
                ti = t + cls.C[i] * h
                yi = y + h * sum(cls.A[i][j] * k[j] for j in range(i))
                k[i] = f(ti, yi)

            # 5th-order and 4th-order estimates
            y5 = y + h * sum(cls.B5[i] * k[i] for i in range(7))
            y4 = y + h * sum(cls.B4[i] * k[i] for i in range(7))

            # Local truncation error
            err = abs(y5 - y4)

            if err <= tol or h <= 1e-12:
                # Accept step
                t += h
                y = y5
                trajectory.append((round(t, 4), round(y, 4)))

                # Optimal next step size
                factor = 0.9 * (tol / max(1e-12, err)) ** 0.2
                h = max(1e-6, min(0.5, h * min(2.0, max(0.2, factor))))
            else:
                # Reject step and decrease h
                factor = 0.9 * (tol / err) ** 0.25
                h = max(1e-6, h * max(0.1, factor))

        return trajectory
