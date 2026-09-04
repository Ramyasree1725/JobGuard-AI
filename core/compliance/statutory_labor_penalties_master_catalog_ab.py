"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume AB
Statutory labor reference volume AB covering South Asian regional labor standards
(Bangladesh, Sri Lanka, Nepal, Pakistan), overseas recruitment licensing acts, and worker protection codes.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class SouthAsianLaborStatuteAB:
    statute_id: str
    country_iso: str
    country_name: str
    statutory_act_title: str
    section_reference: str
    prohibited_conduct_summary: str
    penalty_usd_equivalent: float
    remedial_measures: List[str]
    enforcing_ministry: str


class StatutoryLaborPenaltiesMasterCatalogAB:
    """Master expanded catalog volume AB covering South Asian statutory labor codes."""

    def __init__(self):
        self.statutes: Dict[str, SouthAsianLaborStatuteAB] = {}
        self._seed_volume_ab()

    def _seed_volume_ab() -> None:
        """Register South Asian statutory labor regulations."""

        records = [
            (
                "STAT-AB-001",
                "BD",
                "Bangladesh",
                "Overseas Employment and Migrants Act, 2013 (Act No. XLVIII of 2013)",
                "Section 19 & Section 31",
                "Charging recruitment fees or migration costs to overseas jobseekers exceeding maximum government statutory caps.",
                35000.0,
                [
                    "Cancellation of recruiting agency license by the Licensing Authority",
                    "Rigorous imprisonment for a term up to 7 years and fine up to 500,000 BDT",
                    "Full compensation and repatriation cost recovery from agency security bond"
                ],
                "Bureau of Manpower, Employment and Training (BMET / Ministry of Expatriates' Welfare)"
            ),
            (
                "STAT-AB-002",
                "LK",
                "Sri Lanka",
                "Sri Lanka Bureau of Foreign Employment Act (No. 21 of 1985)",
                "Section 62 & Section 67",
                "Carrying on business as a foreign employment agency without a valid license or charging unauthorized candidate fees.",
                30000.0,
                [
                    "Cancellation of the foreign employment agency license",
                    "Forfeiture of bank guarantee furnished to the Bureau",
                    "Criminal prosecution in the Magistrates Court with mandatory compensation orders"
                ],
                "Sri Lanka Bureau of Foreign Employment (SLBFE)"
            ),
            (
                "STAT-AB-003",
                "NP",
                "Nepal",
                "Foreign Employment Act, 2064 (2007)",
                "Section 10 & Section 43",
                "Collecting fees or money from foreign employment candidates without issuing official receipts or charging excess amounts.",
                25000.0,
                [
                    "Revocation of the agency's operating license and confiscation of cash deposit",
                    "Imprisonment for a term from 3 to 7 years and fine of 300,000 to 500,000 NPR",
                    "Full refund of collected money plus 50% statutory penalty interest"
                ],
                "Department of Foreign Employment (DOFE Nepal / Ministry of Labour)"
            ),
            (
                "STAT-AB-004",
                "PK",
                "Pakistan",
                "Emigration Ordinance, 1979 & Rules (XVIII of 1979)",
                "Section 17 & Section 24",
                "Charging unauthorized fees, publishing fraudulent overseas job advertisements, or operating without an Overseas Employment Promoter (OEP) license.",
                40000.0,
                [
                    "Cancellation of OEP license and forfeiture of security deposit",
                    "Imprisonment up to 14 years and fine prosecuted under Special Court of Emigration",
                    "Mandatory restitution of all extorted funds to victims"
                ],
                "Bureau of Emigration and Overseas Employment (BEOE / Ministry of Overseas Pakistanis)"
            )
        ]

        for s_id, iso, cname, title, sec, prohib, pen, rems, enf in records:
            self.statutes[s_id] = SouthAsianLaborStatuteAB(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statutory_act_title=title,
                section_reference=sec,
                prohibited_conduct_summary=prohib,
                penalty_usd_equivalent=pen,
                remedial_measures=rems,
                enforcing_ministry=enf
            )

    def get_statute(self, statute_id: str) -> Optional[SouthAsianLaborStatuteAB]:
        return self.statutes.get(statute_id)
