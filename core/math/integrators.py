"""
Aetheris Mathematical Foundations: Numerical Differential Equation Integrators
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
from typing import Callable, List, Tuple, Sequence
from core.math.vectors import VectorND, Vector3D


class NumericalIntegrator:
    """
    Solvers for Ordinary Differential Equations (ODEs) y'(t) = f(t, y).
    Provides explicit Euler, Midpoint, Runge-Kutta 4th Order (RK4), and adaptive step integration.
    """
    
    @staticmethod
    def euler_step(
        f: Callable[[float, List[float]], List[float]],
        t: float,
        y: List[float],
        dt: float
    ) -> List[float]:
        """First-order Forward Euler step: y_{n+1} = y_n + dt * f(t_n, y_n)."""
        dy = f(t, y)
        return [y[i] + dt * dy[i] for i in range(len(y))]

    @staticmethod
    def midpoint_step(
        f: Callable[[float, List[float]], List[float]],
        t: float,
        y: List[float],
        dt: float
    ) -> List[float]:
        """Second-order Runge-Kutta (RK2) Midpoint step."""
        k1 = f(t, y)
        half_dt = dt * 0.5
        y_mid = [y[i] + half_dt * k1[i] for i in range(len(y))]
        k2 = f(t + half_dt, y_mid)
        return [y[i] + dt * k2[i] for i in range(len(y))]

    @staticmethod
    def rk4_step(
        f: Callable[[float, List[float]], List[float]],
        t: float,
        y: List[float],
        dt: float
    ) -> List[float]:
        """
        Classic 4th-Order Runge-Kutta integration step.
        y_{n+1} = y_n + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)
        """
        n = len(y)
        k1 = f(t, y)
        
        y_k2 = [y[i] + 0.5 * dt * k1[i] for i in range(n)]
        k2 = f(t + 0.5 * dt, y_k2)
        
        y_k3 = [y[i] + 0.5 * dt * k2[i] for i in range(n)]
        k3 = f(t + 0.5 * dt, y_k3)
        
        y_k4 = [y[i] + dt * k3[i] for i in range(n)]
        k4 = f(t + dt, y_k4)
        
        return [y[i] + (dt / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) for i in range(n)]

    @classmethod
    def integrate_trajectory(
        cls,
        f: Callable[[float, List[float]], List[float]],
        t_start: float,
        t_end: float,
        y0: Sequence[float],
        steps: int,
        method: str = "rk4"
    ) -> Tuple[List[float], List[List[float]]]:
        """Integrates ODE system over a time horizon."""
        dt = (t_end - t_start) / float(steps)
        times = [t_start]
        states = [list(y0)]

        curr_t = t_start
        curr_y = list(y0)

        step_fn = cls.rk4_step if method == "rk4" else (cls.midpoint_step if method == "rk2" else cls.euler_step)

        for _ in range(steps):
            curr_y = step_fn(f, curr_t, curr_y, dt)
            curr_t += dt
            times.append(curr_t)
            states.append(curr_y)

        return times, states
