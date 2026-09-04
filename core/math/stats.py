"""
Aetheris Mathematical Foundations: Statistical Distributions & Stochastic Processes
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
import random
from typing import List, Tuple, Sequence, Optional


class GaussianDistribution:
    """
    Univariate and multivariate Gaussian probability distribution utilities,
    Gaussian Process kernels, confidence bounds, and likelihood metrics.
    """
    def __init__(self, mean: float = 0.0, variance: float = 1.0) -> None:
        if variance <= 0.0:
            raise ValueError(f"Variance must be positive, got {variance}")
        self.mean: float = float(mean)
        self.variance: float = float(variance)
        self.std_dev: float = math.sqrt(self.variance)

    def pdf(self, x: float) -> float:
        """Probability density function."""
        diff = x - self.mean
        coeff = 1.0 / (self.std_dev * math.sqrt(2.0 * math.pi))
        exponent = -0.5 * (diff * diff) / self.variance
        return coeff * math.exp(exponent)

    def cdf(self, x: float) -> float:
        """Cumulative distribution function via error function."""
        return 0.5 * (1.0 + math.erf((x - self.mean) / (self.std_dev * math.sqrt(2.0))))

    def sample(self, rng: Optional[random.Random] = None) -> float:
        """Box-Muller transform Gaussian sampling."""
        r = rng if rng is not None else random
        u1 = max(1e-15, r.random())
        u2 = r.random()
        z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        return self.mean + self.std_dev * z0

    def sample_n(self, n: int, rng: Optional[random.Random] = None) -> List[float]:
        return [self.sample(rng) for _ in range(n)]

    def confidence_interval(self, alpha: float = 0.95) -> Tuple[float, float]:
        """Returns bounds [mean - z*sigma, mean + z*sigma] for confidence level alpha."""
        # Common z-score approximations
        if math.isclose(alpha, 0.95, abs_tol=0.01):
            z = 1.95996
        elif math.isclose(alpha, 0.99, abs_tol=0.01):
            z = 2.57583
        elif math.isclose(alpha, 0.90, abs_tol=0.01):
            z = 1.64485
        else:
            z = 1.96
        margin = z * self.std_dev
        return (self.mean - margin, self.mean + margin)


class StatisticsHelper:
    """General statistical aggregators and metrics."""
    
    @staticmethod
    def mean(values: Sequence[float]) -> float:
        if not values:
            return 0.0
        return sum(values) / float(len(values))

    @staticmethod
    def variance(values: Sequence[float], ddof: int = 1) -> float:
        n = len(values)
        if n <= ddof:
            return 0.0
        m = StatisticsHelper.mean(values)
        return sum((x - m) ** 2 for x in values) / float(n - ddof)

    @staticmethod
    def std_dev(values: Sequence[float], ddof: int = 1) -> float:
        return math.sqrt(StatisticsHelper.variance(values, ddof))

    @staticmethod
    def median(values: Sequence[float]) -> float:
        if not values:
            return 0.0
        s = sorted(values)
        n = len(s)
        mid = n // 2
        if n % 2 == 1:
            return s[mid]
        return (s[mid - 1] + s[mid]) * 0.5

    @staticmethod
    def quantile(values: Sequence[float], q: float) -> float:
        if not values:
            return 0.0
        s = sorted(values)
        idx = (len(s) - 1) * max(0.0, min(1.0, q))
        low = int(math.floor(idx))
        high = int(math.ceil(idx))
        if low == high:
            return s[low]
        weight = idx - low
        return s[low] * (1.0 - weight) + s[high] * weight
