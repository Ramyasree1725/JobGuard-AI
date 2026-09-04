"""
JobGuard Core Compliance - Statutory Penalties, Fine Multipliers & Restitution Matrices
Maintains sentencing guidelines, base fine calculations, victim restitution formulas,
and statutory damages across US Federal, EU GDPR, Indian IT Act, and UK Fraud Act jurisdictions.
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class PenaltyComputation:
    statute_code: str
    jurisdiction: str
    minimum_base_fine_usd: float
    maximum_base_fine_usd: float
    statutory_multiplier: float
    imprisonment_years_max: float
    mandatory_restitution: bool
    formula_description: str


class StatutoryPenaltiesMatrix:
    """Master calculations for assessing legal liability and criminal exposure of fraud operators."""

    def __init__(self):
        self.matrices: Dict[str, PenaltyComputation] = {}
        self._load_penalty_matrices()

    def register_penalty(self, comp: PenaltyComputation) -> None:
        self.matrices[comp.statute_code] = comp

    def _load_penalty_matrices(self) -> None:
        """Populate international sentencing guidelines."""
        entries = [
            PenaltyComputation(
                statute_code="USA-18USC-1343",
                jurisdiction="US Federal",
                minimum_base_fine_usd=250000.0,
                maximum_base_fine_usd=1000000.0,
                statutory_multiplier=2.0,  # 2x pecuniary gain
                imprisonment_years_max=20.0,
                mandatory_restitution=True,
                formula_description="Max($1,000,000, 2 * Gross Pecuniary Gain) + Full Mandatory Restitution"
            ),
            PenaltyComputation(
                statute_code="USA-FTC-SEC5",
                jurisdiction="US Federal Civil",
                minimum_base_fine_usd=50120.0,
                maximum_base_fine_usd=10000000.0,
                statutory_multiplier=1.0,
                imprisonment_years_max=0.0,
                mandatory_restitution=True,
                formula_description="$50,120 per violation per day + Section 19 consumer redress"
            ),
            PenaltyComputation(
                statute_code="IND-IT-66D",
                jurisdiction="India Federal",
                minimum_base_fine_usd=1200.0,
                maximum_base_fine_usd=12000.0,
                statutory_multiplier=1.0,
                imprisonment_years_max=3.0,
                mandatory_restitution=True,
                formula_description="₹1,00,000 statutory fine + CrPC Section 357 victim compensation"
            ),
            PenaltyComputation(
                statute_code="EU-GDPR-ART83",
                jurisdiction="European Union",
                minimum_base_fine_usd=10000000.0,
                maximum_base_fine_usd=20000000.0,
                statutory_multiplier=0.04,  # 4% worldwide annual turnover
                imprisonment_years_max=0.0,
                mandatory_restitution=True,
                formula_description="Max(€20,000,000, 4% of total worldwide annual turnover)"
            ),
            PenaltyComputation(
                statute_code="GBR-FRAUD-2006",
                jurisdiction="United Kingdom",
                minimum_base_fine_usd=50000.0,
                maximum_base_fine_usd=5000000.0,
                statutory_multiplier=3.0,
                imprisonment_years_max=10.0,
                mandatory_restitution=True,
                formula_description="Unlimited fine under Crown Court + Proceeds of Crime Act (POCA) confiscation"
            )
        ]

        for e in entries:
            self.register_penalty(e)

    def calculate_estimated_liability(self, statute_code: str, victim_losses_usd: float) -> Dict[str, Any]:
        """Calculates total criminal and civil financial liability for a fraud syndicate."""
        comp = self.matrices.get(statute_code, self.matrices["USA-18USC-1343"])
        
        statutory_fine = max(comp.minimum_base_fine_usd, min(comp.maximum_base_fine_usd, victim_losses_usd * comp.statutory_multiplier))
        restitution = victim_losses_usd if comp.mandatory_restitution else 0.0
        total_liability = statutory_fine + restitution

        return {
            "statute_code": comp.statute_code,
            "jurisdiction": comp.jurisdiction,
            "statutory_fine_usd": round(statutory_fine, 2),
            "mandatory_restitution_usd": round(restitution, 2),
            "total_estimated_liability_usd": round(total_liability, 2),
            "max_custodial_sentence_years": comp.imprisonment_years_max,
            "formula_applied": comp.formula_description
        }
