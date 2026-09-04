"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume V
Statutory labor reference volume V covering South American Andean Community labor standards
(Peru, Ecuador, Bolivia, Paraguay, Uruguay), recruitment licensing, and penalties.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class AndeanLaborStatuteV:
    statute_id: str
    country_iso: str
    country_name: str
    statutory_law_name: str
    article_citation: str
    prohibited_conduct_summary: str
    penalty_usd_equivalent: float
    administrative_remedies: List[str]
    enforcing_ministry: str


class StatutoryLaborPenaltiesMasterCatalogV:
    """Master expanded catalog volume V covering South American Andean statutory labor codes."""

    def __init__(self):
        self.statutes: Dict[str, AndeanLaborStatuteV] = {}
        self._seed_volume_v()

    def _seed_volume_v() -> None:
        """Register statutory labor regulations."""

        records = [
            (
                "STAT-V-001",
                "PE",
                "Peru",
                "Ley General de Inspección del Trabajo (Ley Nº 28806) & D.S. 005-2003-TR",
                "Artículo 25 & Artículo 34",
                "Exigir cobro directo o indirecto a los postulantes o trabajadores por servicios de intermediación o colocación laboral.",
                35000.0,
                [
                    "Cancelación del registro de agencias privadas de empleo (RENEEIL)",
                    "Multas muy graves impuestas por la Superintendencia Nacional de Fiscalización Laboral (SUNAFIL)",
                    "Devolución inmediata de los montos indebidamente percibidos"
                ],
                "Superintendencia Nacional de Fiscalización Laboral (SUNAFIL / MTPE)"
            ),
            (
                "STAT-V-002",
                "EC",
                "Ecuador",
                "Código del Trabajo del Ecuador & Mandato Constituyente No. 8",
                "Artículo 44 & Artículo 10",
                "Prohibición de cobrar valores, cauciones o porcentajes de sueldo a los trabajadores por intermediación laboral.",
                40000.0,
                [
                    "Clausura definitiva de la empresa de servicios complementarios",
                    "Sanciones pecuniarias de hasta 200 salarios básicos unificados",
                    "Responsabilidad solidaria entre la agencia y la empresa usuaria"
                ],
                "Ministerio del Trabajo del Ecuador"
            ),
            (
                "STAT-V-003",
                "BO",
                "Bolivia",
                "Ley General del Trabajo & Decreto Supremo Nº 29215",
                "Artículo 8 & Artículo 120",
                "Cobro de comisiones o depósitos a postulantes para acceder a fuentes de empleo o trámites de contratación.",
                20000.0,
                [
                    "Revocatoria de la personería y autorización de funcionamiento",
                    "Intervención de la Dirección General de Trabajo"
                ],
                "Ministerio de Trabajo, Empleo y Previsión Social (Bolivia)"
            ),
            (
                "STAT-V-004",
                "UY",
                "Uruguay",
                "Ley Nº 18.251 (Responsabilidad Laboral en Procesos de Descentralización Empresarial)",
                "Artículo 1 & Artículo 8",
                "Cobrar remuneraciones, depósitos en garantía o gastos de gestión a los trabajadores seleccionados.",
                30000.0,
                [
                    "Responsabilidad solidaria de las obligaciones laborales y previsionales",
                    "Sanciones pecuniarias de la Inspección General del Trabajo y la Seguridad Social"
                ],
                "Ministerio de Trabajo y Seguridad Social (MTSS Uruguay - IGTSS)"
            ),
            (
                "STAT-V-005",
                "PY",
                "Paraguay",
                "Código del Trabajo de la República del Paraguay (Ley Nº 213/93)",
                "Artículo 45 & Artículo 385",
                "Exigir pago o gratificación alguna al trabajador por colocarlo en una empresa o intermediar su contratación.",
                25000.0,
                [
                    "Inhabilitación temporal o definitiva de la agencia intermediadora",
                    "Multas pecuniarias liquidadas en jornales mínimos legales"
                ],
                "Ministerio de Trabajo, Empleo y Seguridad Social (MTESS Paraguay)"
            )
        ]

        for s_id, iso, cname, law, art, prohib, pen, rems, enf in records:
            self.statutes[s_id] = AndeanLaborStatuteV(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statutory_law_name=law,
                article_citation=art,
                prohibited_conduct_summary=prohib,
                penalty_usd_equivalent=pen,
                administrative_remedies=rems,
                enforcing_ministry=enf
            )

    def get_statute(self, statute_id: str) -> Optional[AndeanLaborStatuteV]:
        return self.statutes.get(statute_id)
