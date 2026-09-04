"""
Aetheris Robotics & Simulation: Minimum Jerk Trajectory Planning & Quintic Profiles
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
from typing import List, Tuple, Sequence, Optional
from core.math.vectors import Vector3D


class QuinticPolynomial1D:
    """
    1D Minimum-Jerk Quintic Polynomial:
    s(t) = a0 + a1*t + a2*t^2 + a3*t^3 + a4*t^4 + a5*t^5
    Boundary conditions: s(0), v(0), a(0), s(T), v(T), a(T)
    """
    __slots__ = ('a0', 'a1', 'a2', 'a3', 'a4', 'a5', 't_duration')

    def __init__(
        self,
        x0: float, v0: float, a0: float,
        x1: float, v1: float, a1: float,
        duration: float
    ) -> None:
        if duration <= 1e-6:
            raise ValueError("Trajectory duration must be > 0")
        self.t_duration = float(duration)
        T = self.t_duration
        T2 = T * T
        T3 = T2 * T
        T4 = T3 * T
        T5 = T4 * T

        self.a0 = float(x0)
        self.a1 = float(v0)
        self.a2 = 0.5 * float(a0)

        # Solve linear 3x3 system for [a3, a4, a5]
        # x1 - a0 - a1*T - a2*T^2 = a3*T^3 + a4*T^4 + a5*T^5
        # v1 - a1 - 2*a2*T = 3*a3*T^2 + 4*a4*T^3 + 5*a5*T^4
        # a1_end - 2*a2 = 6*a3*T + 12*a4*T^2 + 20*a5*T^3
        b0 = x1 - self.a0 - self.a1 * T - self.a2 * T2
        b1 = v1 - self.a1 - 2.0 * self.a2 * T
        b2 = a1 - 2.0 * self.a2

        self.a3 = (10.0 * b0 / T3) - (4.0 * b1 / T2) + (0.5 * b2 / T)
        self.a4 = (-15.0 * b0 / T4) + (7.0 * b1 / T3) - (1.0 * b2 / T2)
        self.a5 = (6.0 * b0 / T5) - (3.0 * b1 / T4) + (0.5 * b2 / T3)

    def position(self, t: float) -> float:
        t = max(0.0, min(self.t_duration, float(t)))
        t2 = t * t
        t3 = t2 * t
        t4 = t3 * t
        t5 = t4 * t
        return self.a0 + self.a1 * t + self.a2 * t2 + self.a3 * t3 + self.a4 * t4 + self.a5 * t5

    def velocity(self, t: float) -> float:
        t = max(0.0, min(self.t_duration, float(t)))
        t2 = t * t
        t3 = t2 * t
        t4 = t3 * t
        return self.a1 + 2.0 * self.a2 * t + 3.0 * self.a3 * t2 + 4.0 * self.a4 * t3 + 5.0 * self.a5 * t4

    def acceleration(self, t: float) -> float:
        t = max(0.0, min(self.t_duration, float(t)))
        t2 = t * t
        t3 = t2 * t
        return 2.0 * self.a2 + 6.0 * self.a3 * t + 12.0 * self.a4 * t2 + 20.0 * self.a5 * t3

    def jerk(self, t: float) -> float:
        t = max(0.0, min(self.t_duration, float(t)))
        t2 = t * t
        return 6.0 * self.a3 + 24.0 * self.a4 * t + 60.0 * self.a5 * t2


class TrajectoryGenerator3D:
    """
    Minimum-jerk continuous 3D multi-segment trajectory generator across waypoints.
    Produces smooth C2-continuous position, velocity, and acceleration profiles.
    """
    def __init__(self, waypoints: Sequence[Vector3D], average_speed: float = 1.0) -> None:
        if len(waypoints) < 2:
            raise ValueError("TrajectoryGenerator3D requires at least 2 waypoints")
        self.waypoints = list(waypoints)
        self.average_speed = max(0.01, float(average_speed))
        
        self.segments_x: List[QuinticPolynomial1D] = []
        self.segments_y: List[QuinticPolynomial1D] = []
        self.segments_z: List[QuinticPolynomial1D] = []
        self.segment_durations: List[float] = []
        self.cumulative_times: List[float] = [0.0]
        
        self._build_trajectory()

    def _build_trajectory(self) -> None:
        n = len(self.waypoints)
        for i in range(n - 1):
            p0 = self.waypoints[i]
            p1 = self.waypoints[i + 1]
            dist = p0.distance_to(p1)
            duration = max(0.2, dist / self.average_speed)
            
            # Boundary conditions: start and stop at rest at endpoints
            v0 = 0.0 if i == 0 else 0.2
            v1 = 0.0 if i == n - 2 else 0.2
            
            poly_x = QuinticPolynomial1D(p0.x, 0.0, 0.0, p1.x, 0.0, 0.0, duration)
            poly_y = QuinticPolynomial1D(p0.y, 0.0, 0.0, p1.y, 0.0, 0.0, duration)
            poly_z = QuinticPolynomial1D(p0.z, 0.0, 0.0, p1.z, 0.0, 0.0, duration)
            
            self.segments_x.append(poly_x)
            self.segments_y.append(poly_y)
            self.segments_z.append(poly_z)
            self.segment_durations.append(duration)
            self.cumulative_times.append(self.cumulative_times[-1] + duration)

    @property
    def total_duration(self) -> float:
        return self.cumulative_times[-1]

    def evaluate(self, t: float) -> Tuple[Vector3D, Vector3D, Vector3D]:
        """Returns (position, velocity, acceleration) at time t."""
        t_clamped = max(0.0, min(self.total_duration, float(t)))
        
        # Find segment
        idx = 0
        while idx < len(self.segment_durations) - 1 and t_clamped > self.cumulative_times[idx + 1]:
            idx += 1
            
        t_local = t_clamped - self.cumulative_times[idx]
        
        px = self.segments_x[idx].position(t_local)
        py = self.segments_y[idx].position(t_local)
        pz = self.segments_z[idx].position(t_local)
        
        vx = self.segments_x[idx].velocity(t_local)
        vy = self.segments_y[idx].velocity(t_local)
        vz = self.segments_z[idx].velocity(t_local)
        
        ax = self.segments_x[idx].acceleration(t_local)
        ay = self.segments_y[idx].acceleration(t_local)
        az = self.segments_z[idx].acceleration(t_local)
        
        return (Vector3D(px, py, pz), Vector3D(vx, vy, vz), Vector3D(ax, ay, az))
