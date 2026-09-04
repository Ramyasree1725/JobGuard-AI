"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume R
Statutory labor reference volume R covering Mediterranean and Southern European employment acts
(Italy, Spain, Portugal, Greece), temporary work agency decrees, and statutory recruitment sanctions.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class MediterraneanStatuteR:
    statute_id: str
    country_iso: str
    country_name: str
    act_title: str
    normative_reference: str
    prohibited_practice: str
    maximum_civil_penalty_eur: float
    criminal_charge_summary: str
    enforcement_directorate: str


class StatutoryLaborPenaltiesMasterCatalogR:
    """Master expanded catalog volume R covering Mediterranean European statutory labor codes."""

    def __init__(self):
        self.statutes: Dict[str, MediterraneanStatuteR] = {}
        self._seed_volume_r()

    def _seed_volume_r() -> None:
        """Register Mediterranean statutory labor regulations."""

        records = [
            (
                "STAT-R-001",
                "IT",
                "Italy",
                "Decreto Legislativo 10 settembre 2003, n. 276 (Riforma Biagi)",
                "Articolo 11 & Articolo 18",
                "Percezione di compensi o vantaggi economici dai lavoratori in cambio della loro assunzione o mediazione.",
                50000.0,
                "Arresto fino ad un anno o ammenda; cancellazione dall'albo nazionale delle agenzie per il lavoro.",
                "Ispettorato Nazionale del Lavoro (INL)"
            ),
            (
                "STAT-R-002",
                "ES",
                "Spain",
                "Ley sobre Infracciones y Sanciones en el Orden Social (LISOS - RDL 5/2000)",
                "Artículo 16 & Artículo 19-B",
                "Exigir a los trabajadores precio, tarifa o compensación económica por su selección o intermediación laboral.",
                75000.0,
                "Sanciones de grado máximo y clausura de la agencia de colocación no autorizada.",
                "Inspección de Trabajo y Seguridad Social (ITSS)"
            ),
            (
                "STAT-R-003",
                "PT",
                "Portugal",
                "Código do Trabalho (Lei n.º 7/2009) & Decreto-Lei n.º 260/2009",
                "Artigo 176.º & Artigo 190.º",
                "Cobrança direta ou indireta de quaisquer quantias aos candidatos a emprego pela prestação de serviços de colocação.",
                40000.0,
                "Revogação da licença de agência privada de colocação e contraordenações muito graves.",
                "Autoridade para as Condições do Trabalho (ACT)"
            ),
            (
                "STAT-R-004",
                "GR",
                "Greece",
                "Law 4052/2012 on Temporary Employment and Private Employment Agencies",
                "Article 124 & Article 130",
                "Charging fees, commission, or expenses to jobseekers for job placement services.",
                45000.0,
                "Administrative fines and revocation of the private employment agency operational license.",
                "Hellenic Labour Inspectorate (SEPE)"
            )
        ]

        for s_id, iso, cname, title, norm, prohib, fine, crim, enf in records:
            self.statutes[s_id] = MediterraneanStatuteR(
                statute_id=s_id,
                country_iso=iso,
                country_name=cname,
                act_title=title,
                normative_reference=norm,
                prohibited_practice=prohib,
                maximum_civil_penalty_eur=fine,
                criminal_charge_summary=crim,
                enforcement_directorate=enf
            )

    def get_statute(self, statute_id: str) -> Optional[MediterraneanStatuteR]:
        return self.statutes.get(statute_id)
