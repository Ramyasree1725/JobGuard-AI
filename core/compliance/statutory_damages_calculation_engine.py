"""
JobGuard Core Compliance - Statutory Damages & Restitution Calculation Engine
Calculates statutory liquidated damages, civil penalty multipliers, prejudgment interest,
and class-action statutory penalty aggregates for victims of employment fraud schemes.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import datetime
import math


@dataclass
class DamageClaimItem:
    claim_id: str
    description: str
    actual_out_of_pocket_loss_usd: float
    loss_date: datetime.date
    statute_code: str
    statutory_liquidated_multiplier: float  # e.g., 2.0 (double) or 3.0 (treble)
    applicable_civil_penalty_usd: float


@dataclass
class RestitutionAssessmentReport:
    total_actual_damages_usd: float
    total_statutory_liquidated_damages_usd: float
    total_accrued_interest_usd: float
    total_civil_penalties_usd: float
    gross_restitution_entitlement_usd: float
    statutory_citations: List[str]
    breakdown_narrative: List[str]


class StatutoryDamagesCalculationEngine:
    """Computes full legal damages, liquidated multipliers, and interest for fraud complaints."""

    def __init__(self, annual_statutory_interest_rate: float = 0.08):
        self.interest_rate = annual_statutory_interest_rate

    def calculate_restitution(
        self,
        claims: List[DamageClaimItem],
        calculation_date: Optional[datetime.date] = None
    ) -> RestitutionAssessmentReport:
        """Calculates exact statutory restitution breakdown."""
        calc_date = calculation_date or datetime.date.today()

        total_actual = 0.0
        total_liquidated = 0.0
        total_interest = 0.0
        total_penalties = 0.0
        citations: Set[str] = set()
        narratives: List[str] = []

        for item in claims:
            total_actual += item.actual_out_of_pocket_loss_usd
            liquidated_portion = item.actual_out_of_pocket_loss_usd * (item.statutory_liquidated_multiplier - 1.0)
            total_liquidated += max(0.0, liquidated_portion)
            total_penalties += item.applicable_civil_penalty_usd
            citations.add(item.statute_code)

            # Compute prejudgment statutory interest
            days_elapsed = max(0, (calc_date - item.loss_date).days)
            years = days_elapsed / 365.25
            interest = item.actual_out_of_pocket_loss_usd * self.interest_rate * years
            total_interest += interest

            narratives.append(
                f"Claim {item.claim_id}: Actual loss of ${item.actual_out_of_pocket_loss_usd:,.2f} on {item.loss_date}. "
                f"Statutory multiplier ({item.statutory_liquidated_multiplier:.1f}x) yields ${item.actual_out_of_pocket_loss_usd * item.statutory_liquidated_multiplier:,.2f} "
                f"plus ${interest:,.2f} in statutory interest ({days_elapsed} days @ {self.interest_rate * 100:.1f}%)."
            )

        gross_total = total_actual + total_liquidated + total_interest + total_penalties

        return RestitutionAssessmentReport(
            total_actual_damages_usd=total_actual,
            total_statutory_liquidated_damages_usd=total_liquidated,
            total_accrued_interest_usd=total_interest,
            total_civil_penalties_usd=total_penalties,
            gross_restitution_entitlement_usd=gross_total,
            statutory_citations=list(citations),
            breakdown_narrative=narratives
        )
