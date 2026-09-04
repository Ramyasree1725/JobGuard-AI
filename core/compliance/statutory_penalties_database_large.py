"""
JobGuard Core Compliance - Statutory Labor Penalties Large Database
Contains international statutory labor codes, criminal penalties, and enforcement agencies.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class StatutoryPenaltyLargeItem:
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


def build_statutory_large_catalog() -> Dict[str, StatutoryPenaltyLargeItem]:
    catalog: Dict[str, StatutoryPenaltyLargeItem] = {}
    
    # 1
    catalog["LAW-LG-IN-0001"] = StatutoryPenaltyLargeItem(
        statute_id="LAW-LG-IN-0001",
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
    )
    # 2
    catalog["LAW-LG-IN-0002"] = StatutoryPenaltyLargeItem(
        statute_id="LAW-LG-IN-0002",
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
    )
    # 3
    catalog["LAW-LG-US-0001"] = StatutoryPenaltyLargeItem(
        statute_id="LAW-LG-US-0001",
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
    )
    # 4
    catalog["LAW-LG-US-0002"] = StatutoryPenaltyLargeItem(
        statute_id="LAW-LG-US-0002",
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
    )
    # 5
    catalog["LAW-LG-GB-0001"] = StatutoryPenaltyLargeItem(
        statute_id="LAW-LG-GB-0001",
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
    # 6
    catalog["LAW-LG-GB-0002"] = StatutoryPenaltyLargeItem(
        statute_id="LAW-LG-GB-0002",
        country_code="GB",
        jurisdiction_level="FEDERAL",
        act_title="Employment Agencies Act 1973",
        section_citation="Section 6(1)",
        prohibited_practice="Explicitly forbids employment agencies from charging candidates any fee for finding or seeking employment.",
        fine_ceiling_usd=25000.0,
        custodial_ceiling_months=0,
        mandatory_restitution_flag=True,
        enforcement_agency="Employment Agency Standards (EAS) Inspectorate",
        filing_helpline="0845 955 5105",
        filing_portal_url="https://gov.uk/eas"
    )
    # 7
    catalog["LAW-LG-EU-0001"] = StatutoryPenaltyLargeItem(
        statute_id="LAW-LG-EU-0001",
        country_code="EU",
        jurisdiction_level="DIRECTIVE",
        act_title="Directive (EU) 2019/1152 on Transparent Working Conditions",
        section_citation="Article 13 (Mandatory Training)",
        prohibited_practice="Mandatory training must be provided cost-free to the worker and count as working hours.",
        fine_ceiling_usd=100000.0,
        custodial_ceiling_months=0,
        mandatory_restitution_flag=True,
        enforcement_agency="European Labour Authority (ELA)",
        filing_helpline="+32 2 299 11 11",
        filing_portal_url="https://ela.europa.eu"
    )
    # 8
    catalog["LAW-LG-AU-0001"] = StatutoryPenaltyLargeItem(
        statute_id="LAW-LG-AU-0001",
        country_code="AU",
        jurisdiction_level="FEDERAL",
        act_title="Fair Work Act 2009",
        section_citation="Section 325 (Unreasonable Requirements)",
        prohibited_practice="Prohibits employers from directly or indirectly requiring employees to spend any part of their wages.",
        fine_ceiling_usd=93900.0,
        custodial_ceiling_months=0,
        mandatory_restitution_flag=True,
        enforcement_agency="Fair Work Ombudsman (FWO)",
        filing_helpline="13 13 94",
        filing_portal_url="https://fairwork.gov.au"
    )
    # 9
    catalog["LAW-LG-CA-0001"] = StatutoryPenaltyLargeItem(
        statute_id="LAW-LG-CA-0001",
        country_code="CA",
        jurisdiction_level="PROVINCIAL",
        act_title="Employment Standards Act, 2000 (Ontario)",
        section_citation="Section 24 (Temporary Help Agency Fees)",
        prohibited_practice="Prohibits charging fees to individuals for becoming assignment employees or seeking work.",
        fine_ceiling_usd=500000.0,
        custodial_ceiling_months=0,
        mandatory_restitution_flag=True,
        enforcement_agency="Ontario Ministry of Labour",
        filing_helpline="1-800-531-5551",
        filing_portal_url="https://ontario.ca/labour"
    )
    # 10
    catalog["LAW-LG-SG-0001"] = StatutoryPenaltyLargeItem(
        statute_id="LAW-LG-SG-0001",
        country_code="SG",
        jurisdiction_level="FEDERAL",
        act_title="Employment Agencies Act (Cap. 92)",
        section_citation="Section 14 (Placement Fee Caps)",
        prohibited_practice="Strictly caps placement agency fees and prohibits charging unauthorized candidate deposits.",
        fine_ceiling_usd=80000.0,
        custodial_ceiling_months=24,
        mandatory_restitution_flag=True,
        enforcement_agency="Ministry of Manpower Singapore (MOM)",
        filing_helpline="+65 6438 5122",
        filing_portal_url="https://mom.gov.sg"
    )

    return catalog


class StatutoryLargeManager:
    def __init__(self):
        self.catalog = build_statutory_large_catalog()

    def get_by_id(self, stat_id: str) -> Optional[StatutoryPenaltyLargeItem]:
        return self.catalog.get(stat_id)
