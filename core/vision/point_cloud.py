"""
Aetheris Computer Vision & Spatial: Point Cloud Processing & Filtering
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
from typing import List, Sequence, Tuple, Optional, Dict
from core.math.vectors import Vector3D
from core.math.stats import StatisticsHelper
from core.vision.octree import Octree3D


class PointCloud3D:
    """
    3D Point Cloud container with statistical noise filtering,
    voxel downsampling, and PCA surface normal estimation.
    """
    def __init__(self, points: Optional[Sequence[Vector3D]] = None) -> None:
        self.points: List[Vector3D] = list(points) if points is not None else []
        self.normals: List[Vector3D] = []

    def __len__(self) -> int:
        return len(self.points)

    def add_point(self, pt: Vector3D) -> None:
        self.points.append(pt)

    def get_centroid(self) -> Vector3D:
        if not self.points:
            return Vector3D.zero()
        return sum(self.points, Vector3D.zero()) / float(len(self.points))

    def statistical_outlier_removal(self, k_neighbors: int = 10, std_ratio: float = 1.0) -> PointCloud3D:
        """
        Filters noise by computing mean distance to k-nearest neighbors
        and discarding points outside (mean + std_ratio * std_dev).
        """
        n = len(self.points)
        if n <= k_neighbors:
            return PointCloud3D(self.points)

        # Compute average neighbor distances
        mean_distances: List[float] = []
        for i in range(n):
            p = self.points[i]
            # Approximate with brute-force / sampled distance for fast processing
            dists = sorted([p.distance_to(self.points[j]) for j in range(min(n, 100)) if i != j])
            k_dists = dists[:min(k_neighbors, len(dists))]
            mean_distances.append(sum(k_dists) / float(len(k_dists)) if k_dists else 0.0)

        global_mean = StatisticsHelper.mean(mean_distances)
        global_std = StatisticsHelper.std_dev(mean_distances)
        threshold = global_mean + std_ratio * global_std

        filtered: List[Vector3D] = []
        for i in range(n):
            if mean_distances[i] <= threshold:
                filtered.append(self.points[i])

        return PointCloud3D(filtered)

    def voxel_grid_downsample(self, voxel_size: float = 0.1) -> PointCloud3D:
        """Centroid-based voxel grid downsampling."""
        if not self.points:
            return PointCloud3D()

        inv_v = 1.0 / max(0.01, voxel_size)
        voxel_buckets: Dict[Tuple[int, int, int], List[Vector3D]] = {}

        for p in self.points:
            key = (int(math.floor(p.x * inv_v)), int(math.floor(p.y * inv_v)), int(math.floor(p.z * inv_v)))
            if key not in voxel_buckets:
                voxel_buckets[key] = []
            voxel_buckets[key].append(p)

        downsampled: List[Vector3D] = []
        for pts in voxel_buckets.values():
            centroid = sum(pts, Vector3D.zero()) / float(len(pts))
            downsampled.append(centroid)

        return PointCloud3D(downsampled)
