"""
JobGuard Core Knowledge - Counterfeit Check Routing Transit & ABA Number Database
Maintains known fraudulent, altered, closed, or high-risk ABA routing transit numbers
and counterfeit check watermarks extracted from forensic examination of scam disbursements.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class ABARoutingRecord:
    routing_number_9_digit: str
    legitimate_financial_institution: str
    headquarters_city_state: str
    is_frequently_counterfeited_in_scams: bool
    known_counterfeit_drawer_names: List[str]
    alert_notes: str


class CounterfeitCheckRoutingDatabase:
    """Master database for validating routing numbers on candidate-received employment checks."""

    def __init__(self):
        self.routing_table: Dict[str, ABARoutingRecord] = {}
        self._initialize_routing_table()

    def _initialize_routing_table(self) -> None:
        """Register ABA transit numbers frequently cloned in employment fraud."""

        records = [
            (
                "021000021",
                "JPMorgan Chase Bank, N.A.",
                "New York, NY",
                True,
                ["Global Tech Logistics LLC", "Apex Talent Solutions Inc", "Omni Health Staffing"],
                "High prevalence of forged cashier checks issued under non-existent corporate sub-accounts."
            ),
            (
                "121000247",
                "Wells Fargo Bank, N.A.",
                "San Francisco, CA",
                True,
                ["Premier IT Solutions LLC", "United Care Staffing Agency", "HomeOffice Direct Supplies"],
                "Scammers print counterfeit official checks with valid Wells Fargo routing but invalid account numbers."
            ),
            (
                "071000013",
                "Bank of America, N.A.",
                "Charlotte, NC",
                True,
                ["FastTrack Logistics Inc", "Modern Workplace Solutions", "Digital Careers HR"],
                "Counterfeit checks issued with altered MICR encoding lines."
            ),
            (
                "091000019",
                "U.S. Bank, N.A.",
                "Minneapolis, MN",
                True,
                ["National Executive Staffing", "Global Health Systems LLC"],
                "Checks frequently sent via overnight FedEx envelope from residential re-shippers."
            ),
            (
                "111000025",
                "Citibank, N.A.",
                "New York, NY",
                True,
                ["Universal Media Tasks", "Skyline Cloud Logistics"],
                "Stolen corporate identity used to issue checks drawn on closed escrow accounts."
            )
        ]

        for r_num, inst, loc, is_freq, drawers, notes in records:
            self.routing_table[r_num] = ABARoutingRecord(
                routing_number_9_digit=r_num,
                legitimate_financial_institution=inst,
                headquarters_city_state=loc,
                is_frequently_counterfeited_in_scams=is_freq,
                known_counterfeit_drawer_names=drawers,
                alert_notes=notes
            )

    def validate_routing_number(self, routing_9_digit: str) -> Optional[ABARoutingRecord]:
        """Looks up routing transit number and verifies checksum validity."""
        clean = routing_9_digit.strip().replace("-", "").replace(" ", "")
        if len(clean) != 9 or not clean.isdigit():
            return None

        # Check ABA Luhn / Federal Reserve Modulo-10 checksum: 3(d1+d4+d7) + 7(d2+d5+d8) + 1(d3+d6+d9) mod 10 == 0
        d = [int(c) for c in clean]
        checksum = (3 * (d[0] + d[3] + d[6]) + 7 * (d[1] + d[4] + d[7]) + 1 * (d[2] + d[5] + d[8])) % 10
        if checksum != 0:
            return None

        return self.routing_table.get(clean)
