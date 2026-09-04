"""
JobGuard Core Compliance - Statutory Penalties Master Catalog Volume I
Contains detailed legal definitions, civil restitution multipliers, and international
criminal penalties for deceptive recruitment, visa fraud, and identity conversion.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class StatutoryPenaltiesEntryI:
    statute_id: str
    jurisdiction_code: str
    statutory_name: str
    code_citation: str
    prohibited_conduct_detail: str
    civil_penalty_usd: float
    maximum_prison_term_years: int
    mandatory_restitution_clause: str
    enforcement_authority: str


class StatutoryPenaltiesCatalogVolumeI:
    """Master expanded catalog volume I of statutory penalties for fraudulent employment."""

    def __init__(self):
        self.entries: Dict[str, StatutoryPenaltiesEntryI] = {}
        self._seed_volume_i()

    def _seed_volume_i(self) -> None:
        """Register extensive statutory definitions."""

        data = [
            (
                "STAT-I-001",
                "US_FEDERAL",
                "Computer Fraud and Abuse Act (CFAA) § 1030(a)(4)",
                "18 U.S.C. § 1030(a)(4)",
                "Knowingly and with intent to defraud accessing a protected computer without authorization to further an employment fraud scheme.",
                250000.0,
                5,
                "Mandatory restitution for all victim forensic and recovery costs under 18 U.S.C. § 3663A.",
                "Federal Bureau of Investigation (FBI) / U.S. Secret Service"
            ),
            (
                "STAT-I-002",
                "US_FEDERAL",
                "Identity Theft Penalty Enhancement Act",
                "18 U.S.C. § 1028A",
                "Aggravated identity theft in relation to wire fraud (e.g. using stolen candidate SSN or executive name to execute scams).",
                250000.0,
                2,  # Mandatory consecutive 2 years
                "Consecutive mandatory 2-year prison sentence on top of underlying wire fraud sentence.",
                "U.S. Department of Justice (DOJ)"
            ),
            (
                "STAT-I-003",
                "US_FEDERAL",
                "Immigration and Nationality Act (INA) § 274C",
                "8 U.S.C. § 1324c",
                "Document fraud involving counterfeit visa sponsorship appointment letters or falsified employer certifications.",
                10000.0,
                15,
                "Civil money penalties for each document forged plus mandatory deportation/debarment.",
                "U.S. Immigration and Customs Enforcement (ICE) / HSI"
            ),
            (
                "STAT-I-004",
                "US_FEDERAL",
                "Federal Anti-Kickback Enforcement Act",
                "41 U.S.C. § 8702",
                "Prohibition on kickbacks, fee payments, or financial compensation for employment referrals on government contracts.",
                100000.0,
                10,
                "Civil penalties equal to twice the amount of the kickback plus $10,000 per occurrence.",
                "Department of Defense OIG / DOJ"
            ),
            (
                "STAT-I-005",
                "US_CALIFORNIA",
                "California Private Attorneys General Act (PAGA)",
                "Cal. Lab. Code § 2698 et seq.",
                "Aggrieved employees and applicants bringing civil action for systemic labor code and fee deduction violations.",
                200.0,  # Per employee per pay period
                0,
                "75% of civil penalties distributed to Labor and Workforce Development Agency, 25% to aggrieved workers.",
                "California Labor and Workforce Development Agency (LWDA)"
            )
        ]

        for s_id, jur, s_name, cit, cond, fine, prison, rest, enf in data:
            self.entries[s_id] = StatutoryPenaltiesEntryI(
                statute_id=s_id,
                jurisdiction_code=jur,
                statutory_name=s_name,
                code_citation=cit,
                prohibited_conduct_detail=cond,
                civil_penalty_usd=fine,
                maximum_prison_term_years=prison,
                mandatory_restitution_clause=rest,
                enforcement_authority=enf
            )

    def get_entry(self, statute_id: str) -> Optional[StatutoryPenaltiesEntryI]:
        return self.entries.get(statute_id)
