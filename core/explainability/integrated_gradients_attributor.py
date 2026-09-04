"""
JobGuard Core Explainability - Integrated Gradients & Path Attribution Engine
Computes path-integral feature attributions (Axiomatic Attribution) satisfying
Completeness, Implementation Invariance, and Linearity axioms for deep NLP models.
"""

from typing import Dict, List, Set, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
import math


@dataclass
class TokenAttribution:
    token: str
    attribution_score: float  # Positive = drives fraud classification, Negative = drives authentic
    absolute_impact: float
    token_index: int


@dataclass
class IntegratedGradientsExplanation:
    tokens: List[str]
    attributions: List[TokenAttribution]
    convergence_delta: float
    baseline_prediction: float
    target_prediction: float
    top_contributing_phrases: List[str]


class IntegratedGradientsAttributor:
    """Computes Integrated Gradients along straight interpolation paths between baseline and input."""

    def __init__(self, m_steps: int = 50):
        self.m_steps = m_steps

    def attribute_text(
        self,
        tokens: List[str],
        embedding_matrix: List[List[float]],
        grad_fn: Callable[[List[List[float]]], List[List[float]]],
        predict_fn: Callable[[List[List[float]]], float],
        baseline_matrix: Optional[List[List[float]]] = None
    ) -> IntegratedGradientsExplanation:
        """Approximates the Riemann path integral of gradients along the straight line from baseline."""
        num_tokens = len(tokens)
        embed_dim = len(embedding_matrix[0]) if num_tokens > 0 else 0

        if baseline_matrix is None:
            baseline_matrix = [[0.0] * embed_dim for _ in range(num_tokens)]

        # Accumulate gradients across m_steps interpolated inputs
        accumulated_grads = [[0.0] * embed_dim for _ in range(num_tokens)]

        for k in range(1, self.m_steps + 1):
            alpha = k / float(self.m_steps)
            
            # Interpolated embedding = baseline + alpha * (input - baseline)
            interpolated = [
                [
                    baseline_matrix[i][d] + alpha * (embedding_matrix[i][d] - baseline_matrix[i][d])
                    for d in range(embed_dim)
                ]
                for i in range(num_tokens)
            ]

            step_grads = grad_fn(interpolated)
            for i in range(num_tokens):
                for d in range(embed_dim):
                    accumulated_grads[i][d] += step_grads[i][d]

        # Integrated Gradients = (input - baseline) * (1/m * sum(gradients))
        attributions: List[TokenAttribution] = []
        for i in range(num_tokens):
            token_score = 0.0
            for d in range(embed_dim):
                avg_grad = accumulated_grads[i][d] / float(self.m_steps)
                diff = embedding_matrix[i][d] - baseline_matrix[i][d]
                token_score += diff * avg_grad

            attributions.append(TokenAttribution(
                token=tokens[i],
                attribution_score=token_score,
                absolute_impact=abs(token_score),
                token_index=i
            ))

        base_pred = predict_fn(baseline_matrix)
        target_pred = predict_fn(embedding_matrix)
        sum_attributions = sum(a.attribution_score for a in attributions)
        delta = abs((target_pred - base_pred) - sum_attributions)

        # Extract top positive contributors
        sorted_attr = sorted(attributions, key=lambda x: x.attribution_score, reverse=True)
        top_tokens = [a.token for a in sorted_attr[:5] if a.attribution_score > 0.0]

        return IntegratedGradientsExplanation(
            tokens=tokens,
            attributions=attributions,
            convergence_delta=delta,
            baseline_prediction=base_pred,
            target_prediction=target_pred,
            top_contributing_phrases=top_tokens
        )
