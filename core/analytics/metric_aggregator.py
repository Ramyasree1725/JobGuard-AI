"""
JobGuard Core Analytics - HyperLogLog & T-Digest High-Precision Aggregators
Computes approximate percentiles (P50, P90, P99) and distinct scammer cardinality
with minimal fixed memory footprints.
"""

import math
import hashlib
from typing import List, Dict, Tuple, Optional


class HyperLogLogCounter:
    """Distinct cardinality estimator with O(log log N) memory footprint."""

    def __init__(self, p: int = 10):
        self.p = p  # Precision parameter (m = 2^p registers)
        self.m = 1 << p
        self.registers = [0] * self.m
        
        # Alpha constant calculation
        if self.m == 16:
            self.alpha = 0.673
        elif self.m == 32:
            self.alpha = 0.697
        elif self.m == 64:
            self.alpha = 0.709
        else:
            self.alpha = 0.7213 / (1.0 + 1.079 / self.m)

    def add(self, item: str) -> None:
        """Hash item and update matching register."""
        h = int(hashlib.sha256(item.encode("utf-8")).hexdigest()[:16], 16)
        j = h & (self.m - 1)  # Register index
        w = h >> self.p       # Remaining bits

        # Count leading zeros in w + 1
        rho = 1
        while w > 0 and (w & 1) == 0:
            rho += 1
            w >>= 1

        self.registers[j] = max(self.registers[j], rho)

    def count(self) -> int:
        """Estimate distinct cardinality."""
        z = 1.0 / sum(2.0 ** (-r) for r in self.registers)
        raw_est = self.alpha * (self.m ** 2) * z

        # Small range correction
        if raw_est <= 2.5 * self.m:
            v = self.registers.count(0)
            if v > 0:
                return int(self.m * math.log(self.m / v))
        return int(raw_est)


class TDigestQuantileEstimator:
    """Accurate streaming percentile (P50, P95, P99) accumulator."""

    def __init__(self, max_centroids: int = 100):
        self.max_centroids = max_centroids
        self.centroids: List[List[float]] = []  # [mean, weight]

    def add(self, value: float, weight: float = 1.0) -> None:
        self.centroids.append([float(value), float(weight)])
        if len(self.centroids) > self.max_centroids * 2:
            self._compress()

    def _compress(self) -> None:
        if not self.centroids:
            return
        self.centroids.sort(key=lambda c: c[0])
        compressed = []
        curr_mean, curr_wt = self.centroids[0]

        for m, w in self.centroids[1:]:
            if curr_wt + w <= 10.0:
                curr_mean = (curr_mean * curr_wt + m * w) / (curr_wt + w)
                curr_wt += w
            else:
                compressed.append([curr_mean, curr_wt])
                curr_mean, curr_wt = m, w

        compressed.append([curr_mean, curr_wt])
        self.centroids = compressed

    def quantile(self, q: float) -> float:
        """Query quantile q in range [0.0, 1.0]."""
        if not self.centroids:
            return 0.0
        self._compress()
        total_wt = sum(c[1] for c in self.centroids)
        target_wt = q * total_wt
        cum_wt = 0.0

        for mean, wt in self.centroids:
            cum_wt += wt
            if cum_wt >= target_wt:
                return round(mean, 2)
        return round(self.centroids[-1][0], 2)


class HistogramBinner:
    """Categorizes continuous scores into discrete statistical histogram buckets."""

    def __init__(self, bin_edges: Optional[List[float]] = None):
        self.bin_edges = bin_edges or [0.0, 20.0, 40.0, 60.0, 80.0, 100.0]
        self.counts = [0] * (len(self.bin_edges) - 1)

    def add_value(self, val: float) -> None:
        for i in range(len(self.bin_edges) - 1):
            if self.bin_edges[i] <= val < self.bin_edges[i + 1]:
                self.counts[i] += 1
                return
        if val >= self.bin_edges[-1]:
            self.counts[-1] += 1

    def get_distribution(self) -> Dict[str, int]:
        dist = {}
        for i in range(len(self.bin_edges) - 1):
            label = f"{self.bin_edges[i]:.0f}-{self.bin_edges[i+1]:.0f}%"
            dist[label] = self.counts[i]
        return dist
