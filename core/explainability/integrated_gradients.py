"""
JobGuard Core Explainability - Integrated Gradients & Path Attribution
Calculates path integrals between a neutral baseline and the input vector,
guaranteeing completeness and implementation invariance for deep models.
"""

from typing import List, Tuple, Dict, Callable, Optional
from dataclasses import dataclass


@dataclass
class GradientAttribution:
    total_attribution: float
    feature_attributions: Dict[str, float]
    convergence_delta: float  # Difference between integral sum and f(x) - f(baseline)


class IntegratedGradients:
    """Axiomatic feature attribution using numerical Riemann path integration."""

    def __init__(self, steps: int = 50):
        self.steps = max(10, steps)

    def attribute(
        self,
        predict_fn: Callable[[List[float]], float],
        input_vector: List[float],
        baseline_vector: Optional[List[float]] = None,
        feature_names: Optional[List[str]] = None
    ) -> GradientAttribution:
        n = len(input_vector)
        baseline = baseline_vector or [0.0] * n
        names = feature_names or [f"dim_{i}" for i in range(n)]

        # Step 1: Interpolate along straight line path: x_k = baseline + (k / m) * (input - baseline)
        interpolated_points: List[List[float]] = []
        for k in range(1, self.steps + 1):
            alpha = k / self.steps
            point = [baseline[i] + alpha * (input_vector[i] - baseline[i]) for i in range(n)]
            interpolated_points.append(point)

        # Step 2: Approximate gradients at each interpolated point via finite differences
        eps = 1e-4
        avg_gradients = [0.0] * n

        for pt in interpolated_points:
            base_score = predict_fn(pt)
            for i in range(n):
                perturbed = list(pt)
                perturbed[i] += eps
                perturbed_score = predict_fn(perturbed)
                grad_i = (perturbed_score - base_score) / eps
                avg_gradients[i] += grad_i

        for i in range(n):
            avg_gradients[i] /= self.steps

        # Step 3: Integrated Gradients: (input_i - baseline_i) * avg_grad_i
        attributions: Dict[str, float] = {}
        total_attr = 0.0
        for i in range(n):
            attr_i = (input_vector[i] - baseline[i]) * avg_gradients[i]
            attributions[names[i]] = round(attr_i, 5)
            total_attr += attr_i

        # Step 4: Completeness Check: Sum(IG) should equal f(x) - f(baseline)
        fx = predict_fn(input_vector)
        f_base = predict_fn(baseline)
        expected_diff = fx - f_base
        delta = abs(total_attr - expected_diff)

        return GradientAttribution(
            total_attribution=round(total_attr, 4),
            feature_attributions=attributions,
            convergence_delta=round(delta, 5)
        )
