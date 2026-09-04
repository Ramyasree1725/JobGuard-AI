"""
JobGuard Core Compliance - Statutory Labor Penalties Master Catalog Volume N
Statutory labor reference volume N covering Canadian provincial employment acts
(Quebec, Alberta, Manitoba, Saskatchewan, Nova Scotia), worker recruitment fee bans, and penalties.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class CanadianProvincialStatuteN:
    statute_id: str
    province_code: str
    province_name: str
    statute_name: str
    relevant_section: str
    fee_prohibition_summary: str
    maximum_corporate_penalty_cad: float
    restitution_provisions: str
    lead_ministry: str


class StatutoryLaborPenaltiesMasterCatalogN:
    """Master expanded catalog volume N covering Canadian provincial labor legislation."""

    def __init__(self):
        self.statutes: Dict[str, CanadianProvincialStatuteN] = {}
        self._seed_volume_n()

    def _seed_volume_n() -> None:
        """Register Canadian provincial labor statutes."""

        records = [
            (
                "STAT-N-001",
                "CA_QC",
                "Quebec",
                "Act respecting labour standards (CQLR c. N-1.1)",
                "Section 92.5 & Section 140",
                "No personnel placement agency or recruitment enterprise may charge any fees to a worker for their placement.",
                100000.0,
                "Mandatory reimbursement of all fees collected with interest plus administrative penalties.",
                "Commission des normes, de l'équité, de la santé et de la sécurité du travail (CNESST)"
            ),
            (
                "STAT-N-002",
                "CA_AB",
                "Alberta",
                "Employment Standards Code (RSA 2000 c. E-9)",
                "Section 12.1 & Section 132",
                "Prohibits employment agencies from demanding or collecting fees from individuals seeking employment.",
                100000.0,
                "Director of Employment Standards order for full recovery of fees paid.",
                "Alberta Jobs, Economy and Trade (Employment Standards Branch)"
            ),
            (
                "STAT-N-003",
                "CA_MB",
                "Manitoba",
                "The Worker Recruitment and Protection Act (C.C.S.M. c. W197)",
                "Section 3 & Section 21",
                "Strict licensing requirement for foreign worker recruiters. Complete prohibition on charging workers any fee.",
                50000.0,
                "Full compensation order and forfeiture of mandatory $10,000 security bond.",
                "Manitoba Labour and Immigration (Employment Standards Division)"
            ),
            (
                "STAT-N-004",
                "CA_SK",
                "Saskatchewan",
                "The Saskatchewan Employment Act (SS 2013 c. S-15.1)",
                "Part II, Section 2-88",
                "Unlawful for any person to charge or receive a fee from a worker for finding or assisting in finding employment.",
                50000.0,
                "Order to repay fees to employee enforceable as a judgment of the Court of King's Bench.",
                "Saskatchewan Ministry of Labour Relations and Workplace Safety"
            ),
            (
                "STAT-N-005",
                "CA_NS",
                "Nova Scotia",
                "Labour Standards Code (RSNS 1989 c. 246)",
                "Section 89B & Section 90",
                "Bans recruiters and employers from charging fees to workers for recruitment or placement services.",
                25000.0,
                "Director order requiring full repayment of fees with statutory interest.",
                "Nova Scotia Department of Labour, Skills and Immigration"
            )
        ]

        for s_id, p_code, p_name, s_name, sec, fee_sum, pen, rest, min_dept in records:
            self.statutes[s_id] = CanadianProvincialStatuteN(
                statute_id=s_id,
                province_code=p_code,
                province_name=p_name,
                statute_name=s_name,
                relevant_section=sec,
                fee_prohibition_summary=fee_sum,
                maximum_corporate_penalty_cad=pen,
                restitution_provisions=rest,
                lead_ministry=min_dept
            )

    def get_statute(self, statute_id: str) -> Optional[CanadianProvincialStatuteN]:
        return self.statutes.get(statute_id)
