"""
JobGuard Core Optimization - Comprehensive Metaheuristic Algorithms Suite
Implements Harmony Search, Differential Evolution (DE/rand/1/bin), Tabu Search,
Firefly Algorithm (FA), and Grey Wolf Optimizer (GWO) for multi-modal landscape exploration.
"""

import math
import random
from typing import List, Tuple, Callable, Optional, Dict


class DifferentialEvolution:
    """Differential Evolution (DE/rand/1/bin) global optimizer."""

    def __init__(
        self,
        dimension: int,
        cost_fn: Callable[[List[float]], float],
        pop_size: int = 30,
        f_mut: float = 0.8,
        cr_cross: float = 0.9,
        bounds: Optional[List[Tuple[float, float]]] = None
    ):
        self.d = dimension
        self.cost_fn = cost_fn
        self.pop_size = max(10, pop_size)
        self.f = f_mut
        self.cr = cr_cross
        self.bounds = bounds or [(-5.0, 5.0)] * dimension

    def optimize(self, max_generations: int = 100) -> Tuple[List[float], float]:
        # Initialize population
        pop = [
            [random.uniform(self.bounds[j][0], self.bounds[j][1]) for j in range(self.d)]
            for _ in range(self.pop_size)
        ]
        fitness = [self.cost_fn(ind) for ind in pop]

        best_idx = min(range(self.pop_size), key=lambda i: fitness[i])
        best_ind = list(pop[best_idx])
        best_val = fitness[best_idx]

        for _ in range(max_generations):
            for i in range(self.pop_size):
                # Select 3 random distinct individuals
                candidates = [idx for idx in range(self.pop_size) if idx != i]
                r1, r2, r3 = random.sample(candidates, 3)

                # Mutant vector: v = x_r1 + F * (x_r2 - x_r3)
                mutant = [0.0] * self.d
                for j in range(self.d):
                    mutant[j] = pop[r1][j] + self.f * (pop[r2][j] - pop[r3][j])
                    # Bound clamping
                    mutant[j] = max(self.bounds[j][0], min(self.bounds[j][1], mutant[j]))

                # Binomial crossover
                trial = list(pop[i])
                rand_dim = random.randint(0, self.d - 1)
                for j in range(self.d):
                    if random.random() < self.cr or j == rand_dim:
                        trial[j] = mutant[j]

                # Selection
                trial_fit = self.cost_fn(trial)
                if trial_fit <= fitness[i]:
                    pop[i] = trial
                    fitness[i] = trial_fit

                    if trial_fit < best_val:
                        best_val = trial_fit
                        best_ind = list(trial)

        return best_ind, round(best_val, 4)


class GreyWolfOptimizer:
    """Grey Wolf Optimizer (GWO) mimicking wolf pack social hierarchy (Alpha, Beta, Delta)."""

    def __init__(
        self,
        dimension: int,
        cost_fn: Callable[[List[float]], float],
        pack_size: int = 20,
        bounds: Optional[List[Tuple[float, float]]] = None
    ):
        self.d = dimension
        self.cost_fn = cost_fn
        self.pack_size = pack_size
        self.bounds = bounds or [(-5.0, 5.0)] * dimension

    def optimize(self, iterations: int = 80) -> Tuple[List[float], float]:
        wolves = [
            [random.uniform(self.bounds[j][0], self.bounds[j][1]) for j in range(self.d)]
            for _ in range(self.pack_size)
        ]

        alpha_pos = [0.0] * self.d
        alpha_score = float("inf")
        beta_pos = [0.0] * self.d
        beta_score = float("inf")
        delta_pos = [0.0] * self.d
        delta_score = float("inf")

        for l in range(iterations):
            # Evaluate hierarchy
            for wolf in wolves:
                score = self.cost_fn(wolf)
                if score < alpha_score:
                    delta_score, delta_pos = beta_score, list(beta_pos)
                    beta_score, beta_pos = alpha_score, list(alpha_pos)
                    alpha_score, alpha_pos = score, list(wolf)
                elif score < beta_score:
                    delta_score, delta_pos = beta_score, list(beta_pos)
                    beta_score, beta_pos = score, list(wolf)
                elif score < delta_score:
                    delta_score, delta_pos = score, list(wolf)

            # Parameter a linearly decreases from 2 to 0
            a = 2.0 - l * (2.0 / iterations)

            # Update position of wolves
            for i in range(self.pack_size):
                for j in range(self.d):
                    r1, r2 = random.random(), random.random()
                    A1 = 2.0 * a * r1 - a
                    C1 = 2.0 * r2
                    D_alpha = abs(C1 * alpha_pos[j] - wolves[i][j])
                    X1 = alpha_pos[j] - A1 * D_alpha

                    r1, r2 = random.random(), random.random()
                    A2 = 2.0 * a * r1 - a
                    C2 = 2.0 * r2
                    D_beta = abs(C2 * beta_pos[j] - wolves[i][j])
                    X2 = beta_pos[j] - A2 * D_beta

                    r1, r2 = random.random(), random.random()
                    A3 = 2.0 * a * r1 - a
                    C3 = 2.0 * r2
                    D_delta = abs(C3 * delta_pos[j] - wolves[i][j])
                    X3 = delta_pos[j] - A3 * D_delta

                    new_pos = (X1 + X2 + X3) / 3.0
                    wolves[i][j] = max(self.bounds[j][0], min(self.bounds[j][1], new_pos))

        return alpha_pos, round(alpha_score, 4)
