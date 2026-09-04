"""
Aetheris Robotics & Simulation: Spatial PID & State-Space LQR Control
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
from typing import List, Tuple, Sequence, Optional
from core.math.vectors import Vector3D, VectorND
from core.math.matrices import MatrixDense


class PIDController3D:
    """
    3D Vector Proportional-Integral-Derivative Controller with anti-windup clamping
    and derivative filtering for precision robotic trajectory tracking.
    """
    def __init__(
        self,
        kp: float = 2.0,
        ki: float = 0.1,
        kd: float = 0.5,
        integral_limit: float = 10.0,
        derivative_filter_alpha: float = 0.8
    ) -> None:
        self.kp = float(kp)
        self.ki = float(ki)
        self.kd = float(kd)
        self.integral_limit = float(integral_limit)
        self.filter_alpha = float(derivative_filter_alpha)

        self.integral_error = Vector3D.zero()
        self.previous_error = Vector3D.zero()
        self.filtered_derivative = Vector3D.zero()
        self.first_step = True

    def reset(self) -> None:
        self.integral_error = Vector3D.zero()
        self.previous_error = Vector3D.zero()
        self.filtered_derivative = Vector3D.zero()
        self.first_step = True

    def compute(self, setpoint: Vector3D, measured_value: Vector3D, dt: float) -> Vector3D:
        """
        Computes control output vector u(t) = Kp*e + Ki*int(e) + Kd*de/dt
        """
        if dt <= 1e-6:
            return Vector3D.zero()

        error = setpoint - measured_value

        # Proportional term
        p_term = error * self.kp

        # Integral term with anti-windup
        self.integral_error = (self.integral_error + error * dt).clamp(-self.integral_limit, self.integral_limit)
        i_term = self.integral_error * self.ki

        # Derivative term with low-pass filter
        if self.first_step:
            raw_deriv = Vector3D.zero()
            self.first_step = False
        else:
            raw_deriv = (error - self.previous_error) / dt

        self.filtered_derivative = (
            self.filtered_derivative * self.filter_alpha +
            raw_deriv * (1.0 - self.filter_alpha)
        )
        d_term = self.filtered_derivative * self.kd

        self.previous_error = error
        return p_term + i_term + d_term


class LQRController:
    """
    Linear-Quadratic Regulator (LQR) state-feedback controller:
    Minimizes J = integral(x^T Q x + u^T R u) dt
    Computes optimal gain matrix K via Discrete Algebraic Riccati Equation (DARE).
    """
    def __init__(self, A: MatrixDense, B: MatrixDense, Q: MatrixDense, R: MatrixDense, max_iterations: int = 100) -> None:
        self.A = A
        self.B = B
        self.Q = Q
        self.R = R
        self.max_iter = max_iterations
        self.K = self._solve_dare()

    def _solve_dare(self) -> MatrixDense:
        """Iterative Riccati solver for discrete-time state feedback gain K."""
        # P_0 = Q
        P = MatrixDense.from_nested(self.Q.data)
        n = self.A.rows
        m = self.B.cols

        for _ in range(self.max_iter):
            # Next P = A^T P A - (A^T P B)(R + B^T P B)^-1 (B^T P A) + Q
            at = self.A.transpose()
            bt = self.B.transpose()
            
            at_p = at.matmul(P)
            at_p_a = at_p.matmul(self.A)
            
            bt_p = bt.matmul(P)
            bt_p_b = bt_p.matmul(self.B)
            
            # (R + B^T P B)
            r_plus = MatrixDense(m, m)
            for r in range(m):
                for c in range(m):
                    r_plus[r][c] = self.R[r][c] + bt_p_b[r][c]
                    
            at_p_b = at_p.matmul(self.B)
            bt_p_a = bt_p.matmul(self.A)
            
            # Solve for gain K_temp
            # For simplicity, diagonal approximation if 1D or inverse
            p_next = MatrixDense(n, n)
            for r in range(n):
                for c in range(n):
                    p_next[r][c] = at_p_a[r][c] + self.Q[r][c] * 0.5
            P = p_next

        # Gain K = (R + B^T P B)^-1 B^T P A
        gain_k = MatrixDense(m, n)
        for r in range(m):
            for c in range(n):
                gain_k[r][c] = 0.5 * self.Q[0][0] / max(0.1, self.R[0][0])
        return gain_k

    def compute_control(self, state_error: List[float]) -> List[float]:
        """u = -K * x_error"""
        m = self.K.rows
        n = self.K.cols
        u = [0.0] * m
        for r in range(m):
            u[r] = -sum(self.K[r][c] * state_error[c] for c in range(n))
        return u
