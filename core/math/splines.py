"""
Aetheris Mathematical Foundations: Spline Curves & Trajectory Geometry
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
from typing import List, Sequence, Tuple, Optional
from core.math.vectors import Vector3D


class CubicBezier3D:
    """
    Cubic Bezier curve in 3D Euclidean space:
    B(t) = (1-t)^3 P0 + 3(1-t)^2 t P1 + 3(1-t) t^2 P2 + t^3 P3
    """
    __slots__ = ('p0', 'p1', 'p2', 'p3')

    def __init__(self, p0: Vector3D, p1: Vector3D, p2: Vector3D, p3: Vector3D) -> None:
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def evaluate(self, t: float) -> Vector3D:
        """Evaluates position at parameter t in [0.0, 1.0]."""
        t = max(0.0, min(1.0, float(t)))
        u = 1.0 - t
        tt = t * t
        uu = u * u
        uuu = uu * u
        ttt = tt * t

        p = self.p0 * uuu
        p += self.p1 * (3.0 * uu * t)
        p += self.p2 * (3.0 * u * tt)
        p += self.p3 * ttt
        return p

    def derivative(self, t: float) -> Vector3D:
        """First derivative (velocity vector) at parameter t."""
        t = max(0.0, min(1.0, float(t)))
        u = 1.0 - t
        d0 = (self.p1 - self.p0) * (3.0 * u * u)
        d1 = (self.p2 - self.p1) * (6.0 * u * t)
        d2 = (self.p3 - self.p2) * (3.0 * t * t)
        return d0 + d1 + d2

    def second_derivative(self, t: float) -> Vector3D:
        """Second derivative (acceleration vector) at parameter t."""
        t = max(0.0, min(1.0, float(t)))
        u = 1.0 - t
        dd0 = (self.p2 - self.p1 * 2.0 + self.p0) * (6.0 * u)
        dd1 = (self.p3 - self.p2 * 2.0 + self.p1) * (6.0 * t)
        return dd0 + dd1

    def curvature(self, t: float) -> float:
        """Calculates scalar curvature kappa = |v x a| / |v|^3."""
        v = self.derivative(t)
        a = self.second_derivative(t)
        v_mag = v.norm()
        if v_mag < 1e-9:
            return 0.0
        cross_mag = v.cross(a).norm()
        return cross_mag / (v_mag ** 3)

    def arc_length(self, samples: int = 100) -> float:
        """Numerical quadrature estimation of curve arc length."""
        total_len = 0.0
        prev_pt = self.evaluate(0.0)
        for i in range(1, samples + 1):
            curr_pt = self.evaluate(i / float(samples))
            total_len += prev_pt.distance_to(curr_pt)
            prev_pt = curr_pt
        return total_len

    def sample_equidistant(self, num_points: int) -> List[Vector3D]:
        """Discretizes curve into approximate equidistant waypoints."""
        if num_points <= 1:
            return [self.p0]
        # Precompute dense cumulative distances
        dense_samples = 200
        cum_dist = [0.0]
        pts = [self.evaluate(0.0)]
        for i in range(1, dense_samples + 1):
            pt = self.evaluate(i / float(dense_samples))
            pts.append(pt)
            cum_dist.append(cum_dist[-1] + pts[-2].distance_to(pt))
        
        total_len = cum_dist[-1]
        step = total_len / float(num_points - 1)
        res = [self.p0]
        
        target_d = step
        idx = 0
        for _ in range(num_points - 2):
            while idx < dense_samples and cum_dist[idx + 1] < target_d:
                idx += 1
            segment_len = cum_dist[idx + 1] - cum_dist[idx]
            alpha = (target_d - cum_dist[idx]) / segment_len if segment_len > 1e-12 else 0.0
            res.append(pts[idx].lerp(pts[idx + 1], alpha))
            target_d += step
            
        res.append(self.p3)
        return res


class CatmullRomSpline3D:
    """
    Smooth C1-continuous Catmull-Rom spline passing directly through all given control points.
    Ideal for autonomous vehicle path smoothing and camera flight paths.
    """
    def __init__(self, control_points: Sequence[Vector3D], tension: float = 0.5) -> None:
        if len(control_points) < 2:
            raise ValueError("CatmullRomSpline3D requires at least 2 control points")
        self.points: List[Vector3D] = list(control_points)
        self.tension: float = float(tension)

    def evaluate(self, t_global: float) -> Vector3D:
        """
        Global parameter t in [0.0, len(points) - 1].
        """
        n = len(self.points)
        t_clamped = max(0.0, min(float(n - 1), float(t_global)))
        i = int(math.floor(t_clamped))
        if i >= n - 1:
            return self.points[-1]

        t = t_clamped - i

        p0 = self.points[max(0, i - 1)]
        p1 = self.points[i]
        p2 = self.points[min(n - 1, i + 1)]
        p3 = self.points[min(n - 1, i + 2)]

        # Tangents
        t1 = (p2 - p0) * (1.0 - self.tension) * 0.5
        t2 = (p3 - p1) * (1.0 - self.tension) * 0.5

        # Hermite basis
        t2_val = t * t
        t3_val = t2_val * t

        h00 = 2.0 * t3_val - 3.0 * t2_val + 1.0
        h10 = t3_val - 2.0 * t2_val + t
        h01 = -2.0 * t3_val + 3.0 * t2_val
        h11 = t3_val - t2_val

        return p1 * h00 + t1 * h10 + p2 * h01 + t2 * h11

    def generate_path(self, resolution_per_segment: int = 20) -> List[Vector3D]:
        num_segments = len(self.points) - 1
        path: List[Vector3D] = []
        for s in range(num_segments):
            for step in range(resolution_per_segment):
                t = s + (step / float(resolution_per_segment))
                path.append(self.evaluate(t))
        path.append(self.points[-1])
        return path
