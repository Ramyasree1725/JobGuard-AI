"""
Aetheris Robotics & Simulation: Spatial Hashing & Triangular Collision Meshes
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
from typing import List, Tuple, Dict, Set, Optional
from core.math.vectors import Vector3D
from core.math.geometry import AABB3D, Ray3D


class Triangle3D:
    __slots__ = ('v0', 'v1', 'v2', 'normal')

    def __init__(self, v0: Vector3D, v1: Vector3D, v2: Vector3D) -> None:
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        edge1 = v1 - v0
        edge2 = v2 - v0
        self.normal = edge1.cross(edge2).normalize()

    def get_aabb(self) -> AABB3D:
        min_x = min(self.v0.x, self.v1.x, self.v2.x)
        min_y = min(self.v0.y, self.v1.y, self.v2.y)
        min_z = min(self.v0.z, self.v1.z, self.v2.z)
        max_x = max(self.v0.x, self.v1.x, self.v2.x)
        max_y = max(self.v0.y, self.v1.y, self.v2.y)
        max_z = max(self.v0.z, self.v1.z, self.v2.z)
        return AABB3D(Vector3D(min_x, min_y, min_z), Vector3D(max_x, max_y, max_z))

    def intersect_ray(self, ray: Ray3D) -> Optional[float]:
        """Moller-Trumbore ray-triangle intersection algorithm."""
        edge1 = self.v1 - self.v0
        edge2 = self.v2 - self.v0
        h = ray.direction.cross(edge2)
        a = edge1.dot(h)

        if abs(a) < 1e-12:
            return None # Ray is parallel to triangle

        f = 1.0 / a
        s = ray.origin - self.v0
        u = f * s.dot(h)

        if u < 0.0 or u > 1.0:
            return None

        q = s.cross(edge1)
        v = f * ray.direction.dot(q)

        if v < 0.0 or u + v > 1.0:
            return None

        t = f * edge2.dot(q)
        return t if t >= 1e-6 else None


class SpatialHashGrid3D:
    """O(1) average lookup spatial hash grid for massive triangular mesh collision checking."""
    def __init__(self, cell_size: float = 1.0) -> None:
        self.cell_size = max(0.1, float(cell_size))
        self.inv_cell = 1.0 / self.cell_size
        self.grid: Dict[Tuple[int, int, int], List[Triangle3D]] = {}

    def _hash_coord(self, pt: Vector3D) -> Tuple[int, int, int]:
        return (
            int(math.floor(pt.x * self.inv_cell)),
            int(math.floor(pt.y * self.inv_cell)),
            int(math.floor(pt.z * self.inv_cell))
        )

    def insert_triangle(self, tri: Triangle3D) -> None:
        aabb = tri.get_aabb()
        min_cell = self._hash_coord(aabb.min_pt)
        max_cell = self._hash_coord(aabb.max_pt)

        for cx in range(min_cell[0], max_cell[0] + 1):
            for cy in range(min_cell[1], max_cell[1] + 1):
                for cz in range(min_cell[2], max_cell[2] + 1):
                    key = (cx, cy, cz)
                    if key not in self.grid:
                        self.grid[key] = []
                    self.grid[key].append(tri)

    def query_ray(self, ray: Ray3D, max_distance: float = 100.0) -> Optional[Tuple[float, Triangle3D]]:
        """Finds closest triangle intersected along ray."""
        tested_triangles: Set[int] = set()
        closest_t = max_distance
        hit_tri: Optional[Triangle3D] = None

        # Sample cells along ray
        num_steps = int(max_distance * self.inv_cell * 2) + 1
        for step in range(num_steps):
            t_sample = step * (self.cell_size * 0.5)
            if t_sample > closest_t:
                break
            pt = ray.get_point(t_sample)
            cell_key = self._hash_coord(pt)
            
            if cell_key in self.grid:
                for tri in self.grid[cell_key]:
                    tri_id = id(tri)
                    if tri_id in tested_triangles:
                        continue
                    tested_triangles.add(tri_id)
                    t_hit = tri.intersect_ray(ray)
                    if t_hit is not None and t_hit < closest_t:
                        closest_t = t_hit
                        hit_tri = tri

        if hit_tri is not None:
            return closest_t, hit_tri
        return None
