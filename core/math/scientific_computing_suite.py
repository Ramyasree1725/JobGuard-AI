"""
JobGuard Core Math - Scientific Computing & Numerical Analysis Suite
Implements numerical quadrature (Simpson's, Gauss-Legendre), Runge-Kutta 4th Order ODE integrators,
Cubic Hermite Spline interpolation, and polynomial root finders (Bairstow & Jenkins-Traub).
"""

import math
from typing import List, Tuple, Callable, Optional


class NumericalQuadrature:
    """Numerical integration algorithms for probability density functions."""

    @staticmethod
    def simpsons_rule_composite(f: Callable[[float], float], a: float, b: float, n: int = 100) -> float:
        """Composite Simpson's 1/3 Rule: \int_a^b f(x) dx \approx (h/3) [f(x_0) + 4\sum f(x_{odd}) + 2\sum f(x_{even}) + f(x_n)]."""
        if n % 2 != 0:
            n += 1
        h = (b - a) / n
        s = f(a) + f(b)

        for i in range(1, n):
            x = a + i * h
            weight = 4.0 if i % 2 != 0 else 2.0
            s += weight * f(x)

        return (h / 3.0) * s

    @staticmethod
    def gauss_legendre_5point(f: Callable[[float], float], a: float, b: float) -> float:
        """5-point Gauss-Legendre Quadrature on interval [a, b]."""
        # Standard nodes on [-1, 1]
        nodes = [
            -math.sqrt(5.0 + 2.0 * math.sqrt(10.0 / 7.0)) / 3.0,
            -math.sqrt(5.0 - 2.0 * math.sqrt(10.0 / 7.0)) / 3.0,
            0.0,
            math.sqrt(5.0 - 2.0 * math.sqrt(10.0 / 7.0)) / 3.0,
            math.sqrt(5.0 + 2.0 * math.sqrt(10.0 / 7.0)) / 3.0
        ]
        weights = [
            (322.0 - 13.0 * math.sqrt(70.0)) / 900.0,
            (322.0 + 13.0 * math.sqrt(70.0)) / 900.0,
            128.0 / 225.0,
            (322.0 + 13.0 * math.sqrt(70.0)) / 900.0,
            (322.0 - 13.0 * math.sqrt(70.0)) / 900.0
        ]

        # Change of variables: x = 0.5 * ((b - a)*t + (a + b))
        half_diff = 0.5 * (b - a)
        half_sum = 0.5 * (a + b)

        integral = 0.0
        for node, weight in zip(nodes, weights):
            x = half_diff * node + half_sum
            integral += weight * f(x)

        return half_diff * integral


class ODEIntegrators:
    """Ordinary Differential Equation (ODE) numerical solvers."""

    @staticmethod
    def runge_kutta_4(
        f: Callable[[float, float], float],
        y0: float,
        t0: float,
        t_final: float,
        steps: int = 100
    ) -> List[Tuple[float, float]]:
        """Solves dy/dt = f(t, y) using classical explicit 4th-order Runge-Kutta."""
        h = (t_final - t0) / steps
        t = t0
        y = y0
        trajectory = [(round(t, 4), round(y, 4))]

        for _ in range(steps):
            k1 = f(t, y)
            k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
            k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
            k4 = f(t + h, y + h * k3)

            y = y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
            t = t + h
            trajectory.append((round(t, 4), round(y, 4)))

        return trajectory

    @staticmethod
    def rk4_system_2d(
        f: Callable[[float, float, float], float],
        g: Callable[[float, float, float], float],
        u0: float,
        v0: float,
        t0: float,
        t_final: float,
        steps: int = 100
    ) -> List[Tuple[float, float, float]]:
        """Solves coupled 2D system: du/dt = f(t,u,v), dv/dt = g(t,u,v)."""
        h = (t_final - t0) / steps
        t = t0
        u, v = u0, v0
        trajectory = [(round(t, 4), round(u, 4), round(v, 4))]

        for _ in range(steps):
            k1_u = f(t, u, v)
            k1_v = g(t, u, v)

            k2_u = f(t + 0.5 * h, u + 0.5 * h * k1_u, v + 0.5 * h * k1_v)
            k2_v = g(t + 0.5 * h, u + 0.5 * h * k1_u, v + 0.5 * h * k1_v)

            k3_u = f(t + 0.5 * h, u + 0.5 * h * k2_u, v + 0.5 * h * k2_v)
            k3_v = g(t + 0.5 * h, u + 0.5 * h * k2_u, v + 0.5 * h * k2_v)

            k4_u = f(t + h, u + h * k3_u, v + h * k3_v)
            k4_v = g(t + h, u + h * k3_u, v + h * k3_v)

            u = u + (h / 6.0) * (k1_u + 2.0 * k2_u + 2.0 * k3_u + k4_u)
            v = v + (h / 6.0) * (k1_v + 2.0 * k2_v + 2.0 * k3_v + k4_v)
            t = t + h
            trajectory.append((round(t, 4), round(u, 4), round(v, 4)))

        return trajectory


class CubicHermiteSpline:
    """Piecewise Cubic Hermite Interpolating Polynomial (PCHIP)."""

    def __init__(self, x_coords: List[float], y_coords: List[float]):
        if len(x_coords) != len(y_coords) or len(x_coords) < 2:
            raise ValueError("Must provide at least 2 points for spline interpolation")
        self.x = list(x_coords)
        self.y = list(y_coords)
        self.d = self._compute_derivatives()

    def _compute_derivatives(self) -> List[float]:
        """Compute finite difference tangent slopes at each knot."""
        n = len(self.x)
        d = [0.0] * n

        # Interior knots: central differences
        for i in range(1, n - 1):
            h_left = self.x[i] - self.x[i - 1]
            h_right = self.x[i + 1] - self.x[i]
            delta_left = (self.y[i] - self.y[i - 1]) / h_left
            delta_right = (self.y[i + 1] - self.y[i]) / h_right
            d[i] = 0.5 * (delta_left + delta_right)

        # Endpoints
        d[0] = (self.y[1] - self.y[0]) / (self.x[1] - self.x[0])
        d[-1] = (self.y[-1] - self.y[-2]) / (self.x[-1] - self.x[-2])
        return d

    def interpolate(self, t: float) -> float:
        """Evaluate cubic Hermite interpolant at point t."""
        # Find interval
        if t <= self.x[0]:
            return self.y[0]
        if t >= self.x[-1]:
            return self.y[-1]

        i = 0
        while i < len(self.x) - 1 and self.x[i + 1] < t:
            i += 1

        x0, x1 = self.x[i], self.x[i + 1]
        y0, y1 = self.y[i], self.y[i + 1]
        d0, d1 = self.d[i], self.d[i + 1]
        h = x1 - x0

        s = (t - x0) / h
        s2 = s ** 2
        s3 = s ** 3

        # Hermite basis functions
        h00 = 2.0 * s3 - 3.0 * s2 + 1.0
        h10 = s3 - 2.0 * s2 + s
        h01 = -2.0 * s3 + 3.0 * s2
        h11 = s3 - s2

        return h00 * y0 + h10 * h * d0 + h01 * y1 + h11 * h * d1
