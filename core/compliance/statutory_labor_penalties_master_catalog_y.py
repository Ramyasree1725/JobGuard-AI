"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume Y
Statutory labor reference volume Y covering Southeast European & Mediterranean labor codes
(Cyprus, Malta, Slovenia, Albania, North Macedonia, Montenegro), recruitment licensing, and penalties.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class MedBalkanLaborStatuteY:
    statute_id: str
    country_iso: str
    country_name: str
    statute_title: str
    article_reference: str
    prohibited_recruitment_practice: str
    maximum_penalty_eur: float
    administrative_remedies: List[str]
    enforcing_ministry: str


class StatutoryLaborPenaltiesMasterCatalogY:
    """Master expanded catalog volume Y covering Mediterranean and Southeast European labor legislation."""

    def __init__(self):
        self.statutes: Dict[str, MedBalkanLaborStatuteY] = {}
        self._seed_volume_y()

    def _seed_volume_y() -> None:
        """Register statutory labor regulations."""

        records = [
            (
                "STAT-Y-001",
                "CY",
                "Cyprus",
                "Private Employment Agency Law of 2012 (Law 126(I)/2012)",
                "Section 16 & Section 28",
                "Charging direct or indirect fees or expenses to work-seekers for job placement services.",
                40000.0,
                [
                    "Immediate revocation of private employment agency license by the Director",
                    "Court-ordered full reimbursement of all fees collected with legal interest",
                    "Criminal prosecution with fines up to €50,000 and imprisonment up to 2 years"
                ],
                "Department of Labour (Ministry of Labour and Social Insurance, Cyprus)"
            ),
            (
                "STAT-Y-002",
                "MT",
                "Malta",
                "Employment Agencies Regulations (S.L. 594.05) & Employment and Training Services Act",
                "Regulation 11 & Section 32",
                "Charging fees or demanding financial consideration from employees or jobseekers for placement.",
                35000.0,
                [
                    "Forfeiture of statutory guarantee bond deposited with the Director",
                    "Cancellation of agency license and publication in the Government Gazette"
                ],
                "Department of Industrial and Employment Relations (DIER Malta)"
            ),
            (
                "STAT-Y-003",
                "SI",
                "Slovenia",
                "Labour Market Regulation Act (Zakon o urejanju trga dela - ZUTD)",
                "Article 12 & Article 135",
                "Demanding payment from jobseekers for employment mediation or temporary work agency services.",
                45000.0,
                [
                    "Removal from the national register of domestic and foreign employment agencies",
                    "Administrative fines imposed by the Labour Inspectorate of the Republic of Slovenia"
                ],
                "Inšpektorat Republike Slovenije za delo (IRSD)"
            ),
            (
                "STAT-Y-004",
                "AL",
                "Albania",
                "Law on Employment Promotion (Law No. 15/2019) & Labour Code",
                "Article 24 & Article 48",
                "Collecting fees or commission from jobseekers for employment mediation services in Albania or abroad.",
                25000.0,
                [
                    "Suspension or revocation of the private employment agency license",
                    "Fines and mandatory restitution enforced by State Labour Inspectorate"
                ],
                "Inspektorati Shtetëror i Punës dhe Shërbimeve Shoqërore (State Labour Inspectorate Albania)"
            ),
            (
                "STAT-Y-005",
                "MK",
                "North Macedonia",
                "Law on Private Employment Agencies (Official Gazette No. 173/15)",
                "Article 14 & Article 39",
                "Charging fees to unemployed persons or job seekers for mediation in employment.",
                30000.0,
                [
                    "Revocation of license issued by Ministry of Labour and Social Policy",
                    "Fines on legal entity and responsible natural person"
                ],
                "State Labour Inspectorate of North Macedonia (DIT)"
            )
        ]

        for s_id, iso, cname, title, art, prohib, pen, rems, enf in records:
            self.statutes[s_id] = MedBalkanLaborStatuteY(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statute_title=title,
                article_reference=art,
                prohibited_recruitment_practice=prohib,
                maximum_penalty_eur=pen,
                administrative_remedies=rems,
                enforcing_ministry=enf
            )

    def get_statute(self, statute_id: str) -> Optional[MedBalkanLaborStatuteY]:
        return self.statutes.get(statute_id)
