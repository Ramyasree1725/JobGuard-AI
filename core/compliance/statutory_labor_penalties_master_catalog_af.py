"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume AF
Statutory labor reference volume AF covering Caribbean Community (CARICOM) regional labor standards
(Guyana, Suriname, Belize, Barbados, Saint Lucia), recruitment licensing acts, and worker protection codes.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class CaricomLaborStatuteAF:
    statute_id: str
    country_iso: str
    country_name: str
    statutory_law_title: str
    section_reference: str
    prohibited_conduct_summary: str
    maximum_penalty_usd_equivalent: float
    remedial_measures: List[str]
    enforcing_ministry: str


class StatutoryLaborPenaltiesMasterCatalogAF:
    """Master expanded catalog volume AF covering CARICOM regional statutory labor codes."""

    def __init__(self):
        self.statutes: Dict[str, CaricomLaborStatuteAF] = {}
        self._seed_volume_af()

    def _seed_volume_af() -> None:
        """Register CARICOM statutory labor regulations."""

        records = [
            (
                "STAT-AF-001",
                "GY",
                "Guyana",
                "Employment of Young Persons and Children Act & Labour Act (Cap. 98:01)",
                "Section 8 & Section 42",
                "Demanding consideration or charging fees to workers for job placement, or publishing fraudulent recruitment adverts.",
                25000.0,
                [
                    "Prosecution in the Magistrates' Court and summary conviction fines",
                    "Mandatory refund of all extorted fees to affected work-seekers",
                    "Cancellation of recruiter or employment agency operating permit"
                ],
                "Ministry of Labour (Co-operative Republic of Guyana)"
            ),
            (
                "STAT-AF-002",
                "SR",
                "Suriname",
                "Arbeidswetgeving & Wet Arbeidsbemiddeling (Employment Mediation Act)",
                "Article 12 & Article 29",
                "Collecting fees or charging commissions to jobseekers for domestic or overseas employment mediation.",
                20000.0,
                [
                    "Withdrawal of the private employment agency license by the Ministry",
                    "Administrative penalties imposed by the Labour Inspection Directorate (Arbeidsinspectie)"
                ],
                "Ministerie van Arbeid, Werkgelegenheid en Jeugdzaken (AWJ Suriname)"
            ),
            (
                "STAT-AF-003",
                "BZ",
                "Belize",
                "Labour Act (Chapter 297 of the Laws of Belize)",
                "Section 48 & Section 182",
                "Operating private employment recruitment agencies without statutory license or charging prohibited fees to workers.",
                25000.0,
                [
                    "Immediate closure of recruitment office and forfeiture of security deposit",
                    "Labour Commissioner compliance orders for full restitution"
                ],
                "Ministry of Rural Transformation, Community Development, Labour and Local Government (Belize)"
            ),
            (
                "STAT-AF-004",
                "BB",
                "Barbados",
                "Employment Rights Act, 2012 & Recruiting of Workers Act",
                "Section 6 & Section 24",
                "Charging fees or recruitment expenses to workers seeking employment or overseas placement.",
                30000.0,
                [
                    "Revocation of recruiter's permit and proceedings before the Employment Rights Tribunal (ERT)",
                    "Full repayment orders enforceable as High Court judgments"
                ],
                "Ministry of Labour, Social Security and Third Sector (Barbados)"
            ),
            (
                "STAT-AF-005",
                "LC",
                "Saint Lucia",
                "Labour Act (Cap. 16.04 of the Revised Laws of Saint Lucia)",
                "Section 35 & Section 410",
                "Private employment agencies demanding registration or placement fees from job applicants.",
                20000.0,
                [
                    "Cancellation of agency registration",
                    "Fines and mandatory reimbursement enforced by the Department of Labour"
                ],
                "Department of Labour (Saint Lucia)"
            )
        ]

        for s_id, iso, cname, title, sec, prohib, pen, rems, enf in records:
            self.statutes[s_id] = CaricomLaborStatuteAF(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statutory_law_title=title,
                section_reference=sec,
                prohibited_conduct_summary=prohib,
                maximum_penalty_usd_equivalent=pen,
                remedial_measures=rems,
                enforcing_ministry=enf
            )

    def get_statute(self, statute_id: str) -> Optional[CaricomLaborStatuteAF]:
        return self.statutes.get(statute_id)
