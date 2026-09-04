"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume X
Statutory labor reference volume X covering Central Asian and Asia-Pacific labor codes
(Kazakhstan, Uzbekistan, New Zealand, Fiji), recruitment licensing standards, and penalties.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class AsiaPacificCentralAsiaStatuteX:
    statute_id: str
    country_iso: str
    country_name: str
    statutory_act_title: str
    article_reference: str
    prohibited_recruitment_practice: str
    maximum_penalty_usd: float
    remedial_measures: List[str]
    enforcement_ministry: str


class StatutoryLaborPenaltiesMasterCatalogX:
    """Master expanded catalog volume X covering Asia-Pacific and Central Asian labor legislation."""

    def __init__(self):
        self.statutes: Dict[str, AsiaPacificCentralAsiaStatuteX] = {}
        self._seed_volume_x()

    def _seed_volume_x() -> None:
        """Register statutory labor regulations."""

        records = [
            (
                "STAT-X-001",
                "NZ",
                "New Zealand",
                "Employment Relations Act 2000 & Fair Trading Act 1986",
                "Section 142 & Section 40",
                "Charging premiums or fees to jobseekers for securing employment, or making misleading job representations.",
                600000.0,  # NZD 600K
                [
                    "Penalties ordered by Employment Relations Authority (ERA) or Employment Court",
                    "Mandatory refund of all premiums paid by job seekers with interest",
                    "Public warning notices issued by Labour Inspectorate"
                ],
                "Ministry of Business, Innovation and Employment (MBIE - Labour Inspectorate NZ)"
            ),
            (
                "STAT-X-002",
                "KZ",
                "Kazakhstan",
                "Labour Code of the Republic of Kazakhstan & Law on Migration",
                "Article 15 & Article 55",
                "Charging fees to citizens of Kazakhstan for job placement abroad without accreditation.",
                35000.0,
                [
                    "Revocation of license for private employment agencies",
                    "Administrative fines on officials and legal entities"
                ],
                "Ministry of Labour and Social Protection of the Population of the Republic of Kazakhstan"
            ),
            (
                "STAT-X-003",
                "UZ",
                "Uzbekistan",
                "Law of the Republic of Uzbekistan on Private Employment Agencies (No. ZRU-501)",
                "Article 13 & Article 22",
                "Charging fees from jobseekers for employment abroad (services must be paid exclusively by foreign employers).",
                30000.0,
                [
                    "Immediate revocation of private employment agency license",
                    "Forfeiture of statutory guarantee deposit fund placed with Ministry"
                ],
                "Ministry of Poverty Alleviation and Employment of the Republic of Uzbekistan"
            ),
            (
                "STAT-X-004",
                "FJ",
                "Fiji",
                "Employment Relations Act 2007",
                "Section 21 & Section 256",
                "Operating an employment agency without registration or demanding unlawful fees from workers.",
                20000.0,
                [
                    "Fines and cancellation of recruitment agency permit",
                    "Orders by the Employment Relations Tribunal for full restitution"
                ],
                "Ministry of Employment, Productivity and Industrial Relations (Fiji)"
            )
        ]

        for s_id, iso, cname, title, art, prohib, pen, rems, enf in records:
            self.statutes[s_id] = AsiaPacificCentralAsiaStatuteX(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statutory_act_title=title,
                article_reference=art,
                prohibited_recruitment_practice=prohib,
                maximum_penalty_usd=pen,
                remedial_measures=rems,
                enforcement_ministry=enf
            )

    def get_statute(self, statute_id: str) -> Optional[AsiaPacificCentralAsiaStatuteX]:
        return self.statutes.get(statute_id)
