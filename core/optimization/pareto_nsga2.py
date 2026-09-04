"""
Aetheris Optimization & Neural-Symbolic: Non-dominated Sorting Genetic Algorithm II (NSGA-II)
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
import random
from typing import List, Tuple, Sequence, Optional, Callable, Dict, Any


class Individual:
    """Multi-Objective Genetic Solution Candidate."""
    __slots__ = ('genes', 'objectives', 'rank', 'crowding_distance', 'dominated_solutions', 'domination_count')

    def __init__(self, genes: Sequence[float]) -> None:
        self.genes: List[float] = [float(g) for g in genes]
        self.objectives: List[float] = [] # Minimization target values
        self.rank: int = 0
        self.crowding_distance: float = 0.0
        self.dominated_solutions: List[Individual] = []
        self.domination_count: int = 0

    def dominates(self, other: Individual) -> bool:
        """Pareto Domination check (minimizing all objectives)."""
        at_least_one_better = False
        for obj_a, obj_b in zip(self.objectives, other.objectives):
            if obj_a > obj_b:
                return False
            elif obj_a < obj_b:
                at_least_one_better = True
        return at_least_one_better


class NSGA2Optimizer:
    """
    Non-Dominated Sorting Genetic Algorithm II (NSGA-II).
    Features:
    - Fast non-dominated sorting into Pareto fronts (F1, F2, ...).
    - Crowding distance assignment for optimal diversity preservation.
    - Simulated Binary Crossover (SBX) and Polynomial Mutation.
    - Elitist environmental selection.
    """
    def __init__(
        self,
        population_size: int = 60,
        num_variables: int = 4,
        bounds_min: Sequence[float] = (-5.0, -5.0, -5.0, -5.0),
        bounds_max: Sequence[float] = (5.0, 5.0, 5.0, 5.0),
        crossover_rate: float = 0.9,
        mutation_rate: float = 0.1,
        eta_c: float = 20.0,
        eta_m: float = 20.0,
        seed: Optional[int] = None
    ) -> None:
        self.pop_size = population_size
        self.num_vars = num_variables
        self.bounds_min = list(bounds_min)
        self.bounds_max = list(bounds_max)
        self.cr = crossover_rate
        self.mr = mutation_rate
        self.eta_c = eta_c
        self.eta_m = eta_m
        self.rng = random.Random(seed)

        self.population: List[Individual] = []
        self._init_population()

    def _init_population(self) -> None:
        self.population.clear()
        for _ in range(self.pop_size):
            genes = [
                self.rng.uniform(self.bounds_min[i], self.bounds_max[i])
                for i in range(self.num_vars)
            ]
            self.population.append(Individual(genes))

    def evaluate_population(self, obj_func: Callable[[List[float]], List[float]]) -> None:
        for ind in self.population:
            if not ind.objectives:
                ind.objectives = obj_func(ind.genes)

    def fast_non_dominated_sort(self, population: List[Individual]) -> List[List[Individual]]:
        """Sorts population into hierarchical Pareto fronts."""
        fronts: List[List[Individual]] = [[]]

        for p in population:
            p.dominated_solutions.clear()
            p.domination_count = 0
            for q in population:
                if p.dominates(q):
                    p.dominated_solutions.append(q)
                elif q.dominates(p):
                    p.domination_count += 1

            if p.domination_count == 0:
                p.rank = 1
                fronts[0].append(p)

        i = 0
        while len(fronts[i]) > 0:
            next_front: List[Individual] = []
            for p in fronts[i]:
                for q in p.dominated_solutions:
                    q.domination_count -= 1
                    if q.domination_count == 0:
                        q.rank = i + 2
                        next_front.append(q)
            i += 1
            fronts.append(next_front)

        if not fronts[-1]:
            fronts.pop()
        return fronts

    def calculate_crowding_distance(self, front: List[Individual]) -> None:
        n = len(front)
        if n == 0:
            return
        if n <= 2:
            for ind in front:
                ind.crowding_distance = float('inf')
            return

        for ind in front:
            ind.crowding_distance = 0.0

        num_objectives = len(front[0].objectives)

        for m in range(num_objectives):
            front.sort(key=lambda ind: ind.objectives[m])
            front[0].crowding_distance = float('inf')
            front[-1].crowding_distance = float('inf')

            obj_min = front[0].objectives[m]
            obj_max = front[-1].objectives[m]
            span = obj_max - obj_min
            if span < 1e-12:
                continue

            for i in range(1, n - 1):
                if front[i].crowding_distance != float('inf'):
                    dist = (front[i + 1].objectives[m] - front[i - 1].objectives[m]) / span
                    front[i].crowding_distance += dist

    def _tournament_selection(self) -> Individual:
        p1 = self.rng.choice(self.population)
        p2 = self.rng.choice(self.population)

        if p1.rank < p2.rank:
            return p1
        elif p2.rank < p1.rank:
            return p2
        elif p1.crowding_distance > p2.crowding_distance:
            return p1
        return p2

    def _sbx_crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        c1_genes = list(parent1.genes)
        c2_genes = list(parent2.genes)

        if self.rng.random() < self.cr:
            for i in range(self.num_vars):
                if self.rng.random() <= 0.5:
                    y1 = min(parent1.genes[i], parent2.genes[i])
                    y2 = max(parent1.genes[i], parent2.genes[i])
                    
                    if abs(y1 - y2) > 1e-9:
                        rand = self.rng.random()
                        beta = 1.0 + (2.0 * (y1 - self.bounds_min[i]) / (y2 - y1))
                        alpha = 2.0 - (beta ** -(self.eta_c + 1.0))
                        betaq = (rand * alpha) ** (1.0 / (self.eta_c + 1.0)) if rand <= (1.0 / alpha) else (1.0 / (2.0 - rand * alpha)) ** (1.0 / (self.eta_c + 1.0))
                        
                        c1 = 0.5 * ((y1 + y2) - betaq * (y2 - y1))
                        c2 = 0.5 * ((y1 + y2) + betaq * (y2 - y1))
                        
                        c1_genes[i] = max(self.bounds_min[i], min(self.bounds_max[i], c1))
                        c2_genes[i] = max(self.bounds_min[i], min(self.bounds_max[i], c2))

        return Individual(c1_genes), Individual(c2_genes)

    def _polynomial_mutation(self, ind: Individual) -> None:
        for i in range(self.num_vars):
            if self.rng.random() < self.mr:
                y = ind.genes[i]
                yl = self.bounds_min[i]
                yu = self.bounds_max[i]
                delta1 = (y - yl) / (yu - yl) if (yu - yl) > 1e-9 else 0.0
                delta2 = (yu - y) / (yu - yl) if (yu - yl) > 1e-9 else 0.0
                rand = self.rng.random()
                mut_pow = 1.0 / (self.eta_m + 1.0)
                
                if rand <= 0.5:
                    xy = 1.0 - delta1
                    val = 2.0 * rand + (1.0 - 2.0 * rand) * (xy ** (self.eta_m + 1.0))
                    deltaq = (val ** mut_pow) - 1.0
                else:
                    xy = 1.0 - delta2
                    val = 2.0 * (1.0 - rand) + 2.0 * (rand - 0.5) * (xy ** (self.eta_m + 1.0))
                    deltaq = 1.0 - (val ** mut_pow)
                    
                y = y + deltaq * (yu - yl)
                ind.genes[i] = max(yl, min(yu, y))

    def step_generation(self, obj_func: Callable[[List[float]], List[float]]) -> List[Individual]:
        """Runs 1 generation of NSGA-II evolution."""
        self.evaluate_population(obj_func)
        
        # Create offspring
        offspring: List[Individual] = []
        while len(offspring) < self.pop_size:
            p1 = self._tournament_selection()
            p2 = self._tournament_selection()
            c1, c2 = self._sbx_crossover(p1, p2)
            self._polynomial_mutation(c1)
            self._polynomial_mutation(c2)
            c1.objectives = obj_func(c1.genes)
            c2.objectives = obj_func(c2.genes)
            offspring.append(c1)
            if len(offspring) < self.pop_size:
                offspring.append(c2)

        # Combine R_t = P_t U Q_t (size 2N)
        combined = self.population + offspring
        fronts = self.fast_non_dominated_sort(combined)

        new_population: List[Individual] = []
        for front in fronts:
            self.calculate_crowding_distance(front)
            if len(new_population) + len(front) <= self.pop_size:
                new_population.extend(front)
            else:
                # Sort by crowding distance descending and pick remaining
                front.sort(key=lambda ind: ind.crowding_distance, reverse=True)
                remaining = self.pop_size - len(new_population)
                new_population.extend(front[:remaining])
                break

        self.population = new_population
        return self.get_pareto_front()

    def get_pareto_front(self) -> List[Individual]:
        fronts = self.fast_non_dominated_sort(self.population)
        return fronts[0] if fronts else []
