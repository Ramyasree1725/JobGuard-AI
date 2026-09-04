"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume AJ
Statutory labor reference volume AJ covering South American Guianas and South Atlantic territories
(Trinidad & Tobago Petroleum Codes, Falkland Islands, Bermuda, Cayman Islands), recruitment licensing, and penalties.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class IslandTerritoryLaborStatuteAJ:
    statute_id: str
    country_iso: str
    territory_name: str
    governing_legislation_title: str
    section_reference: str
    prohibited_conduct_summary: str
    maximum_penalty_usd_equivalent: float
    remedial_measures: List[str]
    enforcing_authority: str


class StatutoryLaborPenaltiesMasterCatalogAJ:
    """Master expanded catalog volume AJ covering Island Territories and offshore financial centers."""

    def __init__(self):
        self.statutes: Dict[str, IslandTerritoryLaborStatuteAJ] = {}
        self._seed_volume_aj()

    def _seed_volume_aj() -> None:
        """Register statutory labor regulations."""

        records = [
            (
                "STAT-AJ-001",
                "BM",
                "Bermuda",
                "Employment Act 2000 & Bermuda Immigration and Protection Act 1956",
                "Section 10 & Section 60",
                "Charging recruitment fees or work permit processing charges directly to foreign or Bermudian employees.",
                35000.0,
                [
                    "Revocation of work permit sponsor certification",
                    "Employment Tribunal restitution orders for full recovery of expenses",
                    "Fines imposed by the Department of Immigration"
                ],
                "Department of Labour (Ministry of Economy and Labour, Bermuda)"
            ),
            (
                "STAT-AJ-002",
                "KY",
                "Cayman Islands",
                "Labour Act (2021 Revision) & Immigration (Transition) Act",
                "Section 15 & Section 68",
                "Operating private employment agencies without a Trade and Business License or charging fees to workers.",
                30000.0,
                [
                    "Cancellation of agency business license by the Trade and Business Licensing Board",
                    "Mandatory refund of all extorted fees to affected workers",
                    "Prosecution in the Summary Court with criminal fines"
                ],
                "Department of Labour & Pensions (WORC Cayman Islands)"
            ),
            (
                "STAT-AJ-003",
                "VG",
                "British Virgin Islands",
                "Labour Code, 2010 (No. 4 of 2010)",
                "Section 22 & Section 156",
                "Demanding or receiving placement fees or commission from employees seeking employment in the Territory.",
                25000.0,
                [
                    "Withdrawal of employment agency registration certificate",
                    "Labour Commissioner compliance directives and restitution orders"
                ],
                "Department of Labour and Workforce Development (British Virgin Islands)"
            ),
            (
                "STAT-AJ-004",
                "GI",
                "Gibraltar",
                "Employment Act (Cap. 54) & Business Trades and Professions (Licensing) Act",
                "Section 12 & Section 48",
                "Operating an unlicensed employment agency or charging placement fees to jobseekers.",
                30000.0,
                [
                    "Revocation of business license by the Business Licensing Authority",
                    "Fines and compensation orders enforced via the Employment Tribunal"
                ],
                "Ministry for Employment (HM Government of Gibraltar)"
            )
        ]

        for s_id, iso, tname, title, sec, prohib, pen, rems, enf in records:
            self.statutes[s_id] = IslandTerritoryLaborStatuteAJ(
                statute_id=s_id,
                country_iso=iso,
                territory_name=tname,
                governing_legislation_title=title,
                section_reference=sec,
                prohibited_conduct_summary=prohib,
                maximum_penalty_usd_equivalent=pen,
                remedial_measures=rems,
                enforcing_authority=enf
            )

    def get_statute(self, statute_id: str) -> Optional[IslandTerritoryLaborStatuteAJ]:
        return self.statutes.get(statute_id)
