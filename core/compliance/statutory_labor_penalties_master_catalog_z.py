"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume Z
Statutory labor reference volume Z covering Lusophone & Francophone African labor standards
(Angola, Mozambique, Senegal, Ivory Coast, Cameroon), recruitment licensing standards, and penalties.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class FrancoLusoAfricanStatuteZ:
    statute_id: str
    country_iso: str
    country_name: str
    statutory_code_title: str
    article_reference: str
    prohibited_conduct_summary: str
    penalty_usd_equivalent: float
    administrative_remedies: List[str]
    enforcing_ministry: str


class StatutoryLaborPenaltiesMasterCatalogZ:
    """Master expanded catalog volume Z covering Lusophone and Francophone African labor codes."""

    def __init__(self):
        self.statutes: Dict[str, FrancoLusoAfricanStatuteZ] = {}
        self._seed_volume_z()

    def _seed_volume_z() -> None:
        """Register statutory labor regulations."""

        records = [
            (
                "STAT-Z-001",
                "AO",
                "Angola",
                "Lei Geral do Trabalho (Lei n.º 12/23) & Decreto Presidencial n.º 106/18",
                "Artigo 14.º & Artigo 304.º",
                "Cobrança de quaisquer taxas, despesas ou comissões aos trabalhadores pelos serviços de colocação ou recrutamento.",
                35000.0,
                [
                    "Cancelamento do alvará de agência privada de colocação pelo MAPTSS",
                    "Multas pecuniárias graduadas em função da gravidade da infracção",
                    "Obrigação de reembolso integral das quantias extorquidas"
                ],
                "Inspecção Geral do Trabalho (IGT Angola / MAPTSS)"
            ),
            (
                "STAT-Z-002",
                "MZ",
                "Mozambique",
                "Lei do Trabalho (Lei n.º 13/2023) & Regulamento das Agências Privadas de Emprego",
                "Artigo 19.º & Artigo 268.º",
                "Exigir qualquer pagamento, directa ou indirectamente, dos candidatos a emprego ou trabalhadores.",
                30000.0,
                [
                    "Cassação da licença de exercício da actividade de colocação",
                    "Sancionamento contra-ordenacional pela Inspecção Geral do Trabalho"
                ],
                "Inspecção Geral do Trabalho (IGT Moçambique / MITESS)"
            ),
            (
                "STAT-Z-003",
                "SN",
                "Senegal",
                "Code du travail du Sénégal (Loi n° 97-17) & Décret n° 2009-1412",
                "Article L.226 & Article L.280",
                "Percevoir des rétributions ou honoraires auprès des demandeurs d'emploi à l'occasion de leur placement.",
                25000.0,
                [
                    "Fermeture administrative du bureau de placement privé",
                    "Poursuites pénales et restitution obligatoire des frais perçus"
                ],
                "Direction générale du Travail et de la Sécurité sociale (DGTSS Sénégal)"
            ),
            (
                "STAT-Z-004",
                "CI",
                "Ivory Coast",
                "Code du travail de Côte d'Ivoire (Loi n° 2015-532)",
                "Article 11.4 & Article 92.1",
                "Exiger des demandeurs d'emploi une rémunération quelconque pour des services de recrutement ou placement.",
                30000.0,
                [
                    "Retrait de l'agrément ministériel accordé à l'agence de placement",
                    "Sanctions pécuniaires et pénales prononcées par le Tribunal du Travail"
                ],
                "Inspection générale du Travail (Ministère de l'Emploi et de la Protection Sociale)"
            ),
            (
                "STAT-Z-005",
                "CM",
                "Cameroon",
                "Code du travail du Cameroun (Loi n° 92/007)",
                "Article 24 & Article 168",
                "Perception d'une rémunération quelconque auprès des travailleurs à l'occasion des opérations de placement.",
                20000.0,
                [
                    "Annulation de l'autorisation d'ouverture du bureau de placement",
                    "Amendes pénales infligées aux promoteurs et directeurs"
                ],
                "Inspection du Travail et de la Prévoyance Sociale (MINTSS Cameroun)"
            )
        ]

        for s_id, iso, cname, code, art, prohib, pen, rems, enf in records:
            self.statutes[s_id] = FrancoLusoAfricanStatuteZ(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                statutory_code_title=code,
                article_reference=art,
                prohibited_conduct_summary=prohib,
                penalty_usd_equivalent=pen,
                administrative_remedies=rems,
                enforcing_ministry=enf
            )

    def get_statute(self, statute_id: str) -> Optional[FrancoLusoAfricanStatuteZ]:
        return self.statutes.get(statute_id)
