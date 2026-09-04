"""
Aetheris Optimization: Standard Benchmark Test Suites
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
from typing import List, Tuple, Sequence


class OptimizationBenchmarks:
    """Standard global and multi-objective optimization mathematical test functions."""

    @staticmethod
    def sphere(x: Sequence[float]) -> float:
        """f(x) = sum(x_i^2)"""
        return sum(v * v for v in x)

    @staticmethod
    def rosenbrock(x: Sequence[float]) -> float:
        """f(x) = sum(100*(x_{i+1} - x_i^2)^2 + (1 - x_i)^2)"""
        val = 0.0
        for i in range(len(x) - 1):
            val += 100.0 * (x[i + 1] - x[i] ** 2) ** 2 + (1.0 - x[i]) ** 2
        return val

    @staticmethod
    def rastrigin(x: Sequence[float]) -> float:
        """f(x) = 10*d + sum(x_i^2 - 10*cos(2*pi*x_i))"""
        d = len(x)
        return 10.0 * d + sum(v * v - 10.0 * math.cos(2.0 * math.pi * v) for v in x)

    @staticmethod
    def ackley(x: Sequence[float]) -> float:
        """f(x) = -20*exp(-0.2*sqrt(sum(x^2)/d)) - exp(sum(cos(2*pi*x))/d) + 20 + e"""
        d = float(len(x))
        if d == 0:
            return 0.0
        sum_sq = sum(v * v for v in x)
        sum_cos = sum(math.cos(2.0 * math.pi * v) for v in x)
        term1 = -20.0 * math.exp(-0.2 * math.sqrt(sum_sq / d))
        term2 = -math.exp(sum_cos / d)
        return term1 + term2 + 20.0 + math.e

    @staticmethod
    def zdt1_multiobjective(x: Sequence[float]) -> List[float]:
        """
        Zitzler-Deb-Thiele test problem 1 (ZDT1):
        f1(x) = x_0
        g(x) = 1 + 9 * sum_{i=1}^n x_i / (n - 1)
        f2(x) = g(x) * (1 - sqrt(f1 / g(x)))
        """
        f1 = max(0.0, min(1.0, x[0]))
        n = len(x)
        if n > 1:
            g = 1.0 + 9.0 * sum(max(0.0, min(1.0, v)) for v in x[1:]) / float(n - 1)
        else:
            g = 1.0
        f2 = g * (1.0 - math.sqrt(f1 / g))
        return [f1, f2]
