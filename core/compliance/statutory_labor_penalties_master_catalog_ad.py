"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume AD
Statutory labor reference volume AD covering European Union Candidate States & Western Balkans
(Bosnia and Herzegovina, Kosovo, Moldova, Ukraine), employment agency regulations, and fee bans.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class WesternBalkansLaborStatuteAD:
    statute_id: str
    country_iso: str
    country_name: str
    statute_title: str
    citation_article: str
    prohibited_conduct_detail: str
    maximum_penalty_eur: float
    administrative_sanctions: List[str]
    enforcing_ministry: str


class StatutoryLaborPenaltiesMasterCatalogAD:
    """Master expanded catalog volume AD covering Western Balkans and EU candidate state labor codes."""

    def __init__(self):
        self.statutes: Dict[str, WesternBalkansLaborStatuteAD] = {}
        self._seed_volume_ad()

    def _seed_volume_ad() -> None:
        """Register statutory labor regulations."""

        records = [
            (
                "STAT-AD-001",
                "BA",
                "Bosnia and Herzegovina",
                "Labour Law of FBiH & Labour Law of Republika Srpska",
                "Article 15 & Article 174",
                "Charging fees or demanding financial compensation from work-seekers for employment mediation services.",
                25000.0,
                [
                    "Revocation of permit issued by the Federal Ministry of Labour",
                    "Administrative fines on agency legal entity and director",
                    "Court-ordered refund of all collected sums"
                ],
                "Federal Administration for Inspection Affairs (FUZIP BiH)"
            ),
            (
                "STAT-AD-002",
                "XK",
                "Kosovo",
                "Law on Private Employment Agencies (Law No. 04/L-205) & Labour Law",
                "Article 12 & Article 30",
                "Private employment agencies demanding payments or deductions from jobseekers for placement.",
                20000.0,
                [
                    "Withdrawal of private employment agency license by the Ministry",
                    "Fines and mandatory reimbursement enforced by the Labour Inspectorate"
                ],
                "Labour Inspectorate of the Republic of Kosovo (IPK)"
            ),
            (
                "STAT-AD-003",
                "MD",
                "Moldova",
                "Law on Employment Promotion and Unemployment Insurance (No. 105/2018)",
                "Article 11 & Article 62",
                "Collecting fees from citizens of the Republic of Moldova for employment placement services.",
                25000.0,
                [
                    "Revocation of operating license for private employment agencies",
                    "Fines imposed by the State Labour Inspectorate (Inspectoratul de Stat al Muncii)"
                ],
                "Inspectoratul de Stat al Muncii (State Labour Inspectorate Moldova)"
            ),
            (
                "STAT-AD-004",
                "UA",
                "Ukraine",
                "Law of Ukraine 'On Employment of Population' (No. 5067-VI)",
                "Article 37 & Article 53",
                "Charging fees or receiving payments from jobseekers for employment mediation in Ukraine or abroad (fees must be paid exclusively by employers).",
                30000.0,
                [
                    "Cancellation of the agency's declaration of economic activity",
                    "Administrative fines of 20 times the minimum statutory wage per violation",
                    "Full restitution of all extorted funds to job seekers"
                ],
                "State Service of Ukraine on Labour Issues (Derzhpratsi)"
            )
        ]

        for s_id, iso, cname, title, art, prohib, pen, rems, enf in records:
            self.statutes[s_id] = WesternBalkansLaborStatuteAD(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statute_title=title,
                citation_article=art,
                prohibited_conduct_detail=prohib,
                maximum_penalty_eur=pen,
                administrative_sanctions=rems,
                enforcing_ministry=enf
            )

    def get_statute(self, statute_id: str) -> Optional[WesternBalkansLaborStatuteAD]:
        return self.statutes.get(statute_id)
