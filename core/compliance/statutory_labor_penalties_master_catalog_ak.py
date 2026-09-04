"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume AK
Statutory labor reference volume AK covering South Caucasus and Black Sea region labor standards
(Armenia, Azerbaijan, Georgia, Turkey), recruitment agency licensing, and worker protections.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class BlackSeaCaucasusLaborStatuteAK:
    statute_id: str
    country_iso: str
    country_name: str
    statutory_law_title: str
    article_citation: str
    prohibited_conduct_summary: str
    maximum_penalty_usd_equivalent: float
    administrative_remedies: List[str]
    enforcing_ministry: str


class StatutoryLaborPenaltiesMasterCatalogAK:
    """Master expanded catalog volume AK covering Black Sea and South Caucasus labor legislation."""

    def __init__(self):
        self.statutes: Dict[str, BlackSeaCaucasusLaborStatuteAK] = {}
        self._seed_volume_ak()

    def _seed_volume_ak() -> None:
        """Register statutory labor regulations."""

        records = [
            (
                "STAT-AK-001",
                "AM",
                "Armenia",
                "Labour Code of the Republic of Armenia & Law on Employment",
                "Article 18 & Article 34",
                "Charging fees or demanding consideration from jobseekers for employment mediation or domestic placement.",
                25000.0,
                [
                    "Revocation of the private employment mediation permit",
                    "Administrative fines imposed by the Health and Labor Inspection Body (HLIB)",
                    "Compulsory full refund of extorted fees with statutory interest"
                ],
                "Health and Labor Inspection Body of the Republic of Armenia (HLIB)"
            ),
            (
                "STAT-AK-002",
                "AZ",
                "Azerbaijan",
                "Law of the Republic of Azerbaijan on Employment & Labour Code",
                "Article 12 & Article 312",
                "Demanding payment from citizens for job placement services inside the country or overseas.",
                30000.0,
                [
                    "Cancellation of recruitment license issued by Ministry of Labour",
                    "Administrative sanctions and criminal referral for deceptive recruitment"
                ],
                "State Labour Inspection Service (Ministry of Labour and Social Protection of Population, Azerbaijan)"
            ),
            (
                "STAT-AK-003",
                "GE",
                "Georgia",
                "Organic Law of Georgia - Labour Code & Law on Employment Promotion",
                "Article 15 & Article 22",
                "Charging fees to jobseekers for mediation or placement services without accredited certification.",
                20000.0,
                [
                    "Fines and revocation of intermediary registration by Labour Conditions Inspection Department",
                    "Direct restitution orders enforceable in civil courts"
                ],
                "Labour Conditions Inspection Department (Ministry of Internally Displaced Persons, Georgia)"
            ),
            (
                "STAT-AK-004",
                "TR",
                "Turkey",
                "Turkish Labour Law (Law No. 4857) & Turkish Employment Agency Law (Law No. 4904)",
                "Article 17 & Article 20",
                "Private employment agencies charging fees or receiving financial benefits from jobseekers or employees.",
                45000.0,
                [
                    "Cancellation of private employment agency authorization by İŞKUR",
                    "Administrative monetary fines up to 100,000 TRY per violation",
                    "Judicial prosecution for unlicensed intermediation"
                ],
                "Türkiye İş Kurumu Genel Müdürlüğü (İŞKUR / Ministry of Labour and Social Security)"
            )
        ]

        for s_id, iso, cname, title, art, prohib, pen, rems, enf in records:
            self.statutes[s_id] = BlackSeaCaucasusLaborStatuteAK(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statutory_law_title=title,
                article_citation=art,
                prohibited_conduct_summary=prohib,
                maximum_penalty_usd_equivalent=pen,
                remedial_measures=rems,
                enforcing_ministry=enf
            )

    def get_statute(self, statute_id: str) -> Optional[BlackSeaCaucasusLaborStatuteAK]:
        return self.statutes.get(statute_id)
