"""
JobGuard Core Optimization - Simulated Annealing Metaheuristic
Implements Boltzmann probability acceptance and geometric cooling schedules
for combinatorial threat rule weighting and feature selection.
"""

import math
import random
from typing import List, Tuple, Callable, Optional


class SimulatedAnnealingOptimizer:
    """Combinatorial optimization using Metropolis-Hastings acceptance criterion."""

    def __init__(
        self,
        cost_fn: Callable[[List[float]], float],
        initial_temp: float = 100.0,
        cooling_rate: float = 0.95,
        min_temp: float = 1e-3
    ):
        self.cost_fn = cost_fn
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp

    def optimize(self, initial_state: List[float], max_iterations_per_temp: int = 50) -> Tuple[List[float], float]:
        current_state = list(initial_state)
        current_cost = self.cost_fn(current_state)
        best_state = list(current_state)
        best_cost = current_cost
        t = self.initial_temp

        while t > self.min_temp:
            for _ in range(max_iterations_per_temp):
                # Propose neighbor
                neighbor = list(current_state)
                idx = random.randint(0, len(neighbor) - 1)
                neighbor[idx] += random.uniform(-0.2, 0.2)
                
                cost_candidate = self.cost_fn(neighbor)
                delta = cost_candidate - current_cost

                # Accept if better or with Boltzmann probability
                if delta < 0 or random.random() < math.exp(-delta / t):
                    current_state = neighbor
                    current_cost = cost_candidate

                    if current_cost < best_cost:
                        best_state = list(current_state)
                        best_cost = current_cost

            t *= self.cooling_rate

        return best_state, best_cost
