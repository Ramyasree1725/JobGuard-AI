"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume AL
Statutory labor reference volume AL covering East Asian Maritime & Insular jurisdictions
(Macau SAR, Brunei Darussalam, Timor-Leste, Maldives), recruitment licensing standards, and penalties.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class MaritimeInsularLaborStatuteAL:
    statute_id: str
    country_iso: str
    territory_name: str
    governing_legislation_title: str
    article_reference: str
    prohibited_recruitment_practice: str
    maximum_fine_usd_equivalent: float
    remedial_and_penal_measures: List[str]
    enforcing_department: str


class StatutoryLaborPenaltiesMasterCatalogAL:
    """Master expanded catalog volume AL covering Maritime Insular and Asian regional labor codes."""

    def __init__(self):
        self.statutes: Dict[str, MaritimeInsularLaborStatuteAL] = {}
        self._seed_volume_al()

    def _seed_volume_al() -> None:
        """Register statutory labor regulations."""

        records = [
            (
                "STAT-AL-001",
                "MO",
                "Macau SAR",
                "Regime Jurídico da Atividade de Agências de Emprego (Lei n.º 16/2020)",
                "Artigo 24.º & Artigo 38.º",
                "Charging fees or commissions to non-resident workers exceeding statutory limits (maximum 50% of first month salary).",
                35000.0,
                [
                    "Revocation of employment agency license by the Labour Affairs Bureau (DSAL)",
                    "Administrative fines up to MOP 50,000 per affected employee",
                    "Mandatory full restitution of all excess fees charged"
                ],
                "Direcção dos Serviços para os Assuntos Laborais (DSAL Macau)"
            ),
            (
                "STAT-AL-002",
                "BN",
                "Brunei Darussalam",
                "Employment Agencies Order, 2004 & Employment Order, 2009",
                "Section 15 & Section 42",
                "Charging unauthorized placement fees or deducting recruitment costs from employee wages.",
                30000.0,
                [
                    "Cancellation of employment agency license by the Commissioner of Labour",
                    "Forfeiture of security deposit furnished to the Department of Labour",
                    "Imprisonment up to 3 years and fines up to BND 6,000"
                ],
                "Department of Labour (Ministry of Home Affairs, Brunei Darussalam)"
            ),
            (
                "STAT-AL-003",
                "TL",
                "Timor-Leste",
                "Labour Code of Timor-Leste (Law No. 4/2012) & Decree-Law on Employment Mediation",
                "Article 14 & Article 105",
                "Collecting fees from jobseekers for domestic placement or foreign worker dispatch.",
                20000.0,
                [
                    "Withdrawal of the private employment agency license by SEFOPE",
                    "Administrative fines imposed by General Labour Inspectorate (IGT)"
                ],
                "Secretaria de Estado para a Formação Profissional e Emprego (SEFOPE Timor-Leste)"
            ),
            (
                "STAT-AL-004",
                "MV",
                "Maldives",
                "Maldives Employment Act (Law No. 2/2008) & Employment Agency Regulations",
                "Section 18 & Section 86",
                "Private employment agencies demanding service fees or deposits from expatriate or local jobseekers.",
                25000.0,
                [
                    "Deregistration of employment agency by Ministry of Homeland Security and Technology",
                    "Fines up to MVR 50,000 and mandatory reimbursement of all fees collected"
                ],
                "Labour Relations Authority (Ministry of Higher Education, Labour and Skills Development, Maldives)"
            )
        ]

        for s_id, iso, tname, title, art, prohib, fine, rems, enf in records:
            self.statutes[s_id] = MaritimeInsularLaborStatuteAL(
                statute_id=s_id,
                country_iso=iso,
                territory_name=tname,
                governing_legislation_title=title,
                article_reference=art,
                prohibited_recruitment_practice=prohib,
                maximum_fine_usd_equivalent=fine,
                remedial_and_penal_measures=rems,
                enforcing_department=enf
            )

    def get_statute(self, statute_id: str) -> Optional[MaritimeInsularLaborStatuteAL]:
        return self.statutes.get(statute_id)
