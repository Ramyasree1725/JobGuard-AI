"""
JobGuard Core Compliance - International Labor Organization (ILO) Treaty Matrix
Maps ILO Convention No. 181 (Private Employment Agencies), Convention No. 95 (Protection of Wages),
and UN Global Compact human rights standards against deceptive cross-border recruiting traps.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class ILOTreatyStandard(Enum):
    ILO_C181_FEE_PROHIBITION = "ILO_C181_FEE_PROHIBITION"
    ILO_C095_WAGE_PROTECTION = "ILO_C095_WAGE_PROTECTION"
    ILO_C029_FORCED_LABOR = "ILO_C029_FORCED_LABOR"
    UN_MIGRANT_WORKERS_1990 = "UN_MIGRANT_WORKERS_1990"


@dataclass
class TreatyProvision:
    provision_id: str
    treaty_name: str
    article_number: str
    core_mandate: str
    signatory_countries_count: int
    direct_statutory_text: str
    is_fee_charging_prohibited: bool


@dataclass
class TreatyComplianceAuditResult:
    is_fully_compliant: bool
    violated_provisions: List[TreatyProvision]
    international_remedies: List[str]
    compliance_score: float  # 0 to 100


class InternationalLaborTreatyMatrix:
    """Evaluates cross-border recruitment practices against binding international labor conventions."""

    def __init__(self):
        self.provisions: Dict[str, TreatyProvision] = {}
        self._initialize_treaty_database()

    def _initialize_treaty_database(self) -> None:
        """Populate international labor conventions and standards."""

        # ILO Convention No. 181, Article 7 (Fundamental Principle: No fees to jobseekers)
        self.provisions["ILO_C181_ART7"] = TreatyProvision(
            provision_id="ILO_C181_ART7",
            treaty_name="ILO Private Employment Agencies Convention, 1997 (No. 181)",
            article_number="Article 7(1)",
            core_mandate="Private employment agencies shall not charge directly or indirectly, in whole or in part, any fees or costs to workers.",
            signatory_countries_count=37,
            direct_statutory_text="Private employment agencies shall not charge directly or indirectly, in whole or in part, any fees or costs to workers. In the interest of the workers concerned, the competent authority may authorize exceptions in respect of certain categories of workers.",
            is_fee_charging_prohibited=True
        )

        # ILO Convention No. 95, Article 3 (Direct Wage Payment in Legal Tender)
        self.provisions["ILO_C095_ART3"] = TreatyProvision(
            provision_id="ILO_C095_ART3",
            treaty_name="ILO Protection of Wages Convention, 1949 (No. 95)",
            article_number="Article 3",
            core_mandate="Wages payable in money shall be paid only in legal tender, and payment in the form of promissory notes, vouchers, or coupons is prohibited.",
            signatory_countries_count=99,
            direct_statutory_text="Wages payable in money shall be paid only in legal tender, and payment in the form of promissory notes, vouchers, coupons, or any other form alleged to represent legal tender shall be prohibited.",
            is_fee_charging_prohibited=False
        )

        # ILO Convention No. 29, Article 2 (Forced or Compulsory Labor Definition)
        self.provisions["ILO_C029_ART2"] = TreatyProvision(
            provision_id="ILO_C029_ART2",
            treaty_name="ILO Forced Labour Convention, 1930 (No. 29)",
            article_number="Article 2(1)",
            core_mandate="All work or service which is exacted from any person under the menace of any penalty and for which the said person has not offered himself voluntarily.",
            signatory_countries_count=181,
            direct_statutory_text="For the purposes of this Convention the term forced or compulsory labour shall mean all work or service which is exacted from any person under the menace of any penalty and for which the said person has not offered himself voluntarily.",
            is_fee_charging_prohibited=False
        )

    def audit_terms_against_treaties(self, has_recruitment_fees: bool, has_crypto_or_scrip_pay: bool) -> TreatyComplianceAuditResult:
        """Audits employment offer conditions against international conventions."""
        violations: List[TreatyProvision] = []
        score = 100.0
        remedies: List[str] = []

        if has_recruitment_fees:
            p = self.provisions["ILO_C181_ART7"]
            violations.append(p)
            score -= 60.0
            remedies.append("Immediate cessation of candidate fee collection pursuant to ILO C181 Article 7.")

        if has_crypto_or_scrip_pay:
            p = self.provisions["ILO_C095_ART3"]
            violations.append(p)
            score -= 40.0
            remedies.append("Convert compensation to official sovereign legal tender pursuant to ILO C95 Article 3.")

        return TreatyComplianceAuditResult(
            is_fully_compliant=(len(violations) == 0),
            violated_provisions=violations,
            international_remedies=remedies if remedies else ["Offer terms conform to international labor treaties."],
            compliance_score=max(0.0, score)
        )
