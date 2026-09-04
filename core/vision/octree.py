"""
Aetheris Computer Vision & Spatial: Hierarchical 8-ary Spatial Octree
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
from typing import List, Optional, Sequence, Tuple
from core.math.vectors import Vector3D
from core.math.geometry import AABB3D


class OctreeNode:
    """Node in 3D Octree hierarchy."""
    __slots__ = ('bounds', 'points', 'children', 'is_leaf', 'max_points')

    def __init__(self, bounds: AABB3D, max_points: int = 16) -> None:
        self.bounds = bounds
        self.points: List[Vector3D] = []
        self.children: Optional[List[OctreeNode]] = None
        self.is_leaf = True
        self.max_points = max_points

    def subdivide(self) -> None:
        min_p = self.bounds.min_pt
        max_p = self.bounds.max_pt
        mid = self.bounds.center()

        self.children = []
        # 8 octants
        for x_step in [(min_p.x, mid.x), (mid.x, max_p.x)]:
            for y_step in [(min_p.y, mid.y), (mid.y, max_p.y)]:
                for z_step in [(min_p.z, mid.z), (mid.z, max_p.z)]:
                    child_bounds = AABB3D(
                        Vector3D(x_step[0], y_step[0], z_step[0]),
                        Vector3D(x_step[1], y_step[1], z_step[1])
                    )
                    self.children.append(OctreeNode(child_bounds, self.max_points))

        self.is_leaf = False

        # Re-insert existing points into children
        existing = self.points
        self.points = []
        for p in existing:
            self.insert(p)

    def insert(self, p: Vector3D) -> bool:
        if not self.bounds.contains_point(p):
            return False

        if self.is_leaf:
            if len(self.points) < self.max_points:
                self.points.append(p)
                return True
            else:
                self.subdivide()

        if self.children is not None:
            for child in self.children:
                if child.insert(p):
                    return True

        return False

    def query_radius(self, center: Vector3D, radius: float, results: List[Vector3D]) -> None:
        r2 = radius * radius
        if self.is_leaf:
            for p in self.points:
                if center.distance_sq_to(p) <= r2:
                    results.append(p)
        else:
            if self.children is not None:
                for child in self.children:
                    # Quick bounding check: distance to AABB center < radius + AABB diagonal
                    diag = child.bounds.extents().norm()
                    if child.bounds.center().distance_to(center) <= (radius + diag):
                        child.query_radius(center, radius, results)


class Octree3D:
    """Root 3D Octree manager for fast spatial spatial queries and nearest-neighbor lookups."""
    def __init__(self, bounds_min: Vector3D, bounds_max: Vector3D, max_points_per_leaf: int = 16) -> None:
        self.root = OctreeNode(AABB3D(bounds_min, bounds_max), max_points=max_points_per_leaf)
        self.total_points = 0

    def insert(self, pt: Vector3D) -> bool:
        if self.root.insert(pt):
            self.total_points += 1
            return True
        return False

    def build_from_points(self, points: Sequence[Vector3D]) -> None:
        for p in points:
            self.insert(p)

    def query_radius(self, center: Vector3D, radius: float) -> List[Vector3D]:
        results: List[Vector3D] = []
        self.root.query_radius(center, radius, results)
        return results
