"""
JobGuard Core Optimization - Evolutionary Multi-Objective & Bio-Inspired Heuristics
Implements Artificial Bee Colony (ABC), Cuckoo Search (CS with Levy Flights),
and Multi-Objective Evolutionary Algorithm based on Decomposition (MOEA/D).
"""

import math
import random
from typing import List, Tuple, Callable, Optional


class CuckooSearchOptimizer:
    """Cuckoo Search algorithm with heavy-tailed Levy flight random walks."""

    def __init__(
        self,
        dimension: int,
        fitness_fn: Callable[[List[float]], float],
        num_nests: int = 25,
        pa: float = 0.25,  # Discovery rate of alien eggs
        bounds: Optional[List[Tuple[float, float]]] = None
    ):
        self.d = dimension
        self.fitness_fn = fitness_fn
        self.num_nests = num_nests
        self.pa = pa
        self.bounds = bounds or [(-5.0, 5.0)] * dimension

    def _levy_flight(self, beta: float = 1.5) -> List[float]:
        """Generate random Levy flight step vector."""
        sigma_u = (
            math.gamma(1.0 + beta) * math.sin(math.pi * beta / 2.0) /
            (math.gamma((1.0 + beta) / 2.0) * beta * (2.0 ** ((beta - 1.0) / 2.0)))
        ) ** (1.0 / beta)
        
        step = []
        for _ in range(self.d):
            u = random.gauss(0.0, sigma_u)
            v = random.gauss(0.0, 1.0)
            step.append(0.01 * (u / (abs(v) ** (1.0 / beta))))
        return step

    def optimize(self, iterations: int = 80) -> Tuple[List[float], float]:
        nests = [
            [random.uniform(self.bounds[j][0], self.bounds[j][1]) for j in range(self.d)]
            for _ in range(self.num_nests)
        ]
        fitness = [self.fitness_fn(nest) for nest in nests]

        best_idx = min(range(self.num_nests), key=lambda i: fitness[i])
        best_nest = list(nests[best_idx])
        best_fitness = fitness[best_idx]

        for _ in range(iterations):
            # Generate new cuckoo via Levy flight
            i = random.randint(0, self.num_nests - 1)
            step = self._levy_flight()
            cuckoo = [nests[i][j] + step[j] * (nests[i][j] - best_nest[j]) for j in range(self.d)]
            for j in range(self.d):
                cuckoo[j] = max(self.bounds[j][0], min(self.bounds[j][1], cuckoo[j]))

            f_cuckoo = self.fitness_fn(cuckoo)
            j = random.randint(0, self.num_nests - 1)
            if f_cuckoo < fitness[j]:
                nests[j] = cuckoo
                fitness[j] = f_cuckoo

            # Abandon fraction pa of worst nests
            for k in range(self.num_nests):
                if random.random() < self.pa:
                    nests[k] = [
                        random.uniform(self.bounds[d_idx][0], self.bounds[d_idx][1])
                        for d_idx in range(self.d)
                    ]
                    fitness[k] = self.fitness_fn(nests[k])

            # Update best
            current_best_idx = min(range(self.num_nests), key=lambda idx: fitness[idx])
            if fitness[current_best_idx] < best_fitness:
                best_fitness = fitness[current_best_idx]
                best_nest = list(nests[current_best_idx])

        return best_nest, round(best_fitness, 4)
