"""
JobGuard Core Optimization - Whale Optimization Algorithm (WOA) & Salp Swarm Algorithm (SSA)
Implements spiral bubble-net hunting maneuvers and salp chain foraging leaders for hyperparameter tuning.
"""

import math
import random
from typing import List, Tuple, Callable, Optional


class WhaleOptimizationAlgorithm:
    """Whale Optimization Algorithm (WOA) mimicking humpback whale bubble-net hunting strategy."""

    def __init__(
        self,
        dimension: int,
        cost_fn: Callable[[List[float]], float],
        num_whales: int = 25,
        b_spiral: float = 0.5,
        bounds: Optional[List[Tuple[float, float]]] = None
    ):
        self.d = dimension
        self.cost_fn = cost_fn
        self.num_whales = num_whales
        self.b = b_spiral
        self.bounds = bounds or [(-5.0, 5.0)] * dimension

    def optimize(self, max_iter: int = 80) -> Tuple[List[float], float]:
        whales = [
            [random.uniform(self.bounds[j][0], self.bounds[j][1]) for j in range(self.d)]
            for _ in range(self.num_whales)
        ]
        fitness = [self.cost_fn(w) for w in whales]

        best_idx = min(range(self.num_whales), key=lambda i: fitness[i])
        leader_pos = list(whales[best_idx])
        leader_score = fitness[best_idx]

        for t in range(max_iter):
            # a decreases linearly from 2 to 0
            a = 2.0 - t * (2.0 / max_iter)

            for i in range(self.num_whales):
                r1 = random.random()
                r2 = random.random()
                A = 2.0 * a * r1 - a
                C = 2.0 * r2

                p = random.random()
                l = random.uniform(-1.0, 1.0)

                for j in range(self.d):
                    if p < 0.5:
                        if abs(A) < 1.0:
                            # Encircling prey
                            d_leader = abs(C * leader_pos[j] - whales[i][j])
                            whales[i][j] = leader_pos[j] - A * d_leader
                        else:
                            # Exploration / Search for prey
                            rand_idx = random.randint(0, self.num_whales - 1)
                            rand_whale = whales[rand_idx]
                            d_rand = abs(C * rand_whale[j] - whales[i][j])
                            whales[i][j] = rand_whale[j] - A * d_rand
                    else:
                        # Spiral bubble-net attacking maneuver
                        dist_to_leader = abs(leader_pos[j] - whales[i][j])
                        whales[i][j] = dist_to_leader * math.exp(self.b * l) * math.cos(2.0 * math.pi * l) + leader_pos[j]

                    # Clamp bounds
                    whales[i][j] = max(self.bounds[j][0], min(self.bounds[j][1], whales[i][j]))

                # Update score
                score = self.cost_fn(whales[i])
                if score < leader_score:
                    leader_score = score
                    leader_pos = list(whales[i])

        return leader_pos, round(leader_score, 4)
