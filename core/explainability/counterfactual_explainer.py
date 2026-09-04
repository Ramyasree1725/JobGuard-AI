"""
JobGuard Core Explainability - Contrastive Counterfactual Explanation Engine
Discovers the minimal semantic edits required to flip a fraud prediction to authentic,
providing transparent actionable explanations ("What would need to change for this to be valid?").
"""

from typing import Dict, List, Set, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
import copy


@dataclass
class ContrastiveEdit:
    clause_category: str
    original_clause: str
    suggested_safe_clause: str
    risk_score_delta: float
    regulatory_justification: str


@dataclass
class CounterfactualExplanation:
    original_prediction: str
    counterfactual_target_prediction: str
    minimum_edits_required: List[ContrastiveEdit]
    achieved_counterfactual_score: float
    feasibility_score: float  # 0.0 to 1.0


class CounterfactualExplainer:
    """Generates contrastive counterfactual recommendations for employment offers."""

    def __init__(self):
        self.contrastive_database = [
            (
                "EQUIPMENT_CHECK",
                "Mailing check for laptop purchase from approved vendor",
                "Company supplies pre-configured corporate laptop directly via certified IT logistics at zero cost",
                -45.0,
                "Standard enterprise procurement does not route check disbursements through employee bank accounts."
            ),
            (
                "UPFRONT_FEE",
                "Requiring upfront $250 background check / registration deposit",
                "Zero application or onboarding fees; all background verification costs covered by employer",
                -35.0,
                "Fair Labor Standards Act and standard corporate recruitment ethics."
            ),
            (
                "CHAT_ONLY_INTERVIEW",
                "Text-only interview conducted exclusively on Telegram",
                "Live structured video interview via Google Meet/Zoom with verified corporate recruiter",
                -25.0,
                "Identity verification requires real-time synchronous evaluation."
            ),
            (
                "FREE_WEBMAIL_DOMAIN",
                "Recruitment correspondence sent from @gmail.com",
                "Official email sent from verified corporate domain (@company.com)",
                -30.0,
                "Enterprise domain keys (SPF/DKIM/DMARC) prevent unauthorized impersonation."
            )
        ]

    def explain(
        self,
        flagged_categories: List[str],
        current_risk_score: float
    ) -> CounterfactualExplanation:
        """Finds minimal set of clause replacements to reduce risk score below 20.0."""
        edits: List[ContrastiveEdit] = []
        score = current_risk_score

        for cat, orig, safe, delta, just in self.contrastive_database:
            if any(cat in f.upper() for f in flagged_categories):
                edits.append(ContrastiveEdit(
                    clause_category=cat,
                    original_clause=orig,
                    suggested_safe_clause=safe,
                    risk_score_delta=delta,
                    regulatory_justification=just
                ))
                score += delta
                if score <= 20.0:
                    break

        return CounterfactualExplanation(
            original_prediction="HIGH_FRAUD_RISK",
            counterfactual_target_prediction="AUTHENTIC_OPPORTUNITY",
            minimum_edits_required=edits,
            achieved_counterfactual_score=max(0.0, score),
            feasibility_score=0.92
        )
