"""
JobGuard Core Knowledge - Global Recruiter Domain Whitelist Master Volume Four
Expanded directory of verified enterprise domains across telecommunications,
cloud computing, financial market infrastructure, and energy corporations.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class EnterpriseDomainRecordFour:
    domain_id: str
    company_name: str
    primary_domain: str
    careers_portal_url: str
    verified_mx_hosts: List[str]
    enforces_dmarc_reject: bool
    risk_profile_notes: str


class GlobalRecruiterDomainWhitelistVolumeFour:
    """Master whitelist volume four covering Fortune 500 telecommunications, cloud, and energy enterprises."""

    def __init__(self):
        self.domains: Dict[str, EnterpriseDomainRecordFour] = {}
        self._seed_volume_four()

    def _seed_volume_four() -> None:
        """Register verified enterprise domains."""

        enterprises = [
            ("ENT-V4-001", "Verizon Communications Inc.", "verizon.com", "https://verizon.com/about/careers", ["verizon-com.mail.protection.outlook.com"], True, "High target for fake network engineering remote contracts."),
            ("ENT-V4-002", "AT&T Inc.", "att.com", "https://att.jobs", ["att-com.mail.protection.outlook.com"], True, "Strict DMARC reject enforcement."),
            ("ENT-V4-003", "Comcast Corporation", "comcast.com", "https://jobs.comcast.com", ["comcast-com.mail.protection.outlook.com"], True, "Workday ATS integration with strict origin validation."),
            ("ENT-V4-004", "T-Mobile US Inc.", "t-mobile.com", "https://t-mobile.com/careers", ["t-mobile-com.mail.protection.outlook.com"], True, "Enterprise applicant authentication."),
            ("ENT-V4-005", "Charter Communications Inc.", "charter.com", "https://jobs.spectrum.com", ["charter-com.mail.protection.outlook.com"], True, "Multi-factor authentication on applicant portals."),
            ("ENT-V4-006", "Exxon Mobil Corporation", "exxonmobil.com", "https://corporate.exxonmobil.com/careers", ["exxonmobil-com.mail.protection.outlook.com"], True, "Targeted by lookalike overseas offshore drilling contracts."),
            ("ENT-V4-007", "Chevron Corporation", "chevron.com", "https://chevron.com/careers", ["chevron-com.mail.protection.outlook.com"], True, "Strict hiring portal authentication."),
            ("ENT-V4-008", "ConocoPhillips", "conocophillips.com", "https://conocophillips.com/careers", ["conocophillips-com.mail.protection.outlook.com"], True, "Enterprise Workday deployment."),
            ("ENT-V4-009", "ServiceNow Inc.", "servicenow.com", "https://servicenow.com/careers", ["servicenow-com.mail.protection.outlook.com"], True, "SmartRecruiters native careers ecosystem."),
            ("ENT-V4-010", "Snowflake Inc.", "snowflake.com", "https://snowflake.com/careers", ["snowflake-com.mail.protection.outlook.com"], True, "Frequent target of lookalike data engineering lures.")
        ]

        for d_id, name, p_dom, url, mx, dmarc, notes in enterprises:
            self.domains[p_dom.lower()] = EnterpriseDomainRecordFour(
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
