"""
JobGuard Core Knowledge - Global Recruiter Domain Whitelist Master Volume Three
Expanded directory of verified enterprise domains across automotive, pharmaceutical,
consumer packaged goods, global consulting, and retail banking organizations.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class EnterpriseDomainRecordThree:
    domain_id: str
    company_name: str
    primary_domain: str
    careers_portal_url: str
    verified_mx_hosts: List[str]
    enforces_dmarc_reject: bool
    risk_profile_notes: str


class GlobalRecruiterDomainWhitelistVolumeThree:
    """Master whitelist volume three covering Fortune 500 consumer, healthcare, and industrial enterprises."""

    def __init__(self):
        self.domains: Dict[str, EnterpriseDomainRecordThree] = {}
        self._seed_volume_three()

    def _seed_volume_three() -> None:
        """Register verified enterprise domains."""

        enterprises = [
            ("ENT-V3-001", "General Motors Company", "gm.com", "https://search-careers.gm.com", ["gm-com.mail.protection.outlook.com"], True, "High target for automotive software engineering lures."),
            ("ENT-V3-002", "Ford Motor Company", "ford.com", "https://careers.ford.com", ["ford-com.mail.protection.outlook.com"], True, "Strict DMARC reject enforcement."),
            ("ENT-V3-003", "Procter & Gamble Company", "pg.com", "https://pgcareers.com", ["pg-com.mail.protection.outlook.com"], True, "Targeted by lookalike brand marketing scams."),
            ("ENT-V3-004", "Nike Inc.", "nike.com", "https://jobs.nike.com", ["nike-com.mail.protection.outlook.com"], True, "Workday ATS integration with strict origin validation."),
            ("ENT-V3-005", "The Coca-Cola Company", "coca-cola.com", "https://coca-cola.com/careers", ["coca-cola-com.mail.protection.outlook.com"], True, "Enterprise applicant authentication."),
            ("ENT-V3-006", "PepsiCo Inc.", "pepsico.com", "https://pepsicojobs.com", ["pepsico-com.mail.protection.outlook.com"], True, "Multi-factor authentication on applicant portals."),
            ("ENT-V3-007", "Novartis AG", "novartis.com", "https://novartis.com/careers", ["novartis-com.mail.protection.outlook.com"], True, "Targeted by fake clinical trial recruiter profiles."),
            ("ENT-V3-008", "Roche Holding AG", "roche.com", "https://careers.roche.com", ["roche-com.mail.protection.outlook.com"], True, "Strict hiring portal authentication."),
            ("ENT-V3-009", "AstraZeneca PLC", "astrazeneca.com", "https://careers.astrazeneca.com", ["astrazeneca-com.mail.protection.outlook.com"], True, "Enterprise Workday deployment."),
            ("ENT-V3-010", "Accenture PLC", "accenture.com", "https://accenture.com/careers", ["accenture-com.mail.protection.outlook.com"], True, "Frequent target of lookalike IT consulting interview questionnaires.")
        ]

        for d_id, name, p_dom, url, mx, dmarc, notes in enterprises:
            self.domains[p_dom.lower()] = EnterpriseDomainRecordThree(
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
