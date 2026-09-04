"""
JobGuard Core Knowledge - Global Recruitment Threat Intelligence Feed Extended Volume A
Maintains high-fidelity Indicators of Compromise (IoCs), known phishing campaign clusters,
typosquatted domains, and malicious recruiter profiles targeting global technology enterprises.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class ThreatFeedCategoryA(Enum):
    PHISHING_INFRASTRUCTURE = "PHISHING_INFRASTRUCTURE"
    COUNTERFEIT_CHECK_RING = "COUNTERFEIT_CHECK_RING"
    TASK_OPTIMIZATION_SCAM = "TASK_OPTIMIZATION_SCAM"
    IMPERSONATED_EXECUTIVE = "IMPERSONATED_EXECUTIVE"
    MALICIOUS_ASSESSMENT_LURE = "MALICIOUS_ASSESSMENT_LURE"


@dataclass
class ThreatIntelRecordA:
    ioc_id: str
    category: ThreatFeedCategoryA
    indicator_value: str
    targeted_corporation: str
    threat_actor_group: str
    confidence_score: float
    first_seen_timestamp: str
    severity_level: str
    mitigation_guidance: str
    detailed_technical_notes: str


class GlobalRecruitmentThreatIntelligenceFeedExtendedA:
    """Master threat intelligence feed volume A for active recruitment fraud signatures."""

    def __init__(self):
        self.feed_database: Dict[str, ThreatIntelRecordA] = {}
        self._seed_threat_feed()

    def _seed_threat_feed(self) -> None:
        """Populate extensive IoC threat catalog volume A."""

        records_data = [
            (
                "IOC-A-001",
                ThreatFeedCategoryA.PHISHING_INFRASTRUCTURE,
                "careers-google-verify-auth.com",
                "Google LLC",
                "Syndicate-Alpha",
                0.99,
                "2026-01-10",
                "CRITICAL",
                "Block domain across corporate and consumer DNS resolvers. Revoke any submitted credentials.",
                "Fake Greenhouse ATS landing page configured to capture Google OAuth tokens and candidate PII."
            ),
            (
                "IOC-A-002",
                ThreatFeedCategoryA.PHISHING_INFRASTRUCTURE,
                "microsoft-talent-portal-apply.net",
                "Microsoft Corporation",
                "Syndicate-Alpha",
                0.98,
                "2026-01-12",
                "CRITICAL",
                "Blacklist domain and inspect mail gateway logs for inbound recruiter lures.",
                "Lookalike domain hosting deceptive Teams chat questionnaires for home office equipment fraud."
            ),
            (
                "IOC-A-003",
                ThreatFeedCategoryA.PHISHING_INFRASTRUCTURE,
                "amazon-workforce-onboarding-desk.org",
                "Amazon.com Inc",
                "Syndicate-Beta",
                0.99,
                "2026-01-15",
                "CRITICAL",
                "Block incoming SMTP traffic originating from associated nameserver clusters.",
                "Impersonates Amazon HR talent acquisition to extract upfront background check fees."
            ),
            (
                "IOC-A-004",
                ThreatFeedCategoryA.COUNTERFEIT_CHECK_RING,
                "certified-homeoffice-procurement.net",
                "Generic Enterprise",
                "Syndicate-CheckRing",
                0.99,
                "2026-01-18",
                "CRITICAL",
                "Flag any wire transfer instructions pointing to account holders on this host.",
                "Counterfeit vendor storefront utilized to receive check surplus wire payments."
            ),
            (
                "IOC-A-005",
                ThreatFeedCategoryA.COUNTERFEIT_CHECK_RING,
                "apex-it-hardware-dispatch.org",
                "Generic Enterprise",
                "Syndicate-CheckRing",
                0.97,
                "2026-01-20",
                "CRITICAL",
                "Notify bank fraud departments of fake check deposits referencing this entity.",
                "Shell company setup to facilitate wire kickbacks following counterfeit check deposits."
            ),
            (
                "IOC-A-006",
                ThreatFeedCategoryA.TASK_OPTIMIZATION_SCAM,
                "opt-cloud-boost-vip.top",
                "Generic Brand",
                "Syndicate-CryptoRing",
                0.99,
                "2026-01-22",
                "CRITICAL",
                "Advise victims to cease all cryptocurrency transfers immediately. Report wallet addresses.",
                "USDT recharge task rating scheme promising $500/day for reviewing hotel reservations."
            ),
            (
                "IOC-A-007",
                ThreatFeedCategoryA.TASK_OPTIMIZATION_SCAM,
                "app-store-rating-vip.club",
                "Generic Brand",
                "Syndicate-CryptoRing",
                0.98,
                "2026-01-25",
                "CRITICAL",
                "Block domain and trace TRC-20 smart contract deposit addresses.",
                "Tiered VIP commission drainer requiring users to deposit crypto to reset negative balances."
            ),
            (
                "IOC-A-008",
                ThreatFeedCategoryA.IMPERSONATED_EXECUTIVE,
                "@google_vp_talent_acquisition",
                "Google LLC",
                "Syndicate-Alpha",
                0.96,
                "2026-01-28",
                "HIGH",
                "Verify executive identity through official corporate directory. Cease Telegram messaging.",
                "Telegram handle impersonating senior corporate executive to conduct text-only hiring."
            ),
            (
                "IOC-A-009",
                ThreatFeedCategoryA.IMPERSONATED_EXECUTIVE,
                "@microsoft_recruiting_lead_sarah",
                "Microsoft Corporation",
                "Syndicate-Alpha",
                0.95,
                "2026-02-01",
                "HIGH",
                "Demand live video verification on Microsoft Teams. Refuse text questionnaires.",
                "Spoofed recruiter profile operating scripted questionnaires to collect banking data."
            ),
            (
                "IOC-A-010",
                ThreatFeedCategoryA.MALICIOUS_ASSESSMENT_LURE,
                "https://github.com/tech-recruitment-tests/react-takehome-2026",
                "Tech Startups",
                "Lazarus Group",
                "0.99",
                "2026-02-05",
                "CRITICAL",
                "Audit package.json preinstall hooks and isolate repository in ephemeral container.",
                "Take-home assessment repository containing malicious npm dependency designed to steal SSH keys."
            )
        ]

        for ioc_id, cat, val, corp, actor, conf, ts, sev, mit, notes in records_data:
            self.feed_database[val.lower()] = ThreatIntelRecordA(
                ioc_id=ioc_id,
                category=cat,
                indicator_value=val,
                targeted_corporation=corp,
                threat_actor_group=actor,
                confidence_score=float(conf),
                first_seen_timestamp=ts,
                severity_level=sev,
                mitigation_guidance=mit,
                detailed_technical_notes=notes
            )

    def query_threat_feed(self, indicator: str) -> Optional[ThreatIntelRecordA]:
        """Queries the extended threat feed for domain, URL, or handle matches."""
        clean = indicator.lower().strip()
        if "@" in clean and not clean.startswith("@"):
            clean = clean.split("@")[-1]
        return self.feed_database.get(clean)
