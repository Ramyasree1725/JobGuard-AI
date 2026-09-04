"""
JobGuard Core Network - Email Infrastructure & Anti-Spoofing Auditor
Audits Sender Policy Framework (SPF), DomainKeys Identified Mail (DKIM),
and Domain-based Message Authentication, Reporting & Conformance (DMARC) configurations.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import re


class DMARCPolicy(Enum):
    REJECT = "REJECT"
    QUARANTINE = "QUARANTINE"
    NONE = "NONE"
    MISSING = "MISSING"


class SPFQualifier(Enum):
    PASS_ALL = "PASS_ALL"      # +all (Dangerous)
    SOFTFAIL = "SOFTFAIL"      # ~all
    FAIL = "FAIL"              # -all (Strict)
    NEUTRAL = "NEUTRAL"        # ?all
    MISSING = "MISSING"


@dataclass
class EmailSecurityAudit:
    domain_name: str
    spf_record: Optional[str]
    spf_qualifier: SPFQualifier
    has_dkim: bool
    dmarc_record: Optional[str]
    dmarc_policy: DMARCPolicy
    is_spoofable: bool
    email_trust_score: float  # 0 (completely unauthenticated) to 100 (hardened)
    vulnerabilities: List[str]
    advisory_recommendation: str


class EmailInfrastructureAuditor:
    """Evaluates whether an alleged employer's domain is vulnerable to email sender spoofing."""

    def __init__(self):
        pass

    def parse_spf(self, txt_records: List[str]) -> Tuple[Optional[str], SPFQualifier]:
        """Extracts and parses SPF record qualifier mechanisms."""
        spf_str = None
        for txt in txt_records:
            if txt.strip().startswith("v=spf1"):
                spf_str = txt.strip()
                break

        if not spf_str:
            return None, SPFQualifier.MISSING

        if "-all" in spf_str:
            return spf_str, SPFQualifier.FAIL
        elif "~all" in spf_str:
            return spf_str, SPFQualifier.SOFTFAIL
        elif "+all" in spf_str:
            return spf_str, SPFQualifier.PASS_ALL
        elif "?all" in spf_str:
            return spf_str, SPFQualifier.NEUTRAL

        return spf_str, SPFQualifier.SOFTFAIL

    def parse_dmarc(self, dmarc_txt_records: List[str]) -> Tuple[Optional[str], DMARCPolicy]:
        """Extracts and parses DMARC policy tags."""
        dmarc_str = None
        for txt in dmarc_txt_records:
            if "v=DMARC1" in txt:
                dmarc_str = txt.strip()
                break

        if not dmarc_str:
            return None, DMARCPolicy.MISSING

        match = re.search(r"p=(reject|quarantine|none)", dmarc_str, re.IGNORECASE)
        if match:
            pol = match.group(1).upper()
            return dmarc_str, DMARCPolicy(pol)

        return dmarc_str, DMARCPolicy.NONE

    def audit_domain_email_security(
        self,
        domain: str,
        txt_records: List[str],
        dmarc_records: List[str],
        has_dkim_selector: bool = True
    ) -> EmailSecurityAudit:
        """Runs full cryptographic and policy validation for corporate email channels."""
        spf_raw, spf_qual = self.parse_spf(txt_records)
        dmarc_raw, dmarc_pol = self.parse_dmarc(dmarc_records)

        vulnerabilities: List[str] = []
        trust_score = 100.0

        # Check SPF
        if spf_qual == SPFQualifier.MISSING:
            vulnerabilities.append("Missing SPF record: Anyone on the Internet can send emails claiming to be from this domain.")
            trust_score -= 35.0
        elif spf_qual == SPFQualifier.PASS_ALL:
            vulnerabilities.append("Critical SPF misconfiguration: '+all' explicitly authorizes all IP addresses worldwide to send mail.")
            trust_score -= 40.0
        elif spf_qual in (SPFQualifier.NEUTRAL, SPFQualifier.SOFTFAIL):
            trust_score -= 10.0

        # Check DMARC
        if dmarc_pol == DMARCPolicy.MISSING:
            vulnerabilities.append("Missing DMARC record: Mail servers cannot verify alignment or reject unauthorized spoofed messages.")
            trust_score -= 40.0
        elif dmarc_pol == DMARCPolicy.NONE:
            vulnerabilities.append("DMARC policy is set to 'p=none' (monitoring only); spoofed messages will still be delivered to victim inboxes.")
            trust_score -= 20.0

        # Check DKIM
        if not has_dkim_selector:
            vulnerabilities.append("No active DKIM selector signature detected.")
            trust_score -= 15.0

        is_spoofable = (dmarc_pol in (DMARCPolicy.MISSING, DMARCPolicy.NONE)) and (spf_qual in (SPFQualifier.MISSING, SPFQualifier.PASS_ALL, SPFQualifier.NEUTRAL))

        trust_score = max(0.0, min(100.0, trust_score))

        if is_spoofable:
            adv = "CRITICAL: Domain is vulnerable to direct sender email spoofing. Attackers can forge recruitment emails appearing to originate from this domain."
        elif trust_score < 70.0:
            adv = "WARNING: Email authentication policies are weak. Verify sender headers using message trace."
        else:
            adv = "Domain email infrastructure is properly secured with strict SPF and DMARC enforcement."

        return EmailSecurityAudit(
            domain_name=domain,
            spf_record=spf_raw,
            spf_qualifier=spf_qual,
            has_dkim=has_dkim_selector,
            dmarc_record=dmarc_raw,
            dmarc_policy=dmarc_pol,
            is_spoofable=is_spoofable,
            email_trust_score=trust_score,
            vulnerabilities=vulnerabilities if vulnerabilities else ["Hardened email authentication."],
            advisory_recommendation=adv
        )
