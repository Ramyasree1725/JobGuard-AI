"""
JobGuard Core Compliance - Global Statutory Labor Penalties Catalog Volume E
Comprehensive legal statutory reference defining maximum civil and criminal penalties,
sentencing guidelines, and statutory damages for employment fraud, advance-fee solicitation,
and deceptive wage theft across global jurisdictions.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class StatutoryJurisdiction(Enum):
    US_FEDERAL = "US_FEDERAL"
    US_CALIFORNIA = "US_CALIFORNIA"
    US_NEW_YORK = "US_NEW_YORK"
    UK_ENGLAND = "UK_ENGLAND"
    EU_GERMANY = "EU_GERMANY"
    EU_FRANCE = "EU_FRANCE"
    AUSTRALIA = "AUSTRALIA"
    CANADA = "CANADA"
    SINGAPORE = "SINGAPORE"
    JAPAN = "JAPAN"


@dataclass
class StatutoryPenaltyEntry:
    statute_code: str
    jurisdiction: StatutoryJurisdiction
    title: str
    legal_reference_citation: str
    max_criminal_prison_years: int
    max_civil_fine_usd: float
    mandatory_restitution_pct: float
    prohibited_conduct_description: str
    enforcement_agency: str


class StatutoryPenaltiesCatalogE:
    """Legal registry of international anti-fraud statutes and criminal sentencing guidelines."""

    def __init__(self):
        self.penalties: Dict[str, StatutoryPenaltyEntry] = {}
        self._initialize_statute_database()

    def _initialize_statute_database(self) -> None:
        """Register statutes covering recruitment and advance fee fraud."""

        self._register_statute(StatutoryPenaltyEntry(
            statute_code="STAT-US-1343",
            jurisdiction=StatutoryJurisdiction.US_FEDERAL,
            title="Federal Wire Fraud via Interstate Electronic Communications",
            legal_reference_citation="18 U.S. Code § 1343",
            max_criminal_prison_years=20,
            max_civil_fine_usd=250000.0,
            mandatory_restitution_pct=100.0,
            prohibited_conduct_description="Transmitting fraudulent job offers, wire transfer demands, or check kickback instructions across state or international telecommunications lines.",
            enforcement_agency="United States Department of Justice (DOJ) / FBI"
        ))

        self._register_statute(StatutoryPenaltyEntry(
            statute_code="STAT-US-1344",
            jurisdiction=StatutoryJurisdiction.US_FEDERAL,
            title="Financial Institution & Check Counterfeiting Fraud",
            legal_reference_citation="18 U.S. Code § 1344",
            max_criminal_prison_years=30,
            max_civil_fine_usd=1000000.0,
            mandatory_restitution_pct=100.0,
            prohibited_conduct_description="Knowingly executing a scheme to defraud a federally insured financial institution by issuing counterfeit employment cashier checks.",
            enforcement_agency="Federal Bureau of Investigation (FBI)"
        ))

        self._register_statute(StatutoryPenaltyEntry(
            statute_code="STAT-US-CA-LC450",
            jurisdiction=StatutoryJurisdiction.US_CALIFORNIA,
            title="Prohibition of Direct or Indirect Employment Consideration Fees",
            legal_reference_citation="California Labor Code § 450",
            max_criminal_prison_years=1,
            max_civil_fine_usd=25000.0,
            mandatory_restitution_pct=200.0,
            prohibited_conduct_description="Requiring an employee or applicant to pay any fee or purchase any item of value as a condition of securing employment.",
            enforcement_agency="California Labor Commissioner's Office (DIR)"
        ))

        self._register_statute(StatutoryPenaltyEntry(
            statute_code="STAT-UK-FRAUD-2006",
            jurisdiction=StatutoryJurisdiction.UK_ENGLAND,
            title="Fraud by False Representation in Recruitment",
            legal_reference_citation="UK Fraud Act 2006, Section 2",
            max_criminal_prison_years=10,
            max_civil_fine_usd=500000.0,
            mandatory_restitution_pct=100.0,
            prohibited_conduct_description="Dishonestly making a false representation intending to make a gain or cause financial loss to a job applicant.",
            enforcement_agency="City of London Police (National Fraud Intelligence Bureau / Action Fraud)"
        ))

        self._register_statute(StatutoryPenaltyEntry(
            statute_code="STAT-EU-GDPR-ART83",
            jurisdiction=StatutoryJurisdiction.EU_GERMANY,
            title="Deceptive PII Harvesting Under False Employment Pretense",
            legal_reference_citation="EU GDPR Article 83(5)",
            max_criminal_prison_years=0,
            max_civil_fine_usd=22000000.0,  # Or 4% of global turnover
            mandatory_restitution_pct=100.0,
            prohibited_conduct_description="Collecting passports, identity credentials, or banking details without valid lawful basis or through deceptive recruitment portals.",
            enforcement_agency="European Data Protection Board (EDPB)"
        ))

        self._register_statute(StatutoryPenaltyEntry(
            statute_code="STAT-AU-CCA-2010",
            jurisdiction=StatutoryJurisdiction.AUSTRALIA,
            title="Misleading Conduct as to Employment & Advance Fees",
            legal_reference_citation="Competition and Consumer Act 2010 (Australian Consumer Law § 31)",
            max_criminal_prison_years=5,
            max_civil_fine_usd=750000.0,
            mandatory_restitution_pct=100.0,
            prohibited_conduct_description="Conduct liable to mislead the public as to the availability, nature, terms, or conditions of employment.",
            enforcement_agency="Australian Competition and Consumer Commission (ACCC)"
        ))

        self._register_statute(StatutoryPenaltyEntry(
            statute_code="STAT-SG-PC-420",
            jurisdiction=StatutoryJurisdiction.SINGAPORE,
            title="Cheating and Dishonestly Inducing Delivery of Property",
            legal_reference_citation="Singapore Penal Code 1871, Section 420",
            max_criminal_prison_years=10,
            max_civil_fine_usd=100000.0,
            mandatory_restitution_pct=100.0,
            prohibited_conduct_description="Deceiving any candidate to deliver property or make payments under false promises of employment.",
            enforcement_agency="Singapore Police Force Commercial Affairs Department (CAD)"
        ))

    def _register_statute(self, entry: StatutoryPenaltyEntry) -> None:
        self.penalties[entry.statute_code] = entry

    def lookup_statute(self, statute_code: str) -> Optional[StatutoryPenaltyEntry]:
        return self.penalties.get(statute_code)

    def get_statutes_by_jurisdiction(self, jurisdiction: StatutoryJurisdiction) -> List[StatutoryPenaltyEntry]:
        return [s for s in self.penalties.values() if s.jurisdiction == jurisdiction]
