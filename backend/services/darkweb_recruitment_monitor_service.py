"""
JobGuard Backend Service - Dark Web & Underground Recruitment Forum Monitor
Scrapes and monitors illicit onion marketplaces, Telegram cybercrime chat dumps,
and leaked candidate database listings to alert enterprise employers of brand abuse.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import time


@dataclass
class DarkWebListingFinding:
    finding_id: str
    marketplace_source: str
    brand_targeted: str
    listing_title: str
    listing_price_usd: float
    leaked_data_types: List[str]  # e.g., 'CANDIDATE_RESUMES', 'RECRUITER_INMAIL_LOGINS', 'SPOOFED_OFFER_TEMPLATES'
    discovered_timestamp: float
    risk_level: str


class DarkWebRecruitmentMonitorService:
    """Monitors underground forums and leak sites for compromised candidate records and brand templates."""

    def __init__(self):
        self.findings: List[DarkWebListingFinding] = []
        self._seed_recent_findings()

    def _seed_recent_findings(self) -> None:
        """Seed simulated threat findings from underground leak monitoring."""

        self.findings.append(DarkWebListingFinding(
            finding_id="DW-2026-001",
            marketplace_source="BreachForums Mirror",
            brand_targeted="Google",
            listing_title="50,000 Verified Tech Job Seeker Resumes with Phone & Email (US/EU)",
            listing_price_usd=450.0,
            leaked_data_types=["CANDIDATE_RESUMES", "PHONE_NUMBERS"],
            discovered_timestamp=time.time() - 86400 * 2,
            risk_level="HIGH"
        ))

        self.findings.append(DarkWebListingFinding(
            finding_id="DW-2026-002",
            marketplace_source="Telegram CyberMarket",
            brand_targeted="Microsoft",
            listing_title="Microsoft Word Appointment Letter Vector Templates with Signature Overlays",
            listing_price_usd=120.0,
            leaked_data_types=["SPOOFED_OFFER_TEMPLATES", "EXECUTIVE_SIGNATURES"],
            discovered_timestamp=time.time() - 86400 * 5,
            risk_level="CRITICAL"
        ))

    def get_findings_for_brand(self, brand_name: str) -> List[DarkWebListingFinding]:
        """Filters dark web intelligence findings matching a specific corporate employer."""
        clean = brand_name.lower().strip()
        return [f for f in self.findings if clean in f.brand_targeted.lower()]
