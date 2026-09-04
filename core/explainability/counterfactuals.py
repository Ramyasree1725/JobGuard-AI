"""
JobGuard Core Explainability - Counterfactual Generation Engine
Finds the minimal perturbation required to transition a fraudulent job posting
into a compliant, legitimate posting (Actionable Candidate Guidance).
"""

import math
import random
from typing import List, Dict, Tuple, Callable, Optional, Any
from dataclasses import dataclass, field


@dataclass
class CounterfactualResult:
    original_score: float
    target_score: float
    counterfactual_score: float
    modified_features: Dict[str, Tuple[float, float]]  # feat -> (orig_val, new_val)
    total_l1_distance: float
    sparsity_ratio: float  # Fraction of features left unchanged


class CounterfactualGenerator:
    """Gradient-free Nelder-Mead / Coordinate Search optimizer for sparse counterfactuals."""

    def __init__(self, predict_fn: Callable[[List[float]], float], target_score: float = 0.0):
        self.predict_fn = predict_fn
        self.target_score = target_score

    def generate(
        self,
        input_vector: List[float],
        feature_names: Optional[List[str]] = None,
        feature_bounds: Optional[List[Tuple[float, float]]] = None,
        max_iterations: int = 200,
        l1_penalty: float = 0.1
    ) -> CounterfactualResult:
        n = len(input_vector)
        names = feature_names or [f"f_{i}" for i in range(n)]
        bounds = feature_bounds or [(0.0, 1.0)] * n

        orig_score = self.predict_fn(input_vector)
        best_cf = list(input_vector)
        best_loss = float("inf")

        def loss_fn(candidate: List[float]) -> float:
            score = self.predict_fn(candidate)
            pred_loss = (score - self.target_score) ** 2
            l1_dist = sum(abs(c - o) for c, o in zip(candidate, input_vector))
            return pred_loss + l1_penalty * l1_dist

        # Iterative coordinate descent with random restarts
        for _ in range(max_iterations):
            # Select random feature coordinate to perturb towards baseline
            coord = random.randint(0, n - 1)
            low_b, high_b = bounds[coord]
            
            # Try setting to zero or reducing
            test_val = max(low_b, min(high_b, best_cf[coord] * random.uniform(0.0, 0.8)))
            candidate = list(best_cf)
            candidate[coord] = test_val
            
            l = loss_fn(candidate)
            if l < best_loss:
                best_loss = l
                best_cf = candidate

        final_score = self.predict_fn(best_cf)
        modified: Dict[str, Tuple[float, float]] = {}
        changed_count = 0
        total_l1 = 0.0

        for i in range(n):
            if abs(best_cf[i] - input_vector[i]) > 1e-4:
                modified[names[i]] = (round(input_vector[i], 3), round(best_cf[i], 3))
                changed_count += 1
                total_l1 += abs(best_cf[i] - input_vector[i])

        sparsity = (n - changed_count) / max(1, n)

        return CounterfactualResult(
            original_score=round(orig_score, 2),
            target_score=round(self.target_score, 2),
            counterfactual_score=round(final_score, 2),
            modified_features=modified,
            total_l1_distance=round(total_l1, 3),
            sparsity_ratio=round(sparsity, 3)
        )
