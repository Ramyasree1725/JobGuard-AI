"""
Aetheris Computer Vision & Spatial: 3D Voxel Occupancy Grid & DDA Raymarching
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
from typing import List, Tuple, Dict, Set, Optional, Sequence
from core.math.vectors import Vector3D
from core.math.geometry import AABB3D, Ray3D


class VoxelGrid3D:
    """
    Dense and Sparse 3D Voxel Occupancy Grid for spatial robotics mapping,
    point cloud voxelization, and fast Amanatides-Woo DDA raymarching.
    """
    def __init__(
        self,
        bounds_min: Vector3D,
        bounds_max: Vector3D,
        voxel_size: float = 0.2
    ) -> None:
        self.bounds_min = bounds_min
        self.bounds_max = bounds_max
        self.voxel_size = max(0.01, float(voxel_size))
        self.inv_voxel_size = 1.0 / self.voxel_size

        # Grid dimensions
        self.dim_x = int(math.ceil((bounds_max.x - bounds_min.x) * self.inv_voxel_size))
        self.dim_y = int(math.ceil((bounds_max.y - bounds_min.y) * self.inv_voxel_size))
        self.dim_z = int(math.ceil((bounds_max.z - bounds_min.z) * self.inv_voxel_size))

        # Sparse occupancy set of (ix, iy, iz)
        self.occupied_voxels: Set[Tuple[int, int, int]] = set()
        self.voxel_densities: Dict[Tuple[int, int, int], float] = {}

    def world_to_grid(self, pt: Vector3D) -> Optional[Tuple[int, int, int]]:
        """Converts world continuous 3D coordinate to integer voxel indices (ix, iy, iz)."""
        if not (self.bounds_min.x <= pt.x <= self.bounds_max.x and
                self.bounds_min.y <= pt.y <= self.bounds_max.y and
                self.bounds_min.z <= pt.z <= self.bounds_max.z):
            return None

        ix = int((pt.x - self.bounds_min.x) * self.inv_voxel_size)
        iy = int((pt.y - self.bounds_min.y) * self.inv_voxel_size)
        iz = int((pt.z - self.bounds_min.z) * self.inv_voxel_size)

        ix = max(0, min(self.dim_x - 1, ix))
        iy = max(0, min(self.dim_y - 1, iy))
        iz = max(0, min(self.dim_z - 1, iz))
        return (ix, iy, iz)

    def grid_to_world_center(self, ix: int, iy: int, iz: int) -> Vector3D:
        """Converts grid voxel indices to world coordinate center point."""
        return Vector3D(
            self.bounds_min.x + (ix + 0.5) * self.voxel_size,
            self.bounds_min.y + (iy + 0.5) * self.voxel_size,
            self.bounds_min.z + (iz + 0.5) * self.voxel_size
        )

    def insert_point(self, pt: Vector3D, weight: float = 1.0) -> bool:
        coords = self.world_to_grid(pt)
        if coords is None:
            return False
        self.occupied_voxels.add(coords)
        self.voxel_densities[coords] = self.voxel_densities.get(coords, 0.0) + weight
        return True

    def insert_point_cloud(self, points: Sequence[Vector3D]) -> int:
        count = 0
        for p in points:
            if self.insert_point(p):
                count += 1
        return count

    def is_occupied(self, ix: int, iy: int, iz: int) -> bool:
        return (ix, iy, iz) in self.occupied_voxels

    def raymarch_dda(self, ray: Ray3D, max_dist: float = 50.0) -> Optional[Tuple[Vector3D, Tuple[int, int, int]]]:
        """
        Fast 3D Digital Differential Analyzer (DDA) Ray traversal (Amanatides-Woo).
        Finds first occupied voxel along ray.
        """
        start_pt = ray.origin
        curr_grid = self.world_to_grid(start_pt)
        if curr_grid is None:
            # Check if ray enters bounding box
            aabb = AABB3D(self.bounds_min, self.bounds_max)
            t_enter = ray.intersect_aabb(aabb)
            if t_enter is None or t_enter > max_dist:
                return None
            start_pt = ray.get_point(t_enter + 1e-4)
            curr_grid = self.world_to_grid(start_pt)
            if curr_grid is None:
                return None

        ix, iy, iz = curr_grid
        step_x = 1 if ray.direction.x >= 0 else -1
        step_y = 1 if ray.direction.y >= 0 else -1
        step_z = 1 if ray.direction.z >= 0 else -1

        voxel_bounds_x = self.bounds_min.x + (ix + (1 if step_x > 0 else 0)) * self.voxel_size
        voxel_bounds_y = self.bounds_min.y + (iy + (1 if step_y > 0 else 0)) * self.voxel_size
        voxel_bounds_z = self.bounds_min.z + (iz + (1 if step_z > 0 else 0)) * self.voxel_size

        t_max_x = (voxel_bounds_x - start_pt.x) / ray.direction.x if abs(ray.direction.x) > 1e-12 else float('inf')
        t_max_y = (voxel_bounds_y - start_pt.y) / ray.direction.y if abs(ray.direction.y) > 1e-12 else float('inf')
        t_max_z = (voxel_bounds_z - start_pt.z) / ray.direction.z if abs(ray.direction.z) > 1e-12 else float('inf')

        t_delta_x = abs(self.voxel_size / ray.direction.x) if abs(ray.direction.x) > 1e-12 else float('inf')
        t_delta_y = abs(self.voxel_size / ray.direction.y) if abs(ray.direction.y) > 1e-12 else float('inf')
        t_delta_z = abs(self.voxel_size / ray.direction.z) if abs(ray.direction.z) > 1e-12 else float('inf')

        t_traveled = 0.0
        max_steps = self.dim_x + self.dim_y + self.dim_z

        for _ in range(max_steps):
            if (ix, iy, iz) in self.occupied_voxels:
                hit_pt = ray.get_point(t_traveled)
                return hit_pt, (ix, iy, iz)

            if t_max_x < t_max_y:
                if t_max_x < t_max_z:
                    ix += step_x
                    t_traveled = t_max_x
                    t_max_x += t_delta_x
                else:
                    iz += step_z
                    t_traveled = t_max_z
                    t_max_z += t_delta_z
            else:
                if t_max_y < t_max_z:
                    iy += step_y
                    t_traveled = t_max_y
                    t_max_y += t_delta_y
                else:
                    iz += step_z
                    t_traveled = t_max_z
                    t_max_z += t_delta_z

            if ix < 0 or ix >= self.dim_x or iy < 0 or iy >= self.dim_y or iz < 0 or iz >= self.dim_z or t_traveled > max_dist:
                break

        return None

    def get_occupied_centers(self) -> List[Vector3D]:
        return [self.grid_to_world_center(ix, iy, iz) for (ix, iy, iz) in self.occupied_voxels]
