"""
JobGuard Core Compliance - Statutory Labor Penalties Database Part D
Contains statutory labor codes, criminal penalty limits, and enforcement agencies across global jurisdictions.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from core.compliance.statutory_penalty_catalog_a import StatutoryPenaltyRecord


STATUTORY_PENALTIES_D: List[StatutoryPenaltyRecord] = [
    StatutoryPenaltyRecord(
        statute_id="LAW-CAT-D-0001",
        country_code="JP",
        jurisdiction_level="FEDERAL",
        act_title="Japanese Penal Code & Employment Security Act",
        section_citation="Article 246 (Fraud) & Article 32-3",
        prohibited_practice="Prohibits collecting recruitment fees from job seekers and penalizes employment fraud.",
        fine_ceiling_usd=1000000.0,
        custodial_ceiling_months=120,
        mandatory_restitution_flag=True,
        enforcement_agency="Ministry of Health, Labour and Welfare (MHLW)",
        filing_helpline="+81 3-5253-1111",
        filing_portal_url="https://mhlw.go.jp"
    ),
    StatutoryPenaltyRecord(
        statute_id="LAW-CAT-D-0002",
        country_code="NZ",
        jurisdiction_level="FEDERAL",
        act_title="New Zealand Crimes Act 1961 & Employment Relations Act 2000",
        section_citation="Section 240 (Obtaining by Deception)",
        prohibited_practice="Criminalizes obtaining property, service, or pecuniary advantage by deception.",
        fine_ceiling_usd=500000.0,
        custodial_ceiling_months=84,
        mandatory_restitution_flag=True,
        enforcement_agency="Employment New Zealand / MBIE",
        filing_helpline="0800 20 90 20",
        filing_portal_url="https://employment.govt.nz"
    ),
    StatutoryPenaltyRecord(
        statute_id="LAW-CAT-D-0003",
        country_code="IE",
        jurisdiction_level="FEDERAL",
        act_title="Criminal Justice (Theft and Fraud Offences) Act 2001 (Ireland)",
        section_citation="Section 6 (Deception)",
        prohibited_practice="Dishonestly inducing another to act on false pretenses to obtain gain or cause loss.",
        fine_ceiling_usd=1000000.0,
        custodial_ceiling_months=60,
        mandatory_restitution_flag=True,
        enforcement_agency="Workplace Relations Commission (WRC)",
        filing_helpline="0818 80 80 90",
        filing_portal_url="https://workplacerelations.ie"
    ),
    StatutoryPenaltyRecord(
        statute_id="LAW-CAT-D-0004",
        country_code="IL",
        jurisdiction_level="FEDERAL",
        act_title="Israeli Penal Law, 5737-1977 & Employment Service Law",
        section_citation="Section 415 (Obtaining by Fraud)",
        prohibited_practice="Prohibits charging job placement fees to candidates and penalizes recruitment fraud.",
        fine_ceiling_usd=750000.0,
        custodial_ceiling_months=36,
        mandatory_restitution_flag=True,
        enforcement_agency="Ministry of Economy and Industry",
        filing_helpline="*6106",
        filing_portal_url="https://gov.il/economy"
    ),
    StatutoryPenaltyRecord(
        statute_id="LAW-CAT-D-0005",
        country_code="AE",
        jurisdiction_level="FEDERAL",
        act_title="UAE Federal Decree-Law No. 33 of 2021 (Labour Law)",
        section_citation="Article 6 (Prohibition of Charging Recruitment Fees)",
        prohibited_practice="Strictly prohibits charging any fee or cost to workers directly or indirectly for recruitment.",
        fine_ceiling_usd=270000.0,
        custodial_ceiling_months=0,
        mandatory_restitution_flag=True,
        enforcement_agency="Ministry of Human Resources and Emiratisation (MOHRE)",
        filing_helpline="600 590000",
        filing_portal_url="https://mohre.gov.ae"
    )
]


class StatutoryPenaltyManagerD:
    """Manager class for querying statutory penalties in Part D."""

    def __init__(self):
        self.penalties = {p.statute_id: p for p in STATUTORY_PENALTIES_D}

    def get_by_id(self, statute_id: str) -> Optional[StatutoryPenaltyRecord]:
        return self.penalties.get(statute_id.strip().upper())
