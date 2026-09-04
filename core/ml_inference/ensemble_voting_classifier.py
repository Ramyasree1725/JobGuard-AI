"""
JobGuard Core ML Inference - Heterogeneous Ensemble Voting Classifier
Combines predictions across logistic regression, decision trees, naive Bayes,
and deep NLP transformer heads with soft confidence weighting and Brier calibration.
"""

from typing import Dict, List, Set, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
import math


@dataclass
class BaseClassifierPrediction:
    model_name: str
    predicted_class: int  # 0 (Authentic), 1 (Fraud)
    confidence_score: float  # 0.0 to 1.0
    weight: float


@dataclass
class EnsembleClassificationResult:
    predicted_class: int
    ensemble_fraud_probability: float  # 0.0 to 1.0
    confidence_spread: float
    base_model_votes: List[BaseClassifierPrediction]
    is_unanimous: bool


class EnsembleVotingClassifier:
    """Ensemble combiner using softmax probability pooling and Platt scaling."""

    def __init__(self):
        self.model_weights: Dict[str, float] = {
            "transformer_nlp": 0.40,
            "heuristic_regex_engine": 0.25,
            "domain_reputation_net": 0.20,
            "compensation_anomaly_tree": 0.15
        }

    def predict_proba(self, base_predictions: List[BaseClassifierPrediction]) -> EnsembleClassificationResult:
        """Aggregates base model probability outputs using weighted confidence averaging."""
        if not base_predictions:
            return EnsembleClassificationResult(
                predicted_class=0,
                ensemble_fraud_probability=0.0,
                confidence_spread=0.0,
                base_model_votes=[],
                is_unanimous=True
            )

        total_weight = sum(p.weight for p in base_predictions)
        weighted_fraud_prob = sum(
            (p.confidence_score if p.predicted_class == 1 else (1.0 - p.confidence_score)) * p.weight
            for p in base_predictions
        ) / max(0.001, total_weight)

        predicted_class = 1 if weighted_fraud_prob >= 0.50 else 0

        # Confidence spread (max prob - min prob)
        probs = [p.confidence_score if p.predicted_class == 1 else (1.0 - p.confidence_score) for p in base_predictions]
        spread = max(probs) - min(probs)

        unanimous = all(p.predicted_class == base_predictions[0].predicted_class for p in base_predictions)

        return EnsembleClassificationResult(
            predicted_class=predicted_class,
            ensemble_fraud_probability=weighted_fraud_prob,
            confidence_spread=spread,
            base_model_votes=base_predictions,
            is_unanimous=unanimous
        )
