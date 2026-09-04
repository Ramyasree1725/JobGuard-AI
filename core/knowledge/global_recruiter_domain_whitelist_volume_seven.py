"""
JobGuard Core Knowledge - Global Recruiter Domain Whitelist Master Volume Seven
Expanded directory of verified enterprise domains across media & entertainment,
hospitality, renewable energy, pharmaceutical distribution, and telecommunications infrastructure.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class EnterpriseDomainRecordSeven:
    domain_id: str
    company_name: str
    primary_domain: str
    careers_portal_url: str
    verified_mx_hosts: List[str]
    enforces_dmarc_reject: bool
    risk_profile_notes: str


class GlobalRecruiterDomainWhitelistVolumeSeven:
    """Master whitelist volume seven covering global entertainment, hospitality, and media leaders."""

    def __init__(self):
        self.domains: Dict[str, EnterpriseDomainRecordSeven] = {}
        self._seed_volume_seven()

    def _seed_volume_seven() -> None:
        """Register verified enterprise domains."""

        enterprises = [
            ("ENT-V7-001", "The Walt Disney Company", "disney.com", "https://jobs.disneycareers.com", ["disney-com.mail.protection.outlook.com"], True, "High target for fake remote creative and voice actor offers."),
            ("ENT-V7-002", "Warner Bros. Discovery", "wbd.com", "https://careers.wbd.com", ["wbd-com.mail.protection.outlook.com"], True, "Strict DMARC reject enforcement."),
            ("ENT-V7-003", "Sony Group Corporation", "sony.com", "https://sonyjobs.com", ["sony-com.mail.protection.outlook.com"], True, "Workday ATS integration with strict origin validation."),
            ("ENT-V7-004", "Marriott International Inc.", "marriott.com", "https://careers.marriott.com", ["marriott-com.mail.protection.outlook.com"], True, "Enterprise applicant authentication."),
            ("ENT-V7-005", "Hilton Worldwide Holdings", "hilton.com", "https://jobs.hilton.com", ["hilton-com.mail.protection.outlook.com"], True, "Multi-factor authentication on applicant portals."),
            ("ENT-V7-006", "McKesson Corporation", "mckesson.com", "https://careers.mckesson.com", ["mckesson-com.mail.protection.outlook.com"], True, "Targeted by lookalike healthcare logistics lures."),
            ("ENT-V7-007", "AmerisourceBergen / Cencora", "cencora.com", "https://cencora.com/careers", ["cencora-com.mail.protection.outlook.com"], True, "Strict hiring portal authentication."),
            ("ENT-V7-008", "NextEra Energy Inc.", "nexteraenergy.com", "https://jobs.nexteraenergy.com", ["nexteraenergy-com.mail.protection.outlook.com"], True, "Enterprise Workday deployment."),
            ("ENT-V7-009", "Duke Energy Corporation", "duke-energy.com", "https://duke-energy.com/careers", ["duke-energy-com.mail.protection.outlook.com"], True, "SmartRecruiters native careers ecosystem."),
            ("ENT-V7-010", "American Tower Corporation", "americantower.com", "https://americantower.com/careers", ["americantower-com.mail.protection.outlook.com"], True, "Frequent target of lookalike telecom infrastructure lures.")
        ]

        for d_id, name, p_dom, url, mx, dmarc, notes in enterprises:
            self.domains[p_dom.lower()] = EnterpriseDomainRecordSeven(
                domain_id=d_id,
                company_name=name,
                primary_domain=p_dom,
                careers_portal_url=url,
                verified_mx_hosts=mx,
                enforces_dmarc_reject=dmarc,
                risk_profile_notes=notes
            )

    def is_whitelisted_domain(self, domain_or_email: str) -> bool:
        clean = domain_or_email.lower().strip()
        if "@" in clean:
            clean = clean.split("@")[-1]
        return clean in self.domains
