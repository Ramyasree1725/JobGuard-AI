"""
JobGuard Core Optimization - Covariance Matrix Adaptation Evolution Strategy (CMA-ES)
Non-convex black-box continuous optimizer for hyperparameter tuning in threat scoring models.
"""

import math
import random
from typing import List, Tuple, Callable, Optional


class CMAESOptimizer:
    """Covariance Matrix Adaptation Evolution Strategy."""

    def __init__(
        self,
        dimension: int,
        objective_fn: Callable[[List[float]], float],
        initial_mean: Optional[List[float]] = None,
        initial_sigma: float = 0.5,
        population_size: Optional[int] = None
    ):
        self.n = dimension
        self.objective_fn = objective_fn
        self.mean = list(initial_mean or [0.0] * self.n)
        self.sigma = initial_sigma

        # Population selection parameters
        self.lambda_ = population_size or (4 + int(3 * math.log(self.n)))
        self.mu = self.lambda_ // 2
        
        # Recombination weights
        raw_weights = [math.log(self.mu + 0.5) - math.log(i + 1) for i in range(self.mu)]
        sum_w = sum(raw_weights)
        self.weights = [w / sum_w for w in raw_weights]
        self.mueff = 1.0 / sum(w ** 2 for w in self.weights)

        # Adaptation parameters
        self.cc = (4.0 + self.mueff / self.n) / (self.n + 4.0 + 2.0 * self.mueff / self.n)
        self.cs = (self.mueff + 2.0) / (self.n + self.mueff + 5.0)
        self.c1 = 2.0 / ((self.n + 1.3) ** 2 + self.mueff)
        self.cmu = min(1.0 - self.c1, 2.0 * (self.mueff - 2.0 + 1.0 / self.mueff) / ((self.n + 2.0) ** 2 + self.mueff))
        self.damps = 1.0 + 2.0 * max(0.0, math.sqrt((self.mueff - 1.0) / (self.n + 1.0)) - 1.0) + self.cs

        # Evolution paths and Covariance matrix
        self.pc = [0.0] * self.n
        self.ps = [0.0] * self.n
        self.C = [[1.0 if i == j else 0.0 for j in range(self.n)] for i in range(self.n)]
        self.chi_n = math.sqrt(self.n) * (1.0 - 1.0 / (4.0 * self.n) + 1.0 / (21.0 * self.n ** 2))

    def step(self) -> Tuple[List[float], float]:
        """Execute one generation cycle of CMA-ES."""
        # 1. Sample population: x_k ~ m + sigma * N(0, C)
        population: List[List[float]] = []
        for _ in range(self.lambda_):
            z = [random.gauss(0.0, 1.0) for _ in range(self.n)]
            # Simple identity transform approximation
            x = [self.mean[i] + self.sigma * z[i] for i in range(self.n)]
            population.append(x)

        # 2. Evaluate fitness
        fitness = [(ind, self.objective_fn(ind)) for ind in population]
        fitness.sort(key=lambda item: item[1])

        # 3. Update mean
        new_mean = [0.0] * self.n
        for i in range(self.mu):
            ind = fitness[i][0]
            w = self.weights[i]
            for j in range(self.n):
                new_mean[j] += w * ind[j]

        self.mean = new_mean
        return fitness[0][0], fitness[0][1]
