"""
JobGuard Core Compliance - International Statutory Labor Articles Catalog Volume K
Comprehensive statutory labor reference catalog volume K covering Middle Eastern,
South Asian, and African labor codes, statutory recruitment fee bans, and worker rights charters.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class StatutoryLaborArticleK:
    article_id: str
    country_iso: str
    country_name: str
    statutory_law_title: str
    article_reference: str
    prohibited_practices: List[str]
    statutory_protections: List[str]
    maximum_penalty_usd: float
    regulatory_ministry: str


class InternationalStatutoryLaborArticlesCatalogK:
    """Master expanded catalog of international statutory labor codes volume K."""

    def __init__(self):
        self.articles: Dict[str, StatutoryLaborArticleK] = {}
        self._seed_volume_k()

    def _seed_volume_k() -> None:
        """Register statutory definitions across MENA, South Asia, and Africa."""

        records = [
            (
                "ART-K-001",
                "AE",
                "United Arab Emirates",
                "Federal Decree-Law No. 33 of 2021 on Regulation of Labour Relations",
                "Article 6 & Article 60",
                [
                    "Charging or collecting recruitment fees or processing expenses from workers",
                    "Withholding official passports or identity cards of foreign employees",
                    "Misrepresenting contract terms or compensation packages in offer letters"
                ],
                [
                    "Wages Protection System (WPS) electronic bank salary transfers",
                    "Mandatory standardized Ministry of Human Resources & Emiratisation (MOHRE) offer letters"
                ],
                275000.0,
                "Ministry of Human Resources & Emiratisation (MOHRE)"
            ),
            (
                "ART-K-002",
                "SA",
                "Saudi Arabia",
                "Saudi Labor Law (Royal Decree No. M/51)",
                "Article 39 & Article 40",
                [
                    "Requiring job applicants or workers to pay recruitment costs or travel fees",
                    "Employing workers under illegal visa trade / free visa schemes",
                    "Unauthorized deductions from employee wages"
                ],
                [
                    "Mudad digital wage protection system compliance",
                    "Qiwa platform electronic employment contract authentication"
                ],
                100000.0,
                "Ministry of Human Resources and Social Development (MHRSD)"
            ),
            (
                "ART-K-003",
                "QA",
                "Qatar",
                "Qatar Labour Law (Law No. 14 of 2004)",
                "Article 33 & Article 66",
                [
                    "Collecting placement fees or commissions from overseas job seekers",
                    "Deducting visa processing fees from candidate remuneration",
                    "Operating fraudulent labor recruitment offices"
                ],
                [
                    "Mandatory Wage Protection System (WPS) bank monitoring",
                    "Qatar Visa Centre (QVC) pre-departure electronic contract signing"
                ],
                150000.0,
                "Ministry of Labour (MOL Qatar)"
            ),
            (
                "ART-K-004",
                "IN",
                "India",
                "Emigration Act, 1983 & Occupational Safety, Health and Working Conditions Code",
                "Section 10 & Section 24",
                [
                    "Unregistered recruitment agencies charging placement fees exceeding statutory cap",
                    "Publishing fraudulent overseas job offers or issuing forged visa papers",
                    "Operating task optimization crypto schemes masquerading as data entry work"
                ],
                [
                    "eMigrate system registered recruiting agent verification",
                    "Mandatory Pravasi Bharatiya Bima Yojana (PBBY) insurance protection"
                ],
                50000.0,
                "Ministry of External Affairs (MEA) - Protector General of Emigrants (PGE)"
            ),
            (
                "ART-K-005",
                "PH",
                "Philippines",
                "Migrant Workers and Overseas Filipinos Act (Republic Act No. 8042 / RA 10022)",
                "Section 6 (Illegal Recruitment)",
                [
                    "Charging placement fees to seafarers and landbased workers in violation of POEA rules",
                    "Publishing false job vacancies or issuing fictitious work contracts",
                    "Obstructing victim complaints or engaging in recruitment fraud syndicates"
                ],
                [
                    "Department of Migrant Workers (DMW) verified contract certification",
                    "Compulsory insurance coverage for overseas Filipino workers (OFWs)"
                ],
                200000.0,
                "Department of Migrant Workers (DMW) / Department of Justice (DOJ)"
            )
        ]

        for a_id, iso, cname, title, art_ref, prohib, safe, max_p, enf in records:
            self.articles[a_id] = StatutoryLaborArticleK(
                article_id=a_id,
                country_iso=iso,
                country_name=cname,
                statutory_law_title=title,
                article_reference=art_ref,
                prohibited_practices=prohib,
                statutory_protections=safe,
                maximum_penalty_usd=max_p,
                regulatory_ministry=enf
            )

    def get_article(self, article_id: str) -> Optional[StatutoryLaborArticleK]:
        return self.articles.get(article_id)
