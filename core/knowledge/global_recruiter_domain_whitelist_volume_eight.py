"""
JobGuard Core Knowledge - Global Recruiter Domain Whitelist Master Volume Eight
Expanded directory of verified enterprise domains across consumer electronics,
financial rating agencies, insurance conglomerates, and international logistics providers.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class EnterpriseDomainRecordEight:
    domain_id: str
    company_name: str
    primary_domain: str
    careers_portal_url: str
    verified_mx_hosts: List[str]
    enforces_dmarc_reject: bool
    risk_profile_notes: str


class GlobalRecruiterDomainWhitelistVolumeEight:
    """Master whitelist volume eight covering Fortune 500 insurance, rating, and electronics leaders."""

    def __init__(self):
        self.domains: Dict[str, EnterpriseDomainRecordEight] = {}
        self._seed_volume_eight()

    def _seed_volume_eight() -> None:
        """Register verified enterprise domains."""

        enterprises = [
            ("ENT-V8-001", "Samsung Electronics Co., Ltd.", "samsung.com", "https://samsung.com/careers", ["samsung-com.mail.protection.outlook.com"], True, "High target for fake remote hardware and chip design lures."),
            ("ENT-V8-002", "Moody's Corporation", "moodys.com", "https://careers.moodys.com", ["moodys-com.mail.protection.outlook.com"], True, "Strict DMARC reject enforcement."),
            ("ENT-V8-003", "S&P Global Inc.", "spglobal.com", "https://spglobal.com/careers", ["spglobal-com.mail.protection.outlook.com"], True, "Workday ATS integration with strict origin validation."),
            ("ENT-V8-004", "The Progressive Corporation", "progressive.com", "https://progressive.com/careers", ["progressive-com.mail.protection.outlook.com"], True, "Enterprise applicant authentication."),
            ("ENT-V8-005", "The Allstate Corporation", "allstate.com", "https://allstate.jobs", ["allstate-com.mail.protection.outlook.com"], True, "Multi-factor authentication on applicant portals."),
            ("ENT-V8-006", "Prudential Financial Inc.", "prudential.com", "https://jobs.prudential.com", ["prudential-com.mail.protection.outlook.com"], True, "Targeted by lookalike financial analyst lures."),
            ("ENT-V8-007", "MetLife Inc.", "metlife.com", "https://metlife.com/careers", ["metlife-com.mail.protection.outlook.com"], True, "Strict hiring portal authentication."),
            ("ENT-V8-008", "AIG (American International Group)", "aig.com", "https://aig.com/careers", ["aig-com.mail.protection.outlook.com"], True, "Enterprise Workday deployment."),
            ("ENT-V8-009", "DHL Group / Deutsche Post", "dhl.com", "https://careers.dhl.com", ["dhl-com.mail.protection.outlook.com"], True, "Frequent target of package reshipping mule scams."),
            ("ENT-V8-010", "United Parcel Service (UPS)", "ups.com", "https://jobs-ups.com", ["ups-com.mail.protection.outlook.com"], True, "Frequent target of package reshipping mule scams.")
        ]

        for d_id, name, p_dom, url, mx, dmarc, notes in enterprises:
            self.domains[p_dom.lower()] = EnterpriseDomainRecordEight(
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
