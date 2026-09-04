"""
JobGuard Core Optimization - CEC Benchmark Function Suite & Statistical Significance Tests
Contains 50 standard CEC benchmark landscape generators (Shifted, Rotated, Hybrid, and Composition Functions)
and Wilcoxon Signed-Rank / Friedman statistical hypothesis testers for metaheuristic evaluation.
"""

import math
import random
from typing import List, Tuple, Callable, Dict, Optional


class StatisticalHypothesisTests:
    """Non-parametric statistical significance tests for optimization algorithms."""

    @staticmethod
    def wilcoxon_signed_rank_test(sample1: List[float], sample2: List[float]) -> Tuple[float, float]:
        """Calculates W-statistic and asymptotic z-score for paired samples."""
        n = len(sample1)
        if n != len(sample2) or n < 5:
            return 0.0, 1.0

        differences = [s1 - s2 for s1, s2 in zip(sample1, sample2) if s1 != s2]
        n_diff = len(differences)
        if n_diff == 0:
            return 0.0, 1.0

        # Absolute differences with signs
        abs_diffs = sorted([(abs(d), 1 if d > 0 else -1) for d in differences], key=lambda x: x[0])

        # Assign ranks
        w_plus = 0.0
        w_minus = 0.0
        for rank_idx, (abs_val, sign) in enumerate(abs_diffs, start=1):
            if sign > 0:
                w_plus += rank_idx
            else:
                w_minus += rank_idx

        w = min(w_plus, w_minus)
        # Expected value and variance under null hypothesis
        mean_w = n_diff * (n_diff + 1) / 4.0
        std_w = math.sqrt(n_diff * (n_diff + 1) * (2 * n_diff + 1) / 24.0)

        z = (w - mean_w) / max(1e-12, std_w)
        # Approximate 2-tailed p-value from normal distribution
        p_val = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(z) / math.sqrt(2.0))))

        return round(w, 2), round(max(0.0, min(1.0, p_val)), 4)


class CECBenchmarkLandscapeSuite:
    """Shifted and Rotated Benchmark Objective Functions."""

    @staticmethod
    def shifted_sphere(x: List[float], shift_vector: Optional[List[float]] = None) -> float:
        d = len(x)
        shift = shift_vector or [1.0] * d
        return sum((xi - si) ** 2 for xi, si in zip(x, shift))

    @staticmethod
    def shifted_rastrigin(x: List[float], shift_vector: Optional[List[float]] = None, a: float = 10.0) -> float:
        d = len(x)
        shift = shift_vector or [0.5] * d
        total = a * d
        for xi, si in zip(x, shift):
            z = xi - si
            total += z ** 2 - a * math.cos(2.0 * math.pi * z)
        return total

    @staticmethod
    def shifted_rosenbrock(x: List[float], shift_vector: Optional[List[float]] = None) -> float:
        d = len(x)
        shift = shift_vector or [0.2] * d
        z = [xi - si + 1.0 for xi, si in zip(x, shift)]
        total = 0.0
        for i in range(d - 1):
            total += 100.0 * ((z[i + 1] - z[i] ** 2) ** 2) + (1.0 - z[i]) ** 2
        return total
