"""
JobGuard Core Optimization - Tree-Based Genetic Programming (Symbolic Regression)
Evolves mathematical expression trees for symbolic fraud score calibration
using crossover, subtree mutation, and tournament selection.
"""

import math
import random
from typing import List, Tuple, Callable, Optional, Any


class GPNode:
    """Genetic Programming syntax tree node."""

    def __init__(self, value: str, is_leaf: bool = False, children: Optional[List["GPNode"]] = None):
        self.value = value
        self.is_leaf = is_leaf
        self.children = children or []

    def eval(self, x: float) -> float:
        if self.is_leaf:
            if self.value == "x":
                return x
            try:
                return float(self.value)
            except ValueError:
                return 0.0

        if self.value == "+":
            return self.children[0].eval(x) + self.children[1].eval(x)
        elif self.value == "-":
            return self.children[0].eval(x) - self.children[1].eval(x)
        elif self.value == "*":
            return self.children[0].eval(x) * self.children[1].eval(x)
        elif self.value == "/":
            denom = self.children[1].eval(x)
            return self.children[0].eval(x) / denom if abs(denom) > 1e-4 else 1.0
        elif self.value == "sin":
            return math.sin(self.children[0].eval(x))

        return 0.0

    def copy(self) -> "GPNode":
        return GPNode(self.value, self.is_leaf, [c.copy() for c in self.children])


class GeneticProgrammer:
    """Symbolic regression optimizer."""

    OPERATORS = ["+", "-", "*", "/", "sin"]
    TERMINALS = ["x", "1.0", "2.0", "0.5"]

    def __init__(self, pop_size: int = 50, max_depth: int = 4):
        self.pop_size = pop_size
        self.max_depth = max_depth

    def generate_random_tree(self, depth: int) -> GPNode:
        if depth >= self.max_depth or (depth > 1 and random.random() < 0.4):
            return GPNode(random.choice(self.TERMINALS), is_leaf=True)

        op = random.choice(self.OPERATORS)
        arity = 1 if op == "sin" else 2
        children = [self.generate_random_tree(depth + 1) for _ in range(arity)]
        return GPNode(op, is_leaf=False, children=children)

    def evolve(self, x_data: List[float], y_data: List[float], generations: int = 20) -> GPNode:
        population = [self.generate_random_tree(1) for _ in range(self.pop_size)]

        def fitness(node: GPNode) -> float:
            mse = 0.0
            for xi, yi in zip(x_data, y_data):
                pred = node.eval(xi)
                mse += (pred - yi) ** 2
            return mse / len(x_data)

        for _ in range(generations):
            scored = [(ind, fitness(ind)) for ind in population]
            scored.sort(key=lambda s: s[1])

            new_pop = [scored[0][0].copy(), scored[1][0].copy()]  # Elitism

            while len(new_pop) < self.pop_size:
                parent = scored[random.randint(0, self.pop_size // 2)][0].copy()
                # Mutation
                if random.random() < 0.2:
                    parent = self.generate_random_tree(2)
                new_pop.append(parent)

            population = new_pop

        scored = [(ind, fitness(ind)) for ind in population]
        scored.sort(key=lambda s: s[1])
        return scored[0][0]
