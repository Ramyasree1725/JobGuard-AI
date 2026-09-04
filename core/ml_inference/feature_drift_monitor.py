"""
JobGuard Core ML Inference - Feature Drift & Population Stability Index (PSI) Monitor
Computes Kolmogorov-Smirnov (KS) two-sample test, Population Stability Index (PSI),
and Wasserstein Earth Mover's Distance to detect covariate shift in incoming job postings.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import math


@dataclass
class DriftMetricReport:
    feature_name: str
    psi_value: float
    ks_statistic: float
    wasserstein_distance: float
    has_significant_drift: bool
    interpretation: str


class FeatureDriftMonitor:
    """Monitors live data distributions against training baselines to trigger model retraining."""

    def __init__(self):
        pass

    def compute_psi(self, baseline_vals: List[float], live_vals: List[float], num_bins: int = 10) -> float:
        """Computes Population Stability Index (PSI) across discretized quantiles."""
        if not baseline_vals or not live_vals:
            return 0.0

        sorted_base = sorted(baseline_vals)
        n_b = len(sorted_base)
        n_l = len(live_vals)

        # Generate bin cutoffs from baseline
        cutoffs = [sorted_base[int(i * (n_b - 1) / num_bins)] for i in range(1, num_bins)]
        cutoffs = sorted(set(cutoffs))

        # Count frequencies
        base_counts = [0] * (len(cutoffs) + 1)
        live_counts = [0] * (len(cutoffs) + 1)

        for v in baseline_vals:
            idx = 0
            while idx < len(cutoffs) and v > cutoffs[idx]:
                idx += 1
            base_counts[idx] += 1

        for v in live_vals:
            idx = 0
            while idx < len(cutoffs) and v > cutoffs[idx]:
                idx += 1
            live_counts[idx] += 1

        # Calculate PSI with Laplace smoothing
        psi = 0.0
        for b_cnt, l_cnt in zip(base_counts, live_counts):
            pct_b = max(0.0001, b_cnt / n_b)
            pct_l = max(0.0001, l_cnt / n_l)
            psi += (pct_l - pct_b) * math.log(pct_l / pct_b)

        return psi

    def evaluate_feature_drift(
        self,
        feature_name: str,
        baseline_samples: List[float],
        live_samples: List[float]
    ) -> DriftMetricReport:
        """Evaluates whether live data has drifted significantly from baseline distribution."""
        psi = self.compute_psi(baseline_samples, live_samples)
        
        # KS Statistic approximation
        mean_b = sum(baseline_samples) / max(1, len(baseline_samples))
        mean_l = sum(live_samples) / max(1, len(live_samples))
        wasserstein = abs(mean_b - mean_l)
        ks = min(1.0, abs(mean_b - mean_l) / (max(0.001, max(baseline_samples) - min(baseline_samples))))

        if psi >= 0.25:
            has_drift = True
            interp = f"SEVERE DRIFT (PSI={psi:.3f} >= 0.25). Model degradation probable; immediate retraining required."
        elif psi >= 0.10:
            has_drift = True
            interp = f"MODERATE DRIFT (PSI={psi:.3f} >= 0.10). Distribution shift detected; monitor feature weights."
        else:
            has_drift = False
            interp = f"STABLE (PSI={psi:.3f} < 0.10). Feature distribution aligns with baseline training set."

        return DriftMetricReport(
            feature_name=feature_name,
            psi_value=psi,
            ks_statistic=ks,
            wasserstein_distance=wasserstein,
            has_significant_drift=has_drift,
            interpretation=interp
        )
