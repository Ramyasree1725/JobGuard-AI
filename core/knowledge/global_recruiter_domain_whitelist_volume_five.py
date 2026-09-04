"""
JobGuard Core Knowledge - Global Recruiter Domain Whitelist Master Volume Five
Expanded directory of verified enterprise domains across defense, cybersecurity,
semiconductor manufacturing, enterprise database, and cloud infrastructure companies.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class EnterpriseDomainRecordFive:
    domain_id: str
    company_name: str
    primary_domain: str
    careers_portal_url: str
    verified_mx_hosts: List[str]
    enforces_dmarc_reject: bool
    risk_profile_notes: str


class GlobalRecruiterDomainWhitelistVolumeFive:
    """Master whitelist volume five covering global cybersecurity, cloud, and semiconductor leaders."""

    def __init__(self):
        self.domains: Dict[str, EnterpriseDomainRecordFive] = {}
        self._seed_volume_five()

    def _seed_volume_five() -> None:
        """Register verified enterprise domains."""

        enterprises = [
            ("ENT-V5-001", "Palo Alto Networks Inc.", "paloaltonetworks.com", "https://jobs.paloaltonetworks.com", ["paloaltonetworks-com.mail.protection.outlook.com"], True, "High target for fake security engineering offers."),
            ("ENT-V5-002", "CrowdStrike Holdings Inc.", "crowdstrike.com", "https://crowdstrike.com/careers", ["crowdstrike-com.mail.protection.outlook.com"], True, "Strict DMARC reject enforcement."),
            ("ENT-V5-003", "Fortinet Inc.", "fortinet.com", "https://fortinet.com/careers", ["fortinet-com.mail.protection.outlook.com"], True, "Workday ATS integration with strict origin validation."),
            ("ENT-V5-004", "Cloudflare Inc.", "cloudflare.com", "https://cloudflare.com/careers", ["cloudflare-com.mail.protection.outlook.com"], True, "Enterprise applicant authentication."),
            ("ENT-V5-005", "Zscaler Inc.", "zscaler.com", "https://zscaler.com/careers", ["zscaler-com.mail.protection.outlook.com"], True, "Multi-factor authentication on applicant portals."),
            ("ENT-V5-006", "Applied Materials Inc.", "appliedmaterials.com", "https://appliedmaterials.com/careers", ["appliedmaterials-com.mail.protection.outlook.com"], True, "Targeted by lookalike semiconductor engineer lures."),
            ("ENT-V5-007", "Lam Research Corporation", "lamresearch.com", "https://careers.lamresearch.com", ["lamresearch-com.mail.protection.outlook.com"], True, "Strict hiring portal authentication."),
            ("ENT-V5-008", "ASML Holding N.V.", "asml.com", "https://asml.com/careers", ["asml-com.mail.protection.outlook.com"], True, "Enterprise Workday deployment."),
            ("ENT-V5-009", "Synopsys Inc.", "synopsys.com", "https://synopsys.com/careers", ["synopsys-com.mail.protection.outlook.com"], True, "SmartRecruiters native careers ecosystem."),
            ("ENT-V5-010", "Cadence Design Systems", "cadence.com", "https://cadence.com/careers", ["cadence-com.mail.protection.outlook.com"], True, "Frequent target of lookalike EDA software engineer lures.")
        ]

        for d_id, name, p_dom, url, mx, dmarc, notes in enterprises:
            self.domains[p_dom.lower()] = EnterpriseDomainRecordFive(
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
