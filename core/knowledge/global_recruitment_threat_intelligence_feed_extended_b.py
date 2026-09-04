"""
JobGuard Core Knowledge - Global Recruitment Threat Intelligence Feed Extended Volume B
Maintains active Indicators of Compromise (IoCs) across finance, healthcare, defense,
and energy corporate impersonation vectors, including fraudulent recruiter emails and phone ranges.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class ThreatFeedCategoryB(Enum):
    HEALTHCARE_SCAM_PORTAL = "HEALTHCARE_SCAM_PORTAL"
    FINANCIAL_SERVICES_CLONE = "FINANCIAL_SERVICES_CLONE"
    DEFENSE_CONTRACTOR_LURE = "DEFENSE_CONTRACTOR_LURE"
    REPRESENTATIVE_MULE_TRAP = "REPRESENTATIVE_MULE_TRAP"
    VISA_IMMIGRATION_FRAUD = "VISA_IMMIGRATION_FRAUD"


@dataclass
class ThreatIntelRecordB:
    ioc_id: str
    category: ThreatFeedCategoryB
    indicator_value: str
    targeted_corporation: str
    threat_actor_group: str
    confidence_score: float
    first_seen_timestamp: str
    severity_level: str
    mitigation_guidance: str
    detailed_technical_notes: str


class GlobalRecruitmentThreatIntelligenceFeedExtendedB:
    """Master threat intelligence feed volume B for multi-industry recruitment fraud IoCs."""

    def __init__(self):
        self.feed_database: Dict[str, ThreatIntelRecordB] = {}
        self._seed_threat_feed_b()

    def _seed_threat_feed_b(self) -> None:
        """Populate extensive IoC threat catalog volume B."""

        records_data = [
            (
                "IOC-B-001",
                ThreatFeedCategoryB.HEALTHCARE_SCAM_PORTAL,
                "jnj-medical-talent-careers.com",
                "Johnson & Johnson",
                "Syndicate-HealthPhish",
                0.99,
                "2026-01-08",
                "CRITICAL",
                "Block domain and alert healthcare job boards. Advise applicants of fake clinical data entry offers.",
                "Impersonates Johnson & Johnson HR to distribute counterfeit checks for remote medical data entry workstations."
            ),
            (
                "IOC-B-002",
                ThreatFeedCategoryB.HEALTHCARE_SCAM_PORTAL,
                "pfizer-global-recruitment-portal.org",
                "Pfizer Inc",
                "Syndicate-HealthPhish",
                0.98,
                "2026-01-14",
                "CRITICAL",
                "Inspect incoming email headers for lookalike domain routing. Notify candidate advocacy groups.",
                "Deceptive recruitment portal demanding $150 upfront registration fees for pharmaceutical transcriptionist roles."
            ),
            (
                "IOC-B-003",
                ThreatFeedCategoryB.FINANCIAL_SERVICES_CLONE,
                "jpmorgan-careers-direct-apply.net",
                "JPMorgan Chase & Co",
                "Syndicate-FinClones",
                0.99,
                "2026-01-19",
                "CRITICAL",
                "Flag domain with financial sector ISACs. Issue takedown request to hosting provider.",
                "Clones JPMorgan Chase Workday ATS interface to capture candidate banking credentials and SSNs."
            ),
            (
                "IOC-B-004",
                ThreatFeedCategoryB.FINANCIAL_SERVICES_CLONE,
                "goldmansachs-talent-hiring.info",
                "Goldman Sachs Group Inc",
                "Syndicate-FinClones",
                0.97,
                "2026-01-23",
                "CRITICAL",
                "Warn job seekers against chat-only financial analyst evaluations. Block domain at firewall.",
                "Targets finance graduates with fake remote research offers requiring initial cryptocurrency deposits."
            ),
            (
                "IOC-B-005",
                ThreatFeedCategoryB.DEFENSE_CONTRACTOR_LURE,
                "lockheed-martin-careers-clearance.org",
                "Lockheed Martin Corp",
                "Syndicate-DefenseAPT",
                0.99,
                "2026-01-27",
                "CRITICAL",
                "Report to Defense Counterintelligence and Security Agency (DCSA) and FBI cyber division.",
                "Spearphishing portal targeting defense contractors with weaponized security clearance application PDFs."
            ),
            (
                "IOC-B-006",
                ThreatFeedCategoryB.REPRESENTATIVE_MULE_TRAP,
                "skyline-global-logistics-dispatch.com",
                "Generic Logistics",
                "Syndicate-MuleOps",
                0.96,
                "2026-02-02",
                "HIGH",
                "Instruct victims to cease reshipping packages immediately and contact Postal Inspection Service.",
                "Operates package mule re-shipping schemes under the guise of 'Quality Assurance Merchandiser' positions."
            ),
            (
                "IOC-B-007",
                ThreatFeedCategoryB.VISA_IMMIGRATION_FRAUD,
                "gulf-energy-visas-recruitment.online",
                "Energy & Construction",
                "Apex Syndicate",
                0.98,
                "2026-02-08",
                "CRITICAL",
                "Notify international labor organizations and embassy consular fraud units.",
                "Issues forged employment contracts demanding $2,500 advance visa processing fees for overseas energy jobs."
            )
        ]

        for ioc_id, cat, val, corp, actor, conf, ts, sev, mit, notes in records_data:
            self.feed_database[val.lower()] = ThreatIntelRecordB(
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

    def query_threat_feed(self, indicator: str) -> Optional[ThreatIntelRecordB]:
        clean = indicator.lower().strip()
        if "@" in clean and not clean.startswith("@"):
            clean = clean.split("@")[-1]
        return self.feed_database.get(clean)
