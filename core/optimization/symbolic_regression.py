"""
Aetheris Optimization & Neural-Symbolic: Symbolic Regression & Mathematical Discovery
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
import random
from typing import List, Dict, Any, Tuple, Sequence, Optional
from core.optimization.ast_genetic_trees import (
    ASTNode, ConstantNode, VariableNode, BinaryOpNode, UnaryOpNode, TreeGenerator
)


class SymbolicProgram:
    """Individual Program in Symbolic Genetic Population."""
    __slots__ = ('root', 'fitness', 'mse_loss', 'complexity_penalty')

    def __init__(self, root: ASTNode) -> None:
        self.root = root
        self.fitness: float = float('inf')
        self.mse_loss: float = float('inf')
        self.complexity_penalty: float = 0.0


class SymbolicRegressionEngine:
    """
    Symbolic Regression Genetic Programming Engine.
    Discovers analytical mathematical laws, governing physics differential equations,
    and non-linear models from tabular experimental data.
    """
    def __init__(
        self,
        variable_names: List[str],
        population_size: int = 100,
        max_tree_depth: int = 5,
        parsimony_coefficient: float = 0.001,
        crossover_prob: float = 0.7,
        mutation_prob: float = 0.25,
        tournament_size: int = 5,
        seed: Optional[int] = None
    ) -> None:
        self.var_names = list(variable_names)
        self.pop_size = population_size
        self.max_depth = max_tree_depth
        self.parsimony = parsimony_coefficient
        self.p_cross = crossover_prob
        self.p_mut = mutation_prob
        self.t_size = tournament_size
        self.rng = random.Random(seed)

        self.population: List[SymbolicProgram] = []
        self._init_population()

    def _init_population(self) -> None:
        self.population.clear()
        for i in range(self.pop_size):
            method = "grow" if i % 2 == 0 else "full"
            depth = self.rng.randint(2, self.max_depth)
            tree = TreeGenerator.generate_random_tree(self.var_names, depth, method, self.rng)
            self.population.append(SymbolicProgram(tree))

    def evaluate_fitness(self, X: List[Dict[str, float]], y_true: List[float]) -> None:
        n = len(y_true)
        if n == 0:
            return

        for prog in self.population:
            total_sq_err = 0.0
            for i in range(n):
                y_pred = prog.root.evaluate(X[i])
                diff = y_pred - y_true[i]
                if math.isnan(diff) or math.isinf(diff):
                    total_sq_err += 1e6
                else:
                    total_sq_err += min(1e6, diff * diff)

            mse = total_sq_err / float(n)
            num_nodes = len(prog.root.get_all_nodes())
            penalty = self.parsimony * num_nodes

            prog.mse_loss = mse
            prog.complexity_penalty = penalty
            prog.fitness = mse + penalty

    def _tournament(self) -> SymbolicProgram:
        candidates = [self.rng.choice(self.population) for _ in range(self.t_size)]
        candidates.sort(key=lambda p: p.fitness)
        return candidates[0]

    def _crossover(self, parent1: SymbolicProgram, parent2: SymbolicProgram) -> SymbolicProgram:
        t1 = parent1.root.clone()
        t2 = parent2.root.clone()

        nodes1 = t1.get_all_nodes()
        nodes2 = t2.get_all_nodes()

        # Swap random subtrees
        target1 = self.rng.choice(nodes1)
        source2 = self.rng.choice(nodes2).clone()

        # If root
        if target1 is t1:
            return SymbolicProgram(source2)

        # Find parent of target1 in t1 and replace
        for node in nodes1:
            if hasattr(node, 'children'):
                children = getattr(node, 'children')
                for idx, child in enumerate(children):
                    if child is target1:
                        children[idx] = source2
                        return SymbolicProgram(t1)

        return SymbolicProgram(t1)

    def _mutate(self, parent: SymbolicProgram) -> SymbolicProgram:
        t = parent.root.clone()
        nodes = t.get_all_nodes()
        target = self.rng.choice(nodes)
        
        # Replace target with new random subtree
        new_sub = TreeGenerator.generate_random_tree(self.var_names, max_depth=3, rng=self.rng)
        
        if target is t:
            return SymbolicProgram(new_sub)

        for node in nodes:
            if hasattr(node, 'children'):
                children = getattr(node, 'children')
                for idx, child in enumerate(children):
                    if child is target:
                        children[idx] = new_sub
                        return SymbolicProgram(t)

        return SymbolicProgram(t)

    def step_generation(self, X: List[Dict[str, float]], y_true: List[float]) -> SymbolicProgram:
        self.evaluate_fitness(X, y_true)
        self.population.sort(key=lambda p: p.fitness)
        best_prog = self.population[0]

        # Elitism: retain top 5%
        elite_count = max(2, int(self.pop_size * 0.05))
        new_pop: List[SymbolicProgram] = [SymbolicProgram(p.root.clone()) for p in self.population[:elite_count]]

        while len(new_pop) < self.pop_size:
            r = self.rng.random()
            if r < self.p_cross:
                p1 = self._tournament()
                p2 = self._tournament()
                child = self._crossover(p1, p2)
            elif r < self.p_cross + self.p_mut:
                p = self._tournament()
                child = self._mutate(p)
            else:
                p = self._tournament()
                child = SymbolicProgram(p.root.clone())

            if child.root.depth() <= self.max_depth + 2:
                new_pop.append(child)

        self.population = new_pop
        return best_prog
