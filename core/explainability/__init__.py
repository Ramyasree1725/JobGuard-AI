"""
JobGuard Core Explainability & Model Interpretability Framework
Provides SHAP value approximations, integrated gradients, counterfactual candidate generators,
and surrogate decision tree attributions for transparent candidate risk scoring.
"""

from .shap_approx import KernelSHAPApproximator, ShapExplanation
from .integrated_gradients import IntegratedGradients, GradientAttribution
from .counterfactuals import CounterfactualGenerator, CounterfactualResult
from .attribution_trees import SurrogateTreeExplainer, AttributionRule

__all__ = [
    "KernelSHAPApproximator",
    "ShapExplanation",
    "IntegratedGradients",
    "GradientAttribution",
    "CounterfactualGenerator",
    "CounterfactualResult",
    "SurrogateTreeExplainer",
    "AttributionRule",
]
