"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume Q
Statutory labor reference volume Q covering Latin American employment legislation
(Mexico, Brazil, Argentina, Colombia, Chile), recruiter fee bans, and worker protection codes.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class LatinAmericaStatuteQ:
    statute_id: str
    country_iso: str
    country_name: str
    statute_title: str
    article_reference: str
    prohibited_recruitment_practice: str
    maximum_fine_usd_equivalent: float
    remedial_and_penal_consequences: str
    enforcing_ministry: str


class StatutoryLaborPenaltiesMasterCatalogQ:
    """Master expanded catalog volume Q covering Latin American statutory labor codes."""

    def __init__(self):
        self.statutes: Dict[str, LatinAmericaStatuteQ] = {}
        self._seed_volume_q()

    def _seed_volume_q(self) -> None:
        """Register Latin American statutory labor regulations."""

        records = [
            (
                "STAT-Q-001",
                "MX",
                "Mexico",
                "Ley Federal del Trabajo (LFT)",
                "Artículo 133, Fracción I & Artículo 1004",
                "Exigir la compra de artículos de consumo o cobrar cuotas de colocación o capacitación a los aspirantes a un empleo.",
                35000.0,
                "Multas de hasta 5,000 veces la UMA e inhabilitación temporal de la agencia de colocación.",
                "Secretaría del Trabajo y Previsión Social (STPS)"
            ),
            (
                "STAT-Q-002",
                "BR",
                "Brazil",
                "Consolidação das Leis do Trabalho (CLT) & Lei nº 6.019/1974",
                "Artigo 462 & Artigo 19-A",
                "Cobrança de taxa de recrutamento ou intermediação de mão de obra do trabalhador ou candidato.",
                40000.0,
                "Ressarcimento em dobro de todos os valores retidos indevidamente com juros e correção monetária.",
                "Ministério do Trabalho e Emprego (MTE - Fiscalização do Trabalho)"
            ),
            (
                "STAT-Q-003",
                "AR",
                "Argentina",
                "Ley de Contrato de Trabajo (Ley Nº 20.744)",
                "Artículo 131 & Artículo 135",
                "Exigir sumas de dinero o retenciones indebidas a los postulantes como condición para su ingreso laboral.",
                30000.0,
                "Nulidad absoluta de las deducciones y sanciones pecuniarias a los intermediarios laborales.",
                "Ministerio de Capital Humano (Secretaría de Trabajo, Empleo y Seguridad Social)"
            ),
            (
                "STAT-Q-004",
                "CO",
                "Colombia",
                "Código Sustantivo del Trabajo & Ley 1429 de 2010",
                "Artículo 149 & Artículo 77",
                "Cobrar tarifas o sumas de dinero a los trabajadores por los servicios de gestión y colocación de empleo.",
                25000.0,
                "Revocatoria de la autorización de funcionamiento de la agencia y multas administrativas.",
                "Ministerio del Trabajo de Colombia (Unidad del Servicio Público de Empleo)"
            ),
            (
                "STAT-Q-005",
                "CL",
                "Chile",
                "Código del Trabajo de Chile",
                "Artículo 183-C & Artículo 183-K",
                "Exigir cobros o cauciones a los trabajadores que soliciten servicios de intermediación o empleo transitorio.",
                30000.0,
                "Cancelación del registro especial de empresas de servicios transitorios y multas a beneficio fiscal.",
                "Dirección del Trabajo (DT Chile)"
            )
        ]

        for s_id, iso, cname, title, art_ref, prohib, fine, penal, enf in records:
            self.statutes[s_id] = LatinAmericaStatuteQ(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statute_title=title,
                article_reference=art_ref,
                prohibited_recruitment_practice=prohib,
                maximum_fine_usd_equivalent=fine,
                remedial_and_penal_consequences=penal,
                enforcing_ministry=enf
            )

    def get_statute(self, statute_id: str) -> Optional[LatinAmericaStatuteQ]:
        return self.statutes.get(statute_id)
