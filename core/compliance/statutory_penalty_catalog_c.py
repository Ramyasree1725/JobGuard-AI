"""
JobGuard Core Compliance - Statutory Labor Penalties Database Part C
Contains statutory labor codes, criminal penalty limits, and enforcement agencies across global jurisdictions.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from core.compliance.statutory_penalty_catalog_a import StatutoryPenaltyRecord


STATUTORY_PENALTIES_C: List[StatutoryPenaltyRecord] = [
    StatutoryPenaltyRecord(
        statute_id="LAW-CAT-C-0001",
        country_code="DE",
        jurisdiction_level="FEDERAL",
        act_title="German Civil Code (BGB) & Criminal Code (StGB)",
        section_citation="Section 263 StGB (Fraud)",
        prohibited_practice="Punishes obtaining pecuniary advantage through false pretenses or deception.",
        fine_ceiling_usd=1000000.0,
        custodial_ceiling_months=60,
        mandatory_restitution_flag=True,
        enforcement_agency="Federal Criminal Police Office (BKA)",
        filing_helpline="+49 611 55-0",
        filing_portal_url="https://bka.de"
    ),
    StatutoryPenaltyRecord(
        statute_id="LAW-CAT-C-0002",
        country_code="FR",
        jurisdiction_level="FEDERAL",
        act_title="French Labour Code (Code du travail)",
        section_citation="Article L3121-1 & L8221-1",
        prohibited_practice="Prohibits fraudulent undeclared recruitment schemes and unlawful fee deductions.",
        fine_ceiling_usd=500000.0,
        custodial_ceiling_months=36,
        mandatory_restitution_flag=True,
        enforcement_agency="Labour Inspectorate (Inspection du Travail)",
        filing_helpline="3939",
        filing_portal_url="https://travail-emploi.gouv.fr"
    ),
    StatutoryPenaltyRecord(
        statute_id="LAW-CAT-C-0003",
        country_code="NL",
        jurisdiction_level="FEDERAL",
        act_title="Dutch Criminal Code (Wetboek van Strafrecht)",
        section_citation="Article 326 (Oplichting)",
        prohibited_practice="Prohibits inducing individuals to part with money or goods via fabricated names or deception.",
        fine_ceiling_usd=800000.0,
        custodial_ceiling_months=48,
        mandatory_restitution_flag=True,
        enforcement_agency="Netherlands Labour Authority (NLA)",
        filing_helpline="0800-5151",
        filing_portal_url="https://nllabourauthority.nl"
    ),
    StatutoryPenaltyRecord(
        statute_id="LAW-CAT-C-0004",
        country_code="CH",
        jurisdiction_level="FEDERAL",
        act_title="Swiss Criminal Code (StGB)",
        section_citation="Article 146 (Betrug)",
        prohibited_practice="Malicious deception leading to financial injury and unlawful self-enrichment.",
        fine_ceiling_usd=1000000.0,
        custodial_ceiling_months=60,
        mandatory_restitution_flag=True,
        enforcement_agency="Federal Office of Police (fedpol)",
        filing_helpline="+41 58 463 11 23",
        filing_portal_url="https://fedpol.admin.ch"
    ),
    StatutoryPenaltyRecord(
        statute_id="LAW-CAT-C-0005",
        country_code="SE",
        jurisdiction_level="FEDERAL",
        act_title="Swedish Penal Code (Brottsbalken)",
        section_citation="Chapter 9 Section 1 (Bedrageri)",
        prohibited_practice="Inducing action or omission through deceptive representation resulting in financial loss.",
        fine_ceiling_usd=600000.0,
        custodial_ceiling_months=24,
        mandatory_restitution_flag=True,
        enforcement_agency="Swedish Work Environment Authority (Arbetsmiljoverket)",
        filing_helpline="+46 10 730 90 00",
        filing_portal_url="https://av.se"
    )
]


class StatutoryPenaltyManagerC:
    """Manager class for querying statutory penalties in Part C."""

    def __init__(self):
        self.penalties = {p.statute_id: p for p in STATUTORY_PENALTIES_C}

    def get_by_id(self, statute_id: str) -> Optional[StatutoryPenaltyRecord]:
        return self.penalties.get(statute_id.strip().upper())
