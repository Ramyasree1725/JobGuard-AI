"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume O
Statutory labor reference volume O covering Australian state and territory workplace relations laws
(New South Wales, Victoria, Queensland, Western Australia), recruitment licensing, and penalties.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class AustralianStateStatuteO:
    statute_id: str
    state_code: str
    state_name: str
    act_title: str
    section_citation: str
    prohibited_conduct: str
    maximum_penalty_aud: float
    civil_remedy_provisions: str
    enforcing_authority: str


class StatutoryLaborPenaltiesMasterCatalogO:
    """Master expanded catalog volume O covering Australian state and territorial labor legislation."""

    def __init__(self):
        self.statutes: Dict[str, AustralianStateStatuteO] = {}
        self._seed_volume_o()

    def _seed_volume_o() -> None:
        """Register Australian state labor statutes."""

        records = [
            (
                "STAT-O-001",
                "AU_NSW",
                "New South Wales",
                "Fair Trading Act 1987 (NSW) & Industrial Relations Act 1996",
                "Section 32 & Section 381",
                "Misleading representations concerning employment availability, terms, or conditions, and charging unauthorized placement fees.",
                1100000.0,
                "Injunctions, mandatory refunds, and compensation orders for victim economic loss.",
                "NSW Fair Trading / Industrial Relations Commission of NSW"
            ),
            (
                "STAT-O-002",
                "AU_VIC",
                "Victoria",
                "Labour Hire Licensing Act 2018 (Vic)",
                "Section 13 & Section 14",
                "Operating labor hire or recruitment services without a valid license, or demanding prohibited fees from workers.",
                600000.0,
                "Substantial civil penalties for providers and hosts utilizing unlicensed labor hire services.",
                "Labour Hire Authority Victoria (LHA)"
            ),
            (
                "STAT-O-003",
                "AU_QLD",
                "Queensland",
                "Labour Hire Licensing Act 2017 (Qld) & Private Employment Agents Act 2005",
                "Section 10 & Section 11",
                "Private employment agents charging work-seekers any fee for finding or attempting to find work.",
                450000.0,
                "Prosecution in Queensland Industrial Relations Commission and full fee refund orders.",
                "Office of Industrial Relations Queensland (Labour Hire Licensing Compliance Unit)"
            ),
            (
                "STAT-O-004",
                "AU_WA",
                "Western Australia",
                "Employment Agents Act 1976 (WA)",
                "Section 42 & Section 48",
                "Demanding or receiving fees from employees or candidates for securing employment.",
                250000.0,
                "Fines, cancellation of employment agent license, and court-ordered restitution.",
                "Department of Energy, Mines, Industry Regulation and Safety (Consumer Protection WA)"
            ),
            (
                "STAT-O-005",
                "AU_SA",
                "South Australia",
                "Labour Hire Licensing Act 2017 (SA)",
                "Section 11 & Section 12",
                "Operating unlicensed labor hire or recruitment services, or extracting placement fees from candidates.",
                400000.0,
                "Civil penalties and restitution orders enforced via South Australian Employment Tribunal (SAET).",
                "Consumer and Business Services (CBS South Australia)"
            )
        ]

        for s_id, scode, sname, act, sec, prohib, pen, rest, auth in records:
            self.statutes[s_id] = AustralianStateStatuteO(
                statute_id=s_id,
                state_code=scode,
                state_name=sname,
                act_title=act,
                section_citation=sec,
                prohibited_conduct=prohib,
                maximum_penalty_aud=pen,
                civil_remedy_provisions=rest,
                enforcing_authority=auth
            )

    def get_statute(self, statute_id: str) -> Optional[AustralianStateStatuteO]:
        return self.statutes.get(statute_id)
