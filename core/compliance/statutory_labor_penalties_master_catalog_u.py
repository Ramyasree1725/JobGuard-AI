"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume U
Statutory labor reference volume U covering Caribbean and Central American labor standards
(Jamaica, Bahamas, Trinidad and Tobago, Costa Rica, Panama), recruitment licensing, and penalties.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class CaribbeanLaborStatuteU:
    statute_id: str
    country_iso: str
    country_name: str
    statute_title: str
    citation_section: str
    prohibited_recruitment_conduct: str
    penalty_usd_equivalent: float
    remedial_measures: List[str]
    enforcing_authority: str


class StatutoryLaborPenaltiesMasterCatalogU:
    """Master expanded catalog volume U covering Caribbean & Central American labor legislation."""

    def __init__(self):
        self.statutes: Dict[str, CaribbeanLaborStatuteU] = {}
        self._seed_volume_u()

    def _seed_volume_u() -> None:
        """Register statutory labor regulations."""

        records = [
            (
                "STAT-U-001",
                "JM",
                "Jamaica",
                "Employment Agencies Regulation Act & Overseas Employment Act",
                "Section 8 & Section 15",
                "Operating an employment agency without a license or charging unauthorized registration fees to job applicants.",
                25000.0,
                [
                    "Revocation of employment agency license",
                    "Court order for immediate repayment of all fees collected",
                    "Fines and imprisonment for unauthorized agency operators"
                ],
                "Ministry of Labour and Social Security (Jamaica)"
            ),
            (
                "STAT-U-002",
                "TT",
                "Trinidad and Tobago",
                "Recruiting of Workers Act (Chap. 88:10)",
                "Section 4 & Section 12",
                "Recruiting workers without a statutory recruiter's permit or demanding unlawful recruitment fees.",
                30000.0,
                [
                    "Forfeiture of security bond furnished to the licensing authority",
                    "Prosecution in the Industrial Court of Trinidad and Tobago"
                ],
                "Ministry of Labour (Trinidad and Tobago)"
            ),
            (
                "STAT-U-003",
                "CR",
                "Costa Rica",
                "Código de Trabajo de Costa Rica & Reglamento de Intermediación de Empleo",
                "Artículo 11 & Artículo 612",
                "Cobrar sumas de dinero o cuotas de inscripción a los trabajadores por intermediación de empleo.",
                30000.0,
                [
                    "Clausura del establecimiento de intermediación laboral",
                    "Devolución íntegra de los montos percibidos con intereses legales"
                ],
                "Ministerio de Trabajo y Seguridad Social (MTSS Costa Rica)"
            ),
            (
                "STAT-U-004",
                "PA",
                "Panama",
                "Código de Trabajo de la República de Panamá",
                "Artículo 24 & Artículo 1064",
                "Cobrar a los trabajadores por los servicios de colocación o intermediación de empleo.",
                25000.0,
                [
                    "Cancelación de la licencia de operación otorgada por MITRADEL",
                    "Multas pecuniarias a favor del fondo de seguridad social"
                ],
                "Ministerio de Trabajo y Desarrollo Laboral (MITRADEL Panamá)"
            )
        ]

        for s_id, iso, cname, title, sec, prohib, pen, rems, enf in records:
            self.statutes[s_id] = CaribbeanLaborStatuteU(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statute_title=title,
                citation_section=sec,
                prohibited_recruitment_conduct=prohib,
                penalty_usd_equivalent=pen,
                remedial_measures=rems,
                enforcing_authority=enf
            )

    def get_statute(self, statute_id: str) -> Optional[CaribbeanLaborStatuteU]:
        return self.statutes.get(statute_id)
