"""
JobGuard Core Compliance - International Statutory Labor Articles Catalog Volume J
Comprehensive statutory labor reference catalog volume J covering Central and Eastern European labor codes,
statutory fee prohibitions, and mandatory wage security articles.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class StatutoryLaborArticleJ:
    article_id: str
    country_iso: str
    country_name: str
    statutory_act_title: str
    article_number: str
    mandatory_wage_safeguards: List[str]
    prohibited_recruiter_conduct: List[str]
    maximum_administrative_penalty_eur: float
    regulatory_enforcement_body: str


class InternationalStatutoryLaborArticlesCatalogJ:
    """Master expanded catalog of international statutory labor codes volume J."""

    def __init__(self):
        self.articles: Dict[str, StatutoryLaborArticleJ] = {}
        self._seed_volume_j()

    def _seed_volume_j(self) -> None:
        """Register extensive statutory definitions across Eastern & Central Europe."""

        records = [
            (
                "ART-J-001",
                "PL",
                "Poland",
                "Ustawa o promocji zatrudnienia i instytucjach rynku pracy",
                "Article 19a & Article 85",
                [
                    "Wages must be disbursed in legal tender via bank transfer",
                    "Mandatory written employment contract prior to commencing work",
                    "Employer must provide clear written statement of duties"
                ],
                [
                    "Collecting placement fees or administrative charges from job seekers",
                    "Deducting interview or onboarding costs from wages",
                    "Deceptive advertising regarding foreign employment conditions"
                ],
                30000.0,
                "Państwowa Inspekcja Pracy (National Labour Inspectorate - PIP)"
            ),
            (
                "ART-J-002",
                "CZ",
                "Czech Republic",
                "Zákon o zaměstnanosti (Employment Act No. 435/2004 Coll.)",
                "Section 58 & Section 140",
                [
                    "Direct payment of wage compensation without third-party deductions",
                    "Equal treatment and working condition parity for agency workers"
                ],
                [
                    "Demanding financial compensation or deposits from job applicants",
                    "Operating unlicensed employment mediation services",
                    "Issuing fictitious employment certificates for visa procurement"
                ],
                40000.0,
                "Státní úřad inspekce práce (State Labour Inspection Office)"
            ),
            (
                "ART-J-003",
                "HU",
                "Hungary",
                "2012. évi I. törvény a munka törvénykönyvéről (Labor Code)",
                "Section 154 & Section 215",
                [
                    "Timely payment of wages in Hungarian Forint (HUF) or Euro",
                    "Mandatory employer provision of essential work tools"
                ],
                [
                    "Charging work-seekers for registration, interview, or placement",
                    "Imposing unlawful equipment security withholdings",
                    "Unfair commercial recruitment practices targeting vulnerable workers"
                ],
                25000.0,
                "Foglalkoztatás-felügyeleti Hatóság (Employment Supervisory Authority)"
            ),
            (
                "ART-J-004",
                "RO",
                "Romania",
                "Legea nr. 53/2003 - Codul muncii (Labor Code)",
                "Article 166 & Article 260",
                [
                    "Full disbursement of net salary with official payslip documentation",
                    "Prior written disclosure of job location, hazards, and benefits"
                ],
                [
                    "Conditioning employment on payment of registration or training fees",
                    "Operating fraudulent cross-border labor recruitment schemes",
                    "Withholding candidate identity cards or travel documents"
                ],
                35000.0,
                "Inspecția Muncii (Labour Inspection Directorate)"
            ),
            (
                "ART-J-005",
                "BG",
                "Bulgaria",
                "Кодекс на труда (Labour Code) & Employment Promotion Act",
                "Article 242 & Article 28",
                [
                    "Mandatory guaranteed minimum wage protections",
                    "Strict statutory limits on permissible payroll deductions"
                ],
                [
                    "Charging fees to Bulgarian or foreign work-seekers for placement",
                    "Publishing deceptive advertisements for non-existent overseas jobs",
                    "Unlawful retention of employee wages for equipment purchases"
                ],
                20000.0,
                "Главна инспекция по труда (General Labour Inspectorate Executive Agency)"
            )
        ]

        for a_id, iso, cname, title, art_num, safe, prohib, max_p, enf in records:
            self.articles[a_id] = StatutoryLaborArticleJ(
                article_id=a_id,
                country_iso=iso,
                country_name=cname,
                statutory_act_title=title,
                article_number=art_num,
                mandatory_wage_safeguards=safe,
                prohibited_recruiter_conduct=prohib,
                maximum_administrative_penalty_eur=max_p,
                regulatory_enforcement_body=enf
            )

    def get_article(self, article_id: str) -> Optional[StatutoryLaborArticleJ]:
        return self.articles.get(article_id)
