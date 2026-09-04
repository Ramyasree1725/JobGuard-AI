"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume P
Statutory labor reference volume P covering United Kingdom employment agencies regulations,
GLAA licensing standards, and statutory enforcement penalties under UK law.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class UKStatutoryProvisionP:
    provision_id: str
    statutory_instrument: str
    regulation_citation: str
    prohibited_conduct: str
    max_criminal_sanction: str
    civil_penalty_cap_gbp: float
    regulatory_enforcement_body: str
    remedial_measures: List[str]


class StatutoryLaborPenaltiesMasterCatalogP:
    """Master expanded catalog volume P covering UK employment and labor regulations."""

    def __init__(self):
        self.provisions: Dict[str, UKStatutoryProvisionP] = {}
        self._seed_volume_p()

    def _seed_volume_p(self) -> None:
        """Register UK statutory labor regulations."""

        records = [
            (
                "STAT-P-001",
                "Employment Agencies Act 1973 & Conduct Regulations 2003",
                "Regulation 26 & Section 5",
                "Charging work-seekers any fee for finding or seeking to find them employment, directly or indirectly.",
                "Unlimited fine on summary or indictment conviction and prohibition order up to 10 years.",
                250000.0,
                "Employment Agency Standards (EAS) Inspectorate",
                [
                    "Prohibition from running or being involved in employment agencies",
                    "Mandatory full repayment of all unauthorized fees collected from workers",
                    "Public naming and shaming of non-compliant recruitment operators"
                ]
            ),
            (
                "STAT-P-002",
                "Gangmasters (Licensing) Act 2004",
                "Section 12 & Section 13",
                "Acting as a gangmaster or recruiter in agriculture, food processing, or shellfish gathering without a GLAA license.",
                "Imprisonment for up to 10 years and unlimited criminal fines.",
                500000.0,
                "Gangmasters and Labour Abuse Authority (GLAA)",
                [
                    "Confiscation orders under the Proceeds of Crime Act 2002",
                    "Immediate cessation and closure of unlicensed staffing operations",
                    "Prosecution of labour users employing unlicensed gangmasters"
                ]
            ),
            (
                "STAT-P-003",
                "Modern Slavery Act 2015",
                "Section 1 & Section 2",
                "Holding a person in slavery or servitude, requiring forced labor, or facilitating human trafficking for recruitment exploitation.",
                "Maximum sentence of life imprisonment.",
                1000000.0,
                "National Crime Agency (NCA) / Crown Prosecution Service (CPS)",
                [
                    "Slavery and Trafficking Prevention Orders (STPOs)",
                    "Slavery and Trafficking Reparation Orders for victim compensation",
                    "Asset forfeiture and international freezing orders"
                ]
            ),
            (
                "STAT-P-004",
                "Consumer Protection from Unfair Trading Regulations 2008",
                "Regulation 5 & Regulation 6",
                "Misleading actions or omissions regarding job opportunities, pay rates, or employment terms.",
                "Fine up to statutory maximum and imprisonment up to 2 years.",
                150000.0,
                "Trading Standards / Competition and Markets Authority (CMA)",
                [
                    "Enforcement orders requiring cessation of misleading advertisements",
                    "Direct consumer redress and compensation under CPR Part 4A"
                ]
            )
        ]

        for p_id, inst, reg, prohib, crim, cap, enf, rems in records:
            self.provisions[p_id] = UKStatutoryProvisionP(
                provision_id=p_id,
                statutory_instrument=inst,
                regulation_citation=reg,
                prohibited_conduct=prohib,
                max_criminal_sanction=crim,
                civil_penalty_cap_gbp=cap,
                regulatory_enforcement_body=enf,
                remedial_measures=rems
            )

    def get_provision(self, provision_id: str) -> Optional[UKStatutoryProvisionP]:
        return self.provisions.get(provision_id)
