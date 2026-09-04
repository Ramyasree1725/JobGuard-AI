"""
JobGuard Core Compliance - Statutory Labor Penalties Database Part A
Contains statutory labor codes, criminal penalty limits, and enforcement agencies across global jurisdictions.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class StatutoryPenaltyRecord:
    statute_id: str
    country_code: str
    jurisdiction_level: str
    act_title: str
    section_citation: str
    prohibited_practice: str
    fine_ceiling_usd: float
    custodial_ceiling_months: int
    mandatory_restitution_flag: bool
    enforcement_agency: str
    filing_helpline: str
    filing_portal_url: str


STATUTORY_PENALTIES_A: List[StatutoryPenaltyRecord] = [
    StatutoryPenaltyRecord(
        statute_id="LAW-CAT-A-0001",
        country_code="IN",
        jurisdiction_level="FEDERAL",
        act_title="Information Technology Act, 2000",
        section_citation="Section 66D",
        prohibited_practice="Punishes cheating by personation by using computer resources or communication devices.",
        fine_ceiling_usd=1200.0,
        custodial_ceiling_months=36,
        mandatory_restitution_flag=True,
        enforcement_agency="Ministry of Home Affairs - Indian Cyber Crime Coordination Centre (I4C)",
        filing_helpline="1930 (National Cyber Crime Helpline)",
        filing_portal_url="https://cybercrime.gov.in"
    ),
    StatutoryPenaltyRecord(
        statute_id="LAW-CAT-A-0002",
        country_code="IN",
        jurisdiction_level="FEDERAL",
        act_title="Bharatiya Nyaya Sanhita, 2023",
        section_citation="Section 318(4)",
        prohibited_practice="Cheating and dishonestly inducing delivery of property, valuable security, or money.",
        fine_ceiling_usd=12000.0,
        custodial_ceiling_months=84,
        mandatory_restitution_flag=True,
        enforcement_agency="State Police Cyber Crime Divisions",
        filing_helpline="112 (Emergency Police)",
        filing_portal_url="https://digitalpolice.gov.in"
    ),
    StatutoryPenaltyRecord(
        statute_id="LAW-CAT-A-0003",
        country_code="US",
        jurisdiction_level="FEDERAL",
        act_title="United States Code - Title 18",
        section_citation="18 U.S.C. § 1343 (Wire Fraud)",
        prohibited_practice="Criminalizes schemes to defraud or obtain money by false pretenses transmitted via interstate wire.",
        fine_ceiling_usd=1000000.0,
        custodial_ceiling_months=240,
        mandatory_restitution_flag=True,
        enforcement_agency="Federal Bureau of Investigation (FBI) / Department of Justice",
        filing_helpline="1-800-CALL-FBI",
        filing_portal_url="https://ic3.gov"
    ),
    StatutoryPenaltyRecord(
        statute_id="LAW-CAT-A-0004",
        country_code="US",
        jurisdiction_level="FEDERAL",
        act_title="Federal Trade Commission Act",
        section_citation="15 U.S.C. § 45 (Section 5)",
        prohibited_practice="Prohibits unfair or deceptive acts or practices in commerce, including bogus work-from-home earnings claims.",
        fine_ceiling_usd=50120.0,
        custodial_ceiling_months=0,
        mandatory_restitution_flag=True,
        enforcement_agency="Federal Trade Commission (FTC)",
        filing_helpline="1-877-FTC-HELP",
        filing_portal_url="https://reportfraud.ftc.gov"
    ),
    StatutoryPenaltyRecord(
        statute_id="LAW-CAT-A-0005",
        country_code="GB",
        jurisdiction_level="FEDERAL",
        act_title="Fraud Act 2006",
        section_citation="Section 2 (Fraud by False Representation)",
        prohibited_practice="Criminalizes dishonestly making a false representation with intent to make a financial gain.",
        fine_ceiling_usd=5000000.0,
        custodial_ceiling_months=120,
        mandatory_restitution_flag=True,
        enforcement_agency="Action Fraud & National Fraud Intelligence Bureau (NFIB)",
        filing_helpline="0300 123 2040",
        filing_portal_url="https://actionfraud.police.uk"
    )
]


class StatutoryPenaltyManagerA:
    """Manager class for querying statutory penalties in Part A."""

    def __init__(self):
        self.penalties = {p.statute_id: p for p in STATUTORY_PENALTIES_A}

    def get_by_id(self, statute_id: str) -> Optional[StatutoryPenaltyRecord]:
        return self.penalties.get(statute_id.strip().upper())
