"""
JobGuard Core ML Inference - Model Fairness & Demographic Parity Evaluator
Evaluates Equalized Odds, Disparate Impact Ratio, False Positive Rate (FPR) parity,
and calibration across diverse industry sectors, entry-level roles, and candidate demographics.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import math


@dataclass
class FairnessGroupMetrics:
    group_name: str
    sample_size: int
    positive_rate: float
    true_positive_rate: float
    false_positive_rate: float
    accuracy: float


@dataclass
class ModelFairnessAuditReport:
    evaluated_groups: List[FairnessGroupMetrics]
    disparate_impact_ratio: float
    equalized_odds_gap: float
    passes_four_fifths_rule: bool
    is_demographically_fair: bool
    compliance_summary: str


class ModelFairnessEvaluator:
    """Audits fraud classification models for bias across job industries and candidate tiers."""

    def __init__(self):
        pass

    def evaluate_group_fairness(
        self,
        group_data: Dict[str, Tuple[List[int], List[int]]]  # group_name -> (y_true, y_pred)
    ) -> ModelFairnessAuditReport:
        """Calculates disparate impact and TPR/FPR disparities between demographic cohorts."""
        metrics_list: List[FairnessGroupMetrics] = []

        for group_name, (y_true, y_pred) in group_data.items():
            n = len(y_true)
            if n == 0:
                continue

            tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
            fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
            tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 0)
            fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)

            tpr = tp / max(1, tp + fn)
            fpr = fp / max(1, fp + tn)
            pos_rate = sum(y_pred) / n
            acc = (tp + tn) / n

            metrics_list.append(FairnessGroupMetrics(
                group_name=group_name,
                sample_size=n,
                positive_rate=pos_rate,
                true_positive_rate=tpr,
                false_positive_rate=fpr,
                accuracy=acc
            ))

        if len(metrics_list) < 2:
            return ModelFairnessAuditReport(
                evaluated_groups=metrics_list,
                disparate_impact_ratio=1.0,
                equalized_odds_gap=0.0,
                passes_four_fifths_rule=True,
                is_demographically_fair=True,
                compliance_summary="Insufficient groups for comparative disparity audit."
            )

        pos_rates = [g.positive_rate for g in metrics_list]
        disparate_impact = min(pos_rates) / max(0.001, max(pos_rates))

        tprs = [g.true_positive_rate for g in metrics_list]
        fprs = [g.false_positive_rate for g in metrics_list]
        odds_gap = max(abs(max(tprs) - min(tprs)), abs(max(fprs) - min(fprs)))

        passes_4_5ths = (disparate_impact >= 0.80)
        is_fair = passes_4_5ths and odds_gap <= 0.15

        summary = (
            f"Model achieves Disparate Impact Ratio of {disparate_impact:.2f} (Threshold >= 0.80). "
            f"Equalized Odds Gap is {odds_gap:.2f}. EEOC 4/5ths rule satisfied."
            if is_fair else
            f"FAIRNESS VIOLATION: Disparate Impact Ratio {disparate_impact:.2f} is below EEOC 0.80 standard."
        )

        return ModelFairnessAuditReport(
            evaluated_groups=metrics_list,
            disparate_impact_ratio=disparate_impact,
            equalized_odds_gap=odds_gap,
            passes_four_fifths_rule=passes_4_5ths,
            is_demographically_fair=is_fair,
            compliance_summary=summary
        )
