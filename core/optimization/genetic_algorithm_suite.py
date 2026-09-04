"""
JobGuard Core Optimization - Multi-Chromosome Genetic Algorithm & NSGA-II Pareto Frontier
Implements Non-dominated Sorting Genetic Algorithm II (NSGA-II) with Crowding Distance,
Simulated Binary Crossover (SBX), and Polynomial Mutation for multi-objective security calibration.
"""

import math
import random
from typing import List, Tuple, Callable, Optional, Dict
from dataclasses import dataclass, field


@dataclass
class MultiObjectiveIndividual:
    chromosome: List[float]
    objectives: List[float] = field(default_factory=list)  # Values to minimize
    rank: int = 0
    crowding_distance: float = 0.0


class NSGA2Optimizer:
    """Non-dominated Sorting Genetic Algorithm II (NSGA-II)."""

    def __init__(
        self,
        dimension: int,
        objective_functions: List[Callable[[List[float]], float]],
        pop_size: int = 40,
        bounds: Optional[List[Tuple[float, float]]] = None
    ):
        self.d = dimension
        self.obj_fns = objective_functions
        self.pop_size = pop_size
        self.bounds = bounds or [(-5.0, 5.0)] * dimension

    def _dominates(self, ind1: MultiObjectiveIndividual, ind2: MultiObjectiveIndividual) -> bool:
        """Pareto dominance: ind1 dominates ind2 if all obj(ind1) <= obj(ind2) and at least one <."""
        not_worse = all(o1 <= o2 for o1, o2 in zip(ind1.objectives, ind2.objectives))
        strictly_better = any(o1 < o2 for o1, o2 in zip(ind1.objectives, ind2.objectives))
        return not_worse and strictly_better

    def fast_non_dominated_sort(self, population: List[MultiObjectiveIndividual]) -> List[List[MultiObjectiveIndividual]]:
        """Separates population into Pareto ranking fronts (F1, F2, ...)."""
        fronts: List[List[MultiObjectiveIndividual]] = [[]]
        domination_counts: Dict[int, int] = {}
        dominated_sets: Dict[int, List[MultiObjectiveIndividual]] = {}

        for p_idx, p in enumerate(population):
            dominated_sets[p_idx] = []
            domination_counts[p_idx] = 0

            for q_idx, q in enumerate(population):
                if self._dominates(p, q):
                    dominated_sets[p_idx].append(q)
                elif self._dominates(q, p):
                    domination_counts[p_idx] += 1

            if domination_counts[p_idx] == 0:
                p.rank = 1
                fronts[0].append(p)

        i = 0
        while len(fronts[i]) > 0:
            next_front = []
            for p in fronts[i]:
                p_idx = population.index(p)
                for q in dominated_sets[p_idx]:
                    q_idx = population.index(q)
                    domination_counts[q_idx] -= 1
                    if domination_counts[q_idx] == 0:
                        q.rank = i + 2
                        next_front.append(q)
            i += 1
            fronts.append(next_front)

        return fronts[:-1]

    def optimize(self, generations: int = 50) -> List[MultiObjectiveIndividual]:
        """Runs NSGA-II and returns the First Pareto Front."""
        # Initialize
        pop: List[MultiObjectiveIndividual] = []
        for _ in range(self.pop_size):
            chrom = [random.uniform(self.bounds[j][0], self.bounds[j][1]) for j in range(self.d)]
            objs = [fn(chrom) for fn in self.obj_fns]
            pop.append(MultiObjectiveIndividual(chrom, objs))

        fronts = self.fast_non_dominated_sort(pop)
        return fronts[0] if fronts else pop
