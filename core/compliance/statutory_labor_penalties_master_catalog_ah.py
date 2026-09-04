"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume AH
Statutory labor reference volume AH covering Southeast Asian & Oceanic Island jurisdictions
(Papua New Guinea, Solomon Islands, Vanuatu, Samoa, Tonga), employment acts, and recruiter penalties.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class PacificIslandLaborStatuteAH:
    statute_id: str
    country_iso: str
    country_name: str
    statutory_law_title: str
    section_citation: str
    prohibited_recruitment_conduct: str
    penalty_usd_equivalent: float
    remedial_measures: List[str]
    enforcing_department: str


class StatutoryLaborPenaltiesMasterCatalogAH:
    """Master expanded catalog volume AH covering Pacific Island statutory labor codes."""

    def __init__(self):
        self.statutes: Dict[str, PacificIslandLaborStatuteAH] = {}
        self._seed_volume_ah()

    def _seed_volume_ah() -> None:
        """Register Pacific Island statutory labor regulations."""

        records = [
            (
                "STAT-AH-001",
                "PG",
                "Papua New Guinea",
                "Employment Act 1978 & Employment of Non-Citizens Act",
                "Section 18 & Section 142",
                "Operating private employment placement services without a permit or charging placement fees to jobseekers.",
                25000.0,
                [
                    "Prosecution in the National Court of Papua New Guinea",
                    "Mandatory refund of all fees paid with statutory interest",
                    "Cancellation of labor agency operating permit"
                ],
                "Department of Labour and Industrial Relations (DLIR PNG)"
            ),
            (
                "STAT-AH-002",
                "SB",
                "Solomon Islands",
                "Labour Act (Cap. 73) & Labour (Recruiting of Workers) Rules",
                "Section 12 & Section 38",
                "Recruiting workers or charging commissions to job applicants without a statutory recruiter's permit.",
                20000.0,
                [
                    "Revocation of recruiter's license by the Commissioner of Labour",
                    "Fines and compensation orders enforced by the Magistrates Court"
                ],
                "Ministry of Commerce, Industry, Labour and Immigration (Solomon Islands)"
            ),
            (
                "STAT-AH-003",
                "VU",
                "Vanuatu",
                "Employment Act (Cap. 160) & Seasonal Employment Regulations",
                "Section 10 & Section 72",
                "Charging fees or demanding money from citizens of Vanuatu for seasonal or domestic employment placement.",
                25000.0,
                [
                    "Cancellation of seasonal worker recruitment agent license",
                    "Forfeiture of performance security bond deposited with Department of Labour"
                ],
                "Department of Labour (Ministry of Internal Affairs, Vanuatu)"
            ),
            (
                "STAT-AH-004",
                "WS",
                "Samoa",
                "Labour and Employment Relations Act 2013",
                "Section 22 & Section 65",
                "Private employment agents charging fees to work-seekers for finding or securing employment.",
                20000.0,
                [
                    "Immediate withdrawal of private employment agent accreditation",
                    "Court orders for full restitution of extorted amounts"
                ],
                "Ministry of Commerce, Industry and Labour (MCIL Samoa)"
            ),
            (
                "STAT-AH-005",
                "TO",
                "Tonga",
                "Employment Relations Act 2020",
                "Section 14 & Section 50",
                "Demanding or receiving payment from jobseekers for employment placement or recruitment services.",
                20000.0,
                [
                    "Revocation of recruiting agent license",
                    "Fines enforced by the Ministry of Trade and Economic Development"
                ],
                "Ministry of Trade and Economic Development (Labour Division, Tonga)"
            )
        ]

        for s_id, iso, cname, title, sec, prohib, pen, rems, enf in records:
            self.statutes[s_id] = PacificIslandLaborStatuteAH(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statutory_law_title=title,
                section_citation=sec,
                prohibited_recruitment_conduct=prohib,
                penalty_usd_equivalent=pen,
                remedial_measures=rems,
                enforcing_department=enf
            )

    def get_statute(self, statute_id: str) -> Optional[PacificIslandLaborStatuteAH]:
        return self.statutes.get(statute_id)
