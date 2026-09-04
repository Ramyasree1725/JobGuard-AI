"""
JobGuard Core Optimization - Particle Swarm Optimization (PSO)
Continuous population-based global search algorithm with inertia weight damping
and cognitive/social acceleration coefficients.
"""

import math
import random
from typing import List, Tuple, Callable, Optional


class ParticleSwarmOptimizer:
    """Standard Global-Best Particle Swarm Optimizer."""

    def __init__(
        self,
        dimension: int,
        cost_fn: Callable[[List[float]], float],
        num_particles: int = 30,
        inertia_weight: float = 0.7,
        c1: float = 1.4,  # Cognitive component
        c2: float = 1.4,  # Social component
        bounds: Optional[List[Tuple[float, float]]] = None
    ):
        self.d = dimension
        self.cost_fn = cost_fn
        self.num_particles = num_particles
        self.w = inertia_weight
        self.c1 = c1
        self.c2 = c2
        self.bounds = bounds or [(-5.0, 5.0)] * dimension

    def optimize(self, iterations: int = 100) -> Tuple[List[float], float]:
        # Initialize swarm
        positions: List[List[float]] = []
        velocities: List[List[float]] = []
        p_best_pos: List[List[float]] = []
        p_best_cost: List[float] = []

        g_best_pos: List[float] = []
        g_best_cost = float("inf")

        for _ in range(self.num_particles):
            pos = [random.uniform(self.bounds[i][0], self.bounds[i][1]) for i in range(self.d)]
            vel = [random.uniform(-1.0, 1.0) for _ in range(self.d)]
            cost = self.cost_fn(pos)

            positions.append(pos)
            velocities.append(vel)
            p_best_pos.append(list(pos))
            p_best_cost.append(cost)

            if cost < g_best_cost:
                g_best_cost = cost
                g_best_pos = list(pos)

        # Iteration loop
        for _ in range(iterations):
            for i in range(self.num_particles):
                for j in range(self.d):
                    r1 = random.random()
                    r2 = random.random()

                    # Velocity update: v = w*v + c1*r1*(pbest - x) + c2*r2*(gbest - x)
                    velocities[i][j] = (
                        self.w * velocities[i][j] +
                        self.c1 * r1 * (p_best_pos[i][j] - positions[i][j]) +
                        self.c2 * r2 * (g_best_pos[j] - positions[i][j])
                    )

                    # Position update
                    positions[i][j] += velocities[i][j]
                    # Clamp to bounds
                    positions[i][j] = max(self.bounds[j][0], min(self.bounds[j][1], positions[i][j]))

                cost = self.cost_fn(positions[i])

                if cost < p_best_cost[i]:
                    p_best_cost[i] = cost
                    p_best_pos[i] = list(positions[i])

                if cost < g_best_cost:
                    g_best_cost = cost
                    g_best_pos = list(positions[i])

        return g_best_pos, round(g_best_cost, 4)
