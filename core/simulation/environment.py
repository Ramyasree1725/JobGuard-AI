"""
Aetheris Robotics & Simulation: Dynamic 3D Simulation Environment
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
from typing import List, Dict, Any, Optional
from core.math.vectors import Vector3D
from core.math.geometry import AABB3D, Sphere3D


class SimulationEnvironment3D:
    """
    3D Virtual Testing Environment with boundaries, static obstacles,
    dynamic waypoints, target zones, and physical boundaries.
    """
    def __init__(self, bounds_size: float = 30.0) -> None:
        half = bounds_size * 0.5
        self.bounds = AABB3D(Vector3D(-half, -half, 0.0), Vector3D(half, half, bounds_size))
        self.spheres: List[Dict[str, Any]] = []
        self.aabbs: List[Dict[str, Any]] = []
        self.target_position = Vector3D(8.0, 8.0, 4.0)
        self.waypoints: List[Vector3D] = []
        
        self._populate_default_world()

    def _populate_default_world(self) -> None:
        # Add research obstacle spheres
        self.add_sphere("col_sphere_1", Vector3D(3.0, 2.0, 2.5), 1.2)
        self.add_sphere("col_sphere_2", Vector3D(-4.0, 3.0, 3.0), 1.5)
        self.add_sphere("col_sphere_3", Vector3D(1.0, -5.0, 2.0), 1.0)
        
        # Add box obstacles
        self.add_box("col_box_1", Vector3D(-2.0, -2.0, 0.0), Vector3D(-0.5, 0.5, 3.5))
        self.add_box("col_box_2", Vector3D(4.0, -4.0, 0.0), Vector3D(6.0, -2.0, 4.0))

    def add_sphere(self, name: str, center: Vector3D, radius: float) -> None:
        self.spheres.append({
            "name": name,
            "center": center,
            "radius": radius,
            "shape": Sphere3D(center, radius)
        })

    def add_box(self, name: str, min_pt: Vector3D, max_pt: Vector3D) -> None:
        self.aabbs.append({
            "name": name,
            "min_pt": min_pt,
            "max_pt": max_pt,
            "shape": AABB3D(min_pt, max_pt)
        })

    def get_sphere_shapes(self) -> List[Sphere3D]:
        return [s["shape"] for s in self.spheres]

    def get_aabb_shapes(self) -> List[AABB3D]:
        return [b["shape"] for b in self.aabbs]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bounds": {
                "min": self.bounds.min_pt.to_list(),
                "max": self.bounds.max_pt.to_list()
            },
            "target": self.target_position.to_list(),
            "spheres": [
                {"name": s["name"], "center": s["center"].to_list(), "radius": s["radius"]}
                for s in self.spheres
            ],
            "boxes": [
                {"name": b["name"], "min": b["min_pt"].to_list(), "max": b["max_pt"].to_list()}
                for b in self.aabbs
            ]
        }
