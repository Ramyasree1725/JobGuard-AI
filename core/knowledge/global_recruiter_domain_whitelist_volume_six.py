"""
JobGuard Core Knowledge - Global Recruiter Domain Whitelist Master Volume Six
Expanded directory of verified enterprise domains across biotechnology, medical devices,
commercial aerospace, financial exchanges, and industrial automation enterprises.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class EnterpriseDomainRecordSix:
    domain_id: str
    company_name: str
    primary_domain: str
    careers_portal_url: str
    verified_mx_hosts: List[str]
    enforces_dmarc_reject: bool
    risk_profile_notes: str


class GlobalRecruiterDomainWhitelistVolumeSix:
    """Master whitelist volume six covering Fortune 500 biotech, medical, aerospace, and exchange leaders."""

    def __init__(self):
        self.domains: Dict[str, EnterpriseDomainRecordSix] = {}
        self._seed_volume_six()

    def _seed_volume_six() -> None:
        """Register verified enterprise domains."""

        enterprises = [
            ("ENT-V6-001", "Amgen Inc.", "amgen.com", "https://careers.amgen.com", ["amgen-com.mail.protection.outlook.com"], True, "High target for fake clinical research specialist offers."),
            ("ENT-V6-002", "Gilead Sciences Inc.", "gilead.com", "https://gilead.com/careers", ["gilead-com.mail.protection.outlook.com"], True, "Strict DMARC reject enforcement."),
            ("ENT-V6-003", "Medtronic PLC", "medtronic.com", "https://jobs.medtronic.com", ["medtronic-com.mail.protection.outlook.com"], True, "Workday ATS integration with strict origin validation."),
            ("ENT-V6-004", "Stryker Corporation", "stryker.com", "https://careers.stryker.com", ["stryker-com.mail.protection.outlook.com"], True, "Enterprise applicant authentication."),
            ("ENT-V6-005", "Raytheon Technologies (RTX)", "rtx.com", "https://careers.rtx.com", ["rtx-com.mail.protection.outlook.com"], True, "Multi-factor authentication on applicant portals."),
            ("ENT-V6-006", "Northrop Grumman", "northropgrumman.com", "https://northropgrumman.com/careers", ["northropgrumman-com.mail.protection.outlook.com"], True, "Targeted by lookalike defense contractor lures."),
            ("ENT-V6-007", "General Dynamics", "generaldynamics.com", "https://generaldynamics.com/careers", ["generaldynamics-com.mail.protection.outlook.com"], True, "Strict hiring portal authentication."),
            ("ENT-V6-008", "Intercontinental Exchange (ICE)", "theice.com", "https://theice.com/careers", ["theice-com.mail.protection.outlook.com"], True, "Enterprise Workday deployment."),
            ("ENT-V6-009", "CME Group Inc.", "cmegroup.com", "https://cmegroup.com/careers", ["cmegroup-com.mail.protection.outlook.com"], True, "SmartRecruiters native careers ecosystem."),
            ("ENT-V6-010", "Rockwell Automation", "rockwellautomation.com", "https://rockwellautomation.com/careers", ["rockwellautomation-com.mail.protection.outlook.com"], True, "Frequent target of lookalike industrial control engineer lures.")
        ]

        for d_id, name, p_dom, url, mx, dmarc, notes in enterprises:
            self.domains[p_dom.lower()] = EnterpriseDomainRecordSix(
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
