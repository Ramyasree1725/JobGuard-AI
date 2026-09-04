"""
JobGuard Core Security - Comprehensive MITRE ATT&CK Recruitment Threat Mappings Large
Exhaustive matrix mapping enterprise MITRE ATT&CK enterprise tactics, techniques, and procedures (TTPs)
to advanced recruitment fraud, executive impersonation, and social engineering operations.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class MITRETactic(Enum):
    TA0001_INITIAL_ACCESS = "TA0001_INITIAL_ACCESS"
    TA0002_EXECUTION = "TA0002_EXECUTION"
    TA0003_PERSISTENCE = "TA0003_PERSISTENCE"
    TA0005_DEFENSE_EVASION = "TA0005_DEFENSE_EVASION"
    TA0006_CREDENTIAL_ACCESS = "TA0006_CREDENTIAL_ACCESS"
    TA0007_DISCOVERY = "TA0007_DISCOVERY"
    TA0009_COLLECTION = "TA0009_COLLECTION"
    TA0010_EXFILTRATION = "TA0010_EXFILTRATION"
    TA0040_IMPACT = "TA0040_IMPACT"


@dataclass
class MITREAttackMappingRecord:
    technique_id: str
    subtechnique_id: Optional[str]
    tactic: MITRETactic
    technique_name: str
    recruitment_fraud_context: str
    detection_rule_signature: str
    defensive_countermeasure: str
    threat_actor_attribution_tags: List[str]


class MITREAttackRecruitmentThreatMappingsLarge:
    """Master expanded MITRE ATT&CK taxonomy for employment cybersecurity."""

    def __init__(self):
        self.mappings: Dict[str, MITREAttackMappingRecord] = {}
        self._initialize_mappings()

    def _initialize_mappings(self) -> None:
        """Register comprehensive MITRE ATT&CK enterprise recruitment fraud mappings."""

        entries = [
            (
                "T1566",
                "T1566.001",
                MITRETactic.TA0001_INITIAL_ACCESS,
                "Spearphishing Attachment via Fake Interview PDF",
                "Delivering malicious weaponized PDF contracts containing zero-day exploits or macro-enabled assessment forms.",
                r"(?:open|enable\s+macros|run)\s+(?:attached|enclosed)\s+(?:form|application|docm)",
                "Sandbox detonation and automated PDF stream parsing before opening attachments.",
                ["APT29", "Lazarus Group", "SilverPhish"]
            ),
            (
                "T1566",
                "T1566.002",
                MITRETactic.TA0001_INITIAL_ACCESS,
                "Spearphishing Link to Fake ATS Application Portal",
                "Sending direct URLs to fraudulent ATS clones (e.g. greenhouse-careers.info) to harvest candidate credentials.",
                r"https?://(?:[a-zA-Z0-9-]+\.)*(?:boards-greenhouse|jobs-lever|workday-careers)-[a-z0-9]+\.[a-z]{2,}",
                "Automated DNS lookalike resolution and domain age inspection (<30 days).",
                ["Syndicate-Alpha", "FIN7", "ScamOps-Global"]
            ),
            (
                "T1586",
                "T1586.002",
                MITRETactic.TA0001_INITIAL_ACCESS,
                "Compromised / Impersonated Social Media Recruiter Accounts",
                "Creating high-reputation fake LinkedIn profiles posing as senior talent acquisition partners to establish trust.",
                r"linkedin\.com/in/[a-zA-Z0-9_-]+.*(?:recruiter|talent\s+partner|head\s+of\s+hiring)",
                "Cross-referencing recruiter profile against official company directory and employee list.",
                ["Syndicate-Beta", "Lazarus Group"]
            ),
            (
                "T1204",
                "T1204.002",
                MITRETactic.TA0002_EXECUTION,
                "User Execution of Malicious Assessment Code Repository",
                "Instructing software engineering candidates to clone git repositories containing backdoor pre-install scripts.",
                r"(?:git\s+clone|npm\s+install|cargo\s+build|pip\s+install)\s+.*(?:test|take-home|assessment)",
                "Static analysis of package.json scripts and execution only in containerized ephemeral sandboxes.",
                ["Lazarus Group", "DevScam Network"]
            ),
            (
                "T1036",
                "T1036.005",
                MITRETactic.TA0005_DEFENSE_EVASION,
                "Masquerading Match Legitimate Corporate Naming Hierarchy",
                "Using Unicode homoglyphs, visual confusable characters, and deceptive subdomains to mimic genuine enterprises.",
                r"[а-яА-Я].*(?:google|microsoft|amazon|apple)|[0-9].*(?:g00gle|micr0s0ft)",
                "Cyrillic-Latin homoglyph mapping and punycode decoding algorithms.",
                ["Syndicate-Alpha", "Apex Syndicate"]
            ),
            (
                "T1056",
                "T1056.003",
                MITRETactic.TA0006_CREDENTIAL_ACCESS,
                "Web Form Credential & Identity Dossier Exfiltration",
                "Embedding unauthorized web forms to collect Social Security Numbers, passports, and online banking credentials.",
                r"(?:social\s+security|passport|banking\s+pin)\s*:\s*<input",
                "Form action endpoint reputation auditing and Zero-Trust credential policies.",
                ["FIN11", "IdentityTheft Syndicate"]
            ),
            (
                "T1657",
                None,
                MITRETactic.TA0040_IMPACT,
                "Financial Fraud via Counterfeit Check Kickbacks",
                "Executing advance check overpayment schemes to induce victims into wiring personal funds to money mules.",
                r"(?:deposit\s+check|wire\s+surplus|forward\s+remaining\s+balance)",
                "Real-time heuristic check detection and immediate banking alert issuance.",
                ["SilverPhish", "Apex Syndicate", "WestAfrican-BEC"]
            )
        ]

        for t_id, sub_id, tactic, name, ctx, sig, counter, tags in entries:
            key = sub_id or t_id
            record = MITREAttackMappingRecord(
                technique_id=t_id,
                subtechnique_id=sub_id,
                tactic=tactic,
                technique_name=name,
                recruitment_fraud_context=ctx,
                detection_rule_signature=sig,
                defensive_countermeasure=counter,
                threat_actor_attribution_tags=tags
            )
            self.mappings[key] = record

    def get_mapping(self, technique_or_subtechnique_id: str) -> Optional[MITREAttackMappingRecord]:
        return self.mappings.get(technique_or_subtechnique_id)
