"""
Aetheris Mathematical Foundations: Computational Geometry & Collision Primitives
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
from typing import Tuple, List, Optional
from core.math.vectors import Vector3D


class AABB3D:
    """Axis-Aligned Bounding Box in 3D Euclidean Space."""
    __slots__ = ('min_pt', 'max_pt')

    def __init__(self, min_pt: Vector3D, max_pt: Vector3D) -> None:
        self.min_pt = Vector3D(
            min(min_pt.x, max_pt.x),
            min(min_pt.y, max_pt.y),
            min(min_pt.z, max_pt.z)
        )
        self.max_pt = Vector3D(
            max(min_pt.x, max_pt.x),
            max(min_pt.y, max_pt.y),
            max(min_pt.z, max_pt.z)
        )

    def center(self) -> Vector3D:
        return (self.min_pt + self.max_pt) * 0.5

    def extents(self) -> Vector3D:
        return (self.max_pt - self.min_pt) * 0.5

    def size(self) -> Vector3D:
        return self.max_pt - self.min_pt

    def volume(self) -> float:
        s = self.size()
        return s.x * s.y * s.z

    def contains_point(self, p: Vector3D) -> bool:
        return (
            self.min_pt.x <= p.x <= self.max_pt.x and
            self.min_pt.y <= p.y <= self.max_pt.y and
            self.min_pt.z <= p.z <= self.max_pt.z
        )

    def intersects(self, other: AABB3D) -> bool:
        return not (
            self.max_pt.x < other.min_pt.x or self.min_pt.x > other.max_pt.x or
            self.max_pt.y < other.min_pt.y or self.min_pt.y > other.max_pt.y or
            self.max_pt.z < other.min_pt.z or self.min_pt.z > other.max_pt.z
        )

    def expand_to_contain(self, p: Vector3D) -> None:
        self.min_pt.x = min(self.min_pt.x, p.x)
        self.min_pt.y = min(self.min_pt.y, p.y)
        self.min_pt.z = min(self.min_pt.z, p.z)
        self.max_pt.x = max(self.max_pt.x, p.x)
        self.max_pt.y = max(self.max_pt.y, p.y)
        self.max_pt.z = max(self.max_pt.z, p.z)


class Sphere3D:
    """Bounding Sphere primitive."""
    __slots__ = ('center', 'radius')

    def __init__(self, center: Vector3D, radius: float) -> None:
        self.center = center
        self.radius = max(0.0, float(radius))

    def contains_point(self, p: Vector3D) -> bool:
        return self.center.distance_sq_to(p) <= (self.radius * self.radius)

    def intersects_sphere(self, other: Sphere3D) -> bool:
        r_sum = self.radius + other.radius
        return self.center.distance_sq_to(other.center) <= (r_sum * r_sum)

    def intersects_aabb(self, aabb: AABB3D) -> bool:
        # Closest point on AABB to sphere center
        closest_x = max(aabb.min_pt.x, min(self.center.x, aabb.max_pt.x))
        closest_y = max(aabb.min_pt.y, min(self.center.y, aabb.max_pt.y))
        closest_z = max(aabb.min_pt.z, min(self.center.z, aabb.max_pt.z))
        closest = Vector3D(closest_x, closest_y, closest_z)
        return self.center.distance_sq_to(closest) <= (self.radius * self.radius)


class Ray3D:
    """Ray defined by origin and unit direction vector."""
    __slots__ = ('origin', 'direction')

    def __init__(self, origin: Vector3D, direction: Vector3D) -> None:
        self.origin = origin
        self.direction = direction.normalize()

    def get_point(self, distance: float) -> Vector3D:
        return self.origin + self.direction * distance

    def intersect_sphere(self, sphere: Sphere3D) -> Optional[float]:
        """Returns distance t to first intersection or None."""
        oc = self.origin - sphere.center
        b = oc.dot(self.direction)
        c = oc.dot(oc) - sphere.radius * sphere.radius
        discriminant = b * b - c
        if discriminant < 0.0:
            return None
        sqrt_d = math.sqrt(discriminant)
        t = -b - sqrt_d
        if t >= 0.0:
            return t
        t2 = -b + sqrt_d
        return t2 if t2 >= 0.0 else None

    def intersect_aabb(self, aabb: AABB3D) -> Optional[float]:
        """Slab method for Ray-AABB intersection."""
        t_min = -float('inf')
        t_max = float('inf')

        for i in range(3):
            orig = self.origin[i]
            dir_comp = self.direction[i]
            b_min = aabb.min_pt[i]
            b_max = aabb.max_pt[i]

            if abs(dir_comp) < 1e-12:
                if orig < b_min or orig > b_max:
                    return None
            else:
                t1 = (b_min - orig) / dir_comp
                t2 = (b_max - orig) / dir_comp
                if t1 > t2:
                    t1, t2 = t2, t1
                t_min = max(t_min, t1)
                t_max = min(t_max, t2)
                if t_min > t_max or t_max < 0.0:
                    return None

        return t_min if t_min >= 0.0 else t_max
