"""
JobGuard Core Explainability - Kernel SHAP Value Approximation Engine
Computes Shapley additive explanations (SHAP) across textual and tabular feature sets
to attribute exact risk point contributions to individual clauses and indicators.
"""

import math
import random
from typing import Dict, List, Optional, Callable, Any, Tuple
from dataclasses import dataclass, field


@dataclass
class ShapExplanation:
    base_value: float
    predicted_value: float
    feature_contributions: Dict[str, float]
    top_positive_features: List[Tuple[str, float]]
    top_negative_features: List[Tuple[str, float]]


class KernelSHAPApproximator:
    """Estimates Shapley values using weighted linear surrogate regressions."""

    def __init__(self, predict_fn: Callable[[List[float]], float], num_samples: int = 128):
        self.predict_fn = predict_fn
        self.num_samples = num_samples

    def explain(self, instance: List[float], baseline: Optional[List[float]] = None, feature_names: Optional[List[str]] = None) -> ShapExplanation:
        """Compute Shapley value attributions for the input instance."""
        num_feats = len(instance)
        names = feature_names or [f"feat_{i}" for i in range(num_feats)]
        base = baseline or [0.0] * num_feats

        base_val = self.predict_fn(base)
        pred_val = self.predict_fn(instance)

        # Generate binary coalition sample masks
        masks: List[List[int]] = []
        weights: List[float] = []
        sampled_inputs: List[List[float]] = []

        for _ in range(self.num_samples):
            # Random subset of features
            mask = [random.randint(0, 1) for _ in range(num_feats)]
            s = sum(mask)
            
            # Shapley kernel weight: (M - 1) / (comb(M, |z|) * |z| * (M - |z|))
            if s == 0 or s == num_feats:
                w = 1000.0  # Large weight for boundary coalitions
            else:
                try:
                    comb = math.comb(num_feats, s)
                    w = (num_feats - 1.0) / (comb * s * (num_feats - s))
                except Exception:
                    w = 1.0

            # Synthesize input: blend instance and baseline
            synth = [instance[i] if mask[i] == 1 else base[i] for i in range(num_feats)]
            masks.append(mask)
            weights.append(min(100.0, w))
            sampled_inputs.append(synth)

        # Evaluate model predictions for all samples
        sample_preds = [self.predict_fn(inp) for inp in sampled_inputs]

        # Weighted Least Squares regression to solve for phi (Shapley coefficients)
        contributions = self._weighted_least_squares(masks, sample_preds, weights, num_feats, base_val)

        feat_contribs: Dict[str, float] = {
            names[i]: round(contributions[i], 4) for i in range(num_feats)
        }

        sorted_items = sorted(feat_contribs.items(), key=lambda x: abs(x[1]), reverse=True)
        top_pos = [item for item in sorted_items if item[1] > 0][:5]
        top_neg = [item for item in sorted_items if item[1] < 0][:5]

        return ShapExplanation(
            base_value=round(base_val, 4),
            predicted_value=round(pred_val, 4),
            feature_contributions=feat_contribs,
            top_positive_features=top_pos,
            top_negative_features=top_neg
        )

    def _weighted_least_squares(
        self,
        X: List[List[int]],
        y: List[float],
        w: List[float],
        num_feats: int,
        base_val: float
    ) -> List[float]:
        """Solve (X^T W X) \beta = X^T W (y - base_val)."""
        # Form normal equations
        xtwx = [[0.0] * num_feats for _ in range(num_feats)]
        xtwy = [0.0] * num_feats

        for mask, target, weight in zip(X, y, w):
            diff = target - base_val
            for i in range(num_feats):
                if mask[i] == 1:
                    xtwy[i] += weight * mask[i] * diff
                    for j in range(num_feats):
                        if mask[j] == 1:
                            xtwx[i][j] += weight * mask[i] * mask[j]

        # Add ridge regularization diagonal for numerical stability
        for i in range(num_feats):
            xtwx[i][i] += 1e-4

        # Gauss-Jordan elimination
        return self._solve_linear_system(xtwx, xtwy, num_feats)

    @staticmethod
    def _solve_linear_system(A: List[List[float]], b: List[float], n: int) -> List[float]:
        M = [row[:] + [b[i]] for i, row in enumerate(A)]
        for i in range(n):
            # Pivot
            max_row = i
            for k in range(i + 1, n):
                if abs(M[k][i]) > abs(M[max_row][i]):
                    max_row = k
            M[i], M[max_row] = M[max_row], M[i]

            pivot = M[i][i]
            if abs(pivot) < 1e-12:
                continue

            for j in range(i, n + 1):
                M[i][j] /= pivot

            for k in range(n):
                if k != i:
                    factor = M[k][i]
                    for j in range(i, n + 1):
                        M[k][j] -= factor * M[i][j]

        return [M[i][n] for i in range(n)]
