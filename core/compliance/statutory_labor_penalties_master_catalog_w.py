"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume W
Statutory labor reference volume W covering Baltic, Balkan, and Caucasian regional labor standards
(Estonia, Latvia, Lithuania, Croatia, Serbia, Georgia), recruitment licensing, and penalties.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class BalticBalkanStatuteW:
    statute_id: str
    country_iso: str
    country_name: str
    statutory_act_title: str
    section_reference: str
    prohibited_conduct: str
    maximum_penalty_eur: float
    remedial_measures: List[str]
    enforcing_authority: str


class StatutoryLaborPenaltiesMasterCatalogW:
    """Master expanded catalog volume W covering Baltic and Balkan labor legislation."""

    def __init__(self):
        self.statutes: Dict[str, BalticBalkanStatuteW] = {}
        self._seed_volume_w()

    def _seed_volume_w() -> None:
        """Register statutory labor regulations."""

        records = [
            (
                "STAT-W-001",
                "EE",
                "Estonia",
                "Labour Market Measures Act (Tööturumeetmete seadus) & Employment Contracts Act",
                "Section 38 & Section 120",
                "Charging fees or demanding compensation from jobseekers for employment mediation services.",
                32000.0,
                [
                    "Revocation of registration in the register of economic activities",
                    "Misdemeanour proceedings by the Labour Inspectorate (Tööinspektsioon)",
                    "Mandatory restitution of all sums extracted from work-seekers"
                ],
                "Tööinspektsioon (Estonian Labour Inspectorate)"
            ),
            (
                "STAT-W-002",
                "LV",
                "Latvia",
                "Support for Unemployed Persons and Persons Seeking Employment Law",
                "Section 17 & Section 21",
                "Receiving payment or financial compensation from jobseekers for work placement services.",
                30000.0,
                [
                    "Annulment of licence issued by the State Employment Agency (NVA)",
                    "Administrative fines imposed by the State Labour Inspectorate (VDI)"
                ],
                "Valsts darba inspekcija (State Labour Inspectorate Latvia)"
            ),
            (
                "STAT-W-003",
                "LT",
                "Lithuania",
                "Law on Employment of the Republic of Lithuania (Užimtumo įstatymas)",
                "Article 35 & Article 58",
                "Direct or indirect fee collection from jobseekers for employment mediation or placement.",
                35000.0,
                [
                    "Suspension of recruitment agency activities",
                    "Administrative liability under the Code of Administrative Offences"
                ],
                "Valstybinė darbo inspekcija (State Labour Inspectorate Lithuania - VDI)"
            ),
            (
                "STAT-W-004",
                "HR",
                "Croatia",
                "Labour Market Act (Zakon o tržištu rada - NN 118/18)",
                "Article 32 & Article 98",
                "Charging candidates fees for mediation in employment or temp agency assignment.",
                40000.0,
                [
                    "Fines up to 100,000 HRK / equivalent EUR on agency and responsible manager",
                    "Removal from the register of employment mediation agencies"
                ],
                "Državni inspektorat Republike Hrvatske (State Inspectorate of Croatia)"
            ),
            (
                "STAT-W-005",
                "RS",
                "Serbia",
                "Law on Employment and Unemployment Insurance (Zakon o zapošljavanju)",
                "Article 27 & Article 105",
                "Charging fees to persons seeking employment for employment mediation services.",
                25000.0,
                [
                    "Loss of operating license granted by Ministry of Labour",
                    "Misdemeanor fines on legal entity and director"
                ],
                "Ministarstvo za rad, zapošljavanje, boračka i socijalna pitanja (Labour Inspectorate Serbia)"
            )
        ]

        for s_id, iso, cname, title, sec, prohib, pen, rems, enf in records:
            self.statutes[s_id] = BalticBalkanStatuteW(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statutory_act_title=title,
                section_reference=sec,
                prohibited_conduct=prohib,
                maximum_penalty_eur=pen,
                remedial_measures=rems,
                enforcing_authority=enf
            )

    def get_statute(self, statute_id: str) -> Optional[BalticBalkanStatuteW]:
        return self.statutes.get(statute_id)
