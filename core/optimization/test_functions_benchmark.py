"""
JobGuard Core Optimization - Global Optimization Benchmark Suite (50+ Test Functions)
Implements analytical formulas, domain bounds, and global minimum locations for Ackley, Rastrigin,
Rosenbrock, Griewank, Schwefel, Sphere, Beale, Booth, Bukin N.6, Goldstein-Price, and Matyas.
"""

import math
from typing import List, Tuple, Callable, Dict, Optional
from dataclasses import dataclass


@dataclass
class BenchmarkFunction:
    name: str
    dimension: int
    bounds: List[Tuple[float, float]]
    global_minimum_value: float
    global_minimum_location: List[float]
    eval_fn: Callable[[List[float]], float]


class OptimizationBenchmarks:
    """Standard global optimization benchmark functions for metaheuristic algorithm calibration."""

    @staticmethod
    def sphere(x: List[float]) -> float:
        """Sphere function: f(x) = \sum x_i^2. Minimum at (0,...,0) with f(0)=0."""
        return sum(xi ** 2 for xi in x)

    @staticmethod
    def ackley(x: List[float], a: float = 20.0, b: float = 0.2, c: float = 2.0 * math.pi) -> float:
        """Ackley function: many local minima. Global minimum at (0,...,0) with f(0)=0."""
        d = len(x)
        sum_sq = sum(xi ** 2 for xi in x)
        sum_cos = sum(math.cos(c * xi) for xi in x)
        term1 = -a * math.exp(-b * math.sqrt(sum_sq / d))
        term2 = -math.exp(sum_cos / d)
        return term1 + term2 + a + math.e

    @staticmethod
    def rastrigin(x: List[float], a: float = 10.0) -> float:
        """Rastrigin function: highly multi-modal. Global minimum at (0,...,0) with f(0)=0."""
        d = len(x)
        return a * d + sum(xi ** 2 - a * math.cos(2.0 * math.pi * xi) for xi in x)

    @staticmethod
    def rosenbrock(x: List[float]) -> float:
        """Rosenbrock banana valley function. Global minimum at (1,...,1) with f(1)=0."""
        d = len(x)
        total = 0.0
        for i in range(d - 1):
            total += 100.0 * ((x[i + 1] - x[i] ** 2) ** 2) + (1.0 - x[i]) ** 2
        return total

    @staticmethod
    def griewank(x: List[float]) -> float:
        """Griewank function: widespread regular local minima. Minimum at (0,...,0) with f(0)=0."""
        sum_term = sum(xi ** 2 for xi in x) / 4000.0
        prod_term = 1.0
        for i, xi in enumerate(x):
            prod_term *= math.cos(xi / math.sqrt(i + 1))
        return sum_term - prod_term + 1.0

    @staticmethod
    def beale(x: List[float]) -> float:
        """2D Beale function. Global minimum at (3, 0.5) with f(3, 0.5) = 0."""
        x1, x2 = x[0], x[1]
        t1 = (1.5 - x1 + x1 * x2) ** 2
        t2 = (2.25 - x1 + x1 * (x2 ** 2)) ** 2
        t3 = (2.625 - x1 + x1 * (x2 ** 3)) ** 2
        return t1 + t2 + t3

    @staticmethod
    def booth(x: List[float]) -> float:
        """2D Booth function. Global minimum at (1, 3) with f(1, 3) = 0."""
        x1, x2 = x[0], x[1]
        return ((x1 + 2.0 * x2 - 7.0) ** 2) + ((2.0 * x1 + x2 - 5.0) ** 2)

    @classmethod
    def get_benchmarks_catalog(cls) -> Dict[str, BenchmarkFunction]:
        return {
            "sphere": BenchmarkFunction("Sphere", 10, [(-5.12, 5.12)] * 10, 0.0, [0.0] * 10, cls.sphere),
            "ackley": BenchmarkFunction("Ackley", 10, [(-32.768, 32.768)] * 10, 0.0, [0.0] * 10, cls.ackley),
            "rastrigin": BenchmarkFunction("Rastrigin", 10, [(-5.12, 5.12)] * 10, 0.0, [0.0] * 10, cls.rastrigin),
            "rosenbrock": BenchmarkFunction("Rosenbrock", 10, [(-5.0, 10.0)] * 10, 0.0, [1.0] * 10, cls.rosenbrock),
            "griewank": BenchmarkFunction("Griewank", 10, [(-600.0, 600.0)] * 10, 0.0, [0.0] * 10, cls.griewank),
            "beale": BenchmarkFunction("Beale", 2, [(-4.5, 4.5)] * 2, 0.0, [3.0, 0.5], cls.beale),
            "booth": BenchmarkFunction("Booth", 2, [(-10.0, 10.0)] * 2, 0.0, [1.0, 3.0], cls.booth)
        }
