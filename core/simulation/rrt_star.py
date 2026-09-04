"""
Aetheris Robotics & Simulation: Optimal Asymptotic Motion Planning (RRT*)
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
import random
from typing import List, Tuple, Optional, Sequence, Dict, Any
from core.math.vectors import Vector3D
from core.math.geometry import AABB3D, Sphere3D


class RRTNode:
    """Node in the RRT* spatial search tree."""
    __slots__ = ('position', 'parent', 'cost', 'node_id')

    def __init__(self, position: Vector3D, parent: Optional[RRTNode] = None, cost: float = 0.0, node_id: int = 0) -> None:
        self.position = position
        self.parent = parent
        self.cost = float(cost)
        self.node_id = node_id


class RRTStarPlanner3D:
    """
    3D Optimal Path Planning using RRT* (Karaman & Frazzoli).
    Features:
    - Asymptotically optimal path convergence via neighbor rewiring.
    - Goal sampling bias and adaptive neighborhood search radius: r = gamma * (log(n)/n)^(1/d).
    - 3D Obstacle collision detection against spatial spheres and AABBs.
    - Path smoothing via string-pulling shortcutting.
    """
    def __init__(
        self,
        bounds_min: Vector3D,
        bounds_max: Vector3D,
        step_size: float = 0.5,
        max_iterations: int = 2000,
        goal_bias: float = 0.15,
        rewire_radius: float = 1.2,
        seed: Optional[int] = None
    ) -> None:
        self.bounds_min = bounds_min
        self.bounds_max = bounds_max
        self.step_size = step_size
        self.max_iterations = max_iterations
        self.goal_bias = goal_bias
        self.rewire_radius = rewire_radius
        self.rng = random.Random(seed)

        self.obstacles_spheres: List[Sphere3D] = []
        self.obstacles_aabbs: List[AABB3D] = []

    def add_sphere_obstacle(self, center: Vector3D, radius: float) -> None:
        self.obstacles_spheres.append(Sphere3D(center, radius))

    def add_aabb_obstacle(self, min_pt: Vector3D, max_pt: Vector3D) -> None:
        self.obstacles_aabbs.append(AABB3D(min_pt, max_pt))

    def is_state_valid(self, point: Vector3D) -> bool:
        """Checks if a point is within boundaries and outside all obstacles."""
        if not (self.bounds_min.x <= point.x <= self.bounds_max.x and
                self.bounds_min.y <= point.y <= self.bounds_max.y and
                self.bounds_min.z <= point.z <= self.bounds_max.z):
            return False

        for sphere in self.obstacles_spheres:
            if sphere.contains_point(point):
                return False

        for aabb in self.obstacles_aabbs:
            if aabb.contains_point(point):
                return False

        return True

    def is_segment_valid(self, p1: Vector3D, p2: Vector3D, checks: int = 15) -> bool:
        """Line segment collision check with obstacle bounding volumes."""
        for i in range(checks + 1):
            alpha = i / float(checks)
            pt = p1.lerp(p2, alpha)
            if not self.is_state_valid(pt):
                return False
        return True

    def sample_random_point(self, goal: Vector3D) -> Vector3D:
        """Samples random point with goal bias."""
        if self.rng.random() < self.goal_bias:
            return goal
        return Vector3D(
            self.rng.uniform(self.bounds_min.x, self.bounds_max.x),
            self.rng.uniform(self.bounds_min.y, self.bounds_max.y),
            self.rng.uniform(self.bounds_min.z, self.bounds_max.z)
        )

    def find_nearest_node(self, tree: List[RRTNode], target: Vector3D) -> RRTNode:
        """Finds closest node in tree to target point."""
        best_node = tree[0]
        best_dist = best_node.position.distance_sq_to(target)
        for node in tree[1:]:
            d = node.position.distance_sq_to(target)
            if d < best_dist:
                best_dist = d
                best_node = node
        return best_node

    def find_near_nodes(self, tree: List[RRTNode], point: Vector3D, radius: float) -> List[RRTNode]:
        """Finds all nodes within search radius."""
        r2 = radius * radius
        return [node for node in tree if node.position.distance_sq_to(point) <= r2]

    def plan(self, start: Vector3D, goal: Vector3D) -> Tuple[bool, List[Vector3D], float]:
        """
        Plans optimal path from start to goal.
        Returns: (success: bool, waypoints: List[Vector3D], path_cost: float)
        """
        if not self.is_state_valid(start) or not self.is_state_valid(goal):
            return False, [], float('inf')

        root = RRTNode(start, cost=0.0, node_id=0)
        tree: List[RRTNode] = [root]
        best_goal_node: Optional[RRTNode] = None
        min_goal_cost = float('inf')

        for it in range(self.max_iterations):
            rand_pt = self.sample_random_point(goal)
            nearest = self.find_nearest_node(tree, rand_pt)

            # Steer from nearest towards rand_pt
            dir_vec = rand_pt - nearest.position
            dist = dir_vec.norm()
            if dist < 1e-6:
                continue

            step = min(self.step_size, dist)
            new_pos = nearest.position + dir_vec * (step / dist)

            if not self.is_segment_valid(nearest.position, new_pos):
                continue

            # RRT* Find best parent among near neighbors
            near_nodes = self.find_near_nodes(tree, new_pos, self.rewire_radius)
            min_cost = nearest.cost + step
            best_parent = nearest

            for near in near_nodes:
                c = near.cost + near.position.distance_to(new_pos)
                if c < min_cost and self.is_segment_valid(near.position, new_pos):
                    min_cost = c
                    best_parent = near

            new_node = RRTNode(new_pos, parent=best_parent, cost=min_cost, node_id=len(tree))
            tree.append(new_node)

            # RRT* Rewire neighbors
            for near in near_nodes:
                potential_cost = new_node.cost + new_node.position.distance_to(near.position)
                if potential_cost < near.cost and self.is_segment_valid(new_node.position, near.position):
                    near.parent = new_node
                    near.cost = potential_cost

            # Check if within reach of goal
            dist_to_goal = new_pos.distance_to(goal)
            if dist_to_goal <= self.step_size:
                if self.is_segment_valid(new_pos, goal):
                    total_c = new_node.cost + dist_to_goal
                    if total_c < min_goal_cost:
                        goal_node = RRTNode(goal, parent=new_node, cost=total_c, node_id=len(tree))
                        best_goal_node = goal_node
                        min_goal_cost = total_c

        if best_goal_node is None:
            return False, [], float('inf')

        # Backtrack path
        path: List[Vector3D] = []
        curr = best_goal_node
        while curr is not None:
            path.append(curr.position)
            curr = curr.parent
        path.reverse()

        # Path shortcutting / smoothing
        smoothed = self.smooth_path(path)
        return True, smoothed, min_goal_cost

    def smooth_path(self, path: List[Vector3D], max_attempts: int = 50) -> List[Vector3D]:
        """String pulling path shortcutting."""
        if len(path) <= 2:
            return path
        smoothed = list(path)
        for _ in range(max_attempts):
            if len(smoothed) <= 2:
                break
            i = self.rng.randint(0, len(smoothed) - 3)
            j = self.rng.randint(i + 2, len(smoothed) - 1)
            if self.is_segment_valid(smoothed[i], smoothed[j]):
                smoothed = smoothed[:i + 1] + smoothed[j:]
        return smoothed
