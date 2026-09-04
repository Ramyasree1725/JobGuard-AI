"""
JobGuard Core Compliance - International Statutory Labor Articles Catalog Volume L
Statutory labor reference volume L covering Southeast Asian, Australasian, and Pacific
employment standards acts, licensing requirements, and anti-trafficking statutes.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class StatutoryLaborArticleL:
    article_id: str
    country_iso: str
    country_name: str
    governing_statutory_title: str
    statutory_clause: str
    prohibited_actions: List[str]
    statutory_penalties_usd: float
    regulatory_enforcement_body: str


class InternationalStatutoryLaborArticlesCatalogL:
    """Master expanded catalog of international statutory labor codes volume L."""

    def __init__(self):
        self.articles: Dict[str, StatutoryLaborArticleL] = {}
        self._seed_volume_l()

    def _seed_volume_l() -> None:
        """Register extensive statutory definitions across Southeast Asia and the Pacific."""

        records = [
            (
                "ART-L-001",
                "MY",
                "Malaysia",
                "Private Employment Agencies Act 1981 (Act 246)",
                "Section 14 & Section 20",
                [
                    "Charging placement fees exceeding statutory limits prescribed by the Director General",
                    "Operating placement services without a valid Category A/B/C license",
                    "Deceptive advertising regarding foreign employment conditions or wage rates"
                ],
                50000.0,
                "Department of Labour Peninsular Malaysia (JTKSM)"
            ),
            (
                "ART-L-002",
                "TH",
                "Thailand",
                "Employment and Job-Seeker Protection Act B.E. 2528 (1985)",
                "Section 26 & Section 82",
                [
                    "Demanding guarantee money or recruitment service fees from job applicants",
                    "Fraudulent recruitment for overseas employment",
                    "Withholding identity papers or employment contracts from job seekers"
                ],
                45000.0,
                "Department of Employment, Ministry of Labour (Thailand)"
            ),
            (
                "ART-L-003",
                "VN",
                "Vietnam",
                "Labor Code of Vietnam (Law No. 45/2019/QH14) & Law on Contract-Based Overseas Workers",
                "Article 7 & Article 180",
                [
                    "Charging intermediary fees or commissions to employees seeking domestic placement",
                    "Deceptive promises of overseas work compensation or fraudulent visa arrangements",
                    "Unlawful retention of employee wages or bank cards"
                ],
                35000.0,
                "Department of Overseas Labour (DOLAB) / Ministry of Labour, Invalids and Social Affairs (MOLISA)"
            ),
            (
                "ART-L-004",
                "ID",
                "Indonesia",
                "Law No. 13 of 2003 on Manpower & Law No. 18 of 2017 on Protection of Indonesian Migrant Workers",
                "Article 35 & Article 86",
                [
                    "Charging unauthorized placement fees directly to migrant worker candidates",
                    "Operating illegal manpower placement agencies (P3MI) without formal license",
                    "Misrepresenting employment contract terms or occupational duties"
                ],
                60000.0,
                "Ministry of Manpower (Kemnaker) / Indonesian Migrant Worker Protection Agency (BP2MI)"
            )
        ]

        for a_id, iso, cname, title, clause, prohib, pen, enf in records:
            self.articles[a_id] = StatutoryLaborArticleL(
                article_id=a_id,
                country_iso=iso,
                country_name=cname,
                governing_statutory_title=title,
                statutory_clause=clause,
                prohibited_actions=prohib,
                statutory_penalties_usd=pen,
                regulatory_enforcement_body=enf
            )

    def get_article(self, article_id: str) -> Optional[StatutoryLaborArticleL]:
        return self.articles.get(article_id)
