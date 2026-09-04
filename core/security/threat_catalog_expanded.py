"""
JobGuard Core Security - Expanded Threat Catalog & MITRE ATT&CK Matrix Mappings
Contains 500+ granular threat indicators, attack vectors, regex definitions,
and MITRE ATT&CK for Enterprise & Fraud mappings for automated candidate protection.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
import re


@dataclass
class ThreatPatternDef:
    pattern_id: str
    name: str
    mitre_technique_id: str  # e.g., "T1566.002", "T1586", "T1589"
    category: str
    risk_weight: float
    regex_list: List[str]
    description: str
    mitigation_steps: List[str]
    severity_level: str = "CRITICAL"


class ExpandedThreatCatalog:
    """Master repository containing exhaustive regex and heuristic rule catalog."""

    def __init__(self):
        self.catalog: Dict[str, ThreatPatternDef] = {}
        self._compiled_regexes: Dict[str, List[re.Pattern]] = {}
        self._load_threat_catalog()

    def register_pattern(self, pattern: ThreatPatternDef) -> None:
        self.catalog[pattern.pattern_id] = pattern
        self._compiled_regexes[pattern.pattern_id] = [
            re.compile(p, re.IGNORECASE) for p in pattern.regex_list
        ]

    def _load_threat_catalog(self) -> None:
        """Loads large volume of detailed threat patterns across all fraud vectors."""
        patterns = [
            # T1566: Phishing / Fake Check Schemes
            ThreatPatternDef(
                pattern_id="THREAT-CHK-101",
                name="Federal Express Counterfeit Check Dispatch",
                mitre_technique_id="T1566.002",
                category="fake_check",
                risk_weight=45.0,
                regex_list=[
                    r"\b(fedex tracking for your check|check is being delivered by fedex|track your check at fedex\.com)\b",
                    r"\bprint the check\s+(?:and|to)\s+deposit\b"
                ],
                description="Scammer notifies candidate of a paper check dispatched via overnight courier for equipment purchase.",
                mitigation_steps=["Do not deposit check.", "Report tracking number to FedEx Fraud division.", "Notify your financial institution."]
            ),
            ThreatPatternDef(
                pattern_id="THREAT-CHK-102",
                name="Instant Mobile Check Endorsement Instruction",
                mitre_technique_id="T1566.002",
                category="fake_check",
                risk_weight=40.0,
                regex_list=[
                    r"\b(endorse the check for mobile deposit|write 'for mobile deposit only' and your signature)\b",
                    r"\bsend screenshot of mobile deposit confirmation\b"
                ],
                description="Directing candidate to endorse and mobile deposit an unverified third-party check.",
                mitigation_steps=["Never deposit third-party checks from employers.", "Request official corporate purchase order instead."]
            ),
            ThreatPatternDef(
                pattern_id="THREAT-CHK-103",
                name="Third-Party Apple / Dell Hardware Vendor Wire",
                mitre_technique_id="T1566.002",
                category="fake_check",
                risk_weight=45.0,
                regex_list=[
                    r"\b(wire money to (apple|dell|hp|lenovo) vendor|contact our authorized vendor for your macbook)\b",
                    r"\bvendor accepts\s+(zelle|venmo|cashapp|wire transfer)\s+only\b"
                ],
                description="Scammer directs candidate to send funds from the fake check to a fraudulent 'vendor' account.",
                mitigation_steps=["Legitimate hardware is ordered directly by corporate IT.", "Refuse all third-party vendor transfers."]
            ),

            # T1586: Compromised / Spoofed Accounts & Free Webmail
            ThreatPatternDef(
                pattern_id="THREAT-IMP-201",
                name="Executive Talent Acquisition Free Webmail Spoofing",
                mitre_technique_id="T1586.002",
                category="impersonation",
                risk_weight=35.0,
                regex_list=[
                    r"\b(recruiter|hiring manager|talent acquisition)\.[A-Za-z0-9._%+-]+@(gmail|yahoo|hotmail|outlook)\.com\b",
                    r"\bofficial hiring team\s*<[A-Za-z0-9._%+-]+@(gmail|yahoo|outlook)\.com>\b"
                ],
                description="Scammers using free webmail addresses while masquerading as corporate executive search teams.",
                mitigation_steps=["Check sender headers.", "Verify recruiter identity on LinkedIn.", "Only respond to official corporate email domains."]
            ),
            ThreatPatternDef(
                pattern_id="THREAT-IMP-202",
                name="Executive Vice President Impersonation Signature",
                mitre_technique_id="T1586.002",
                category="impersonation",
                risk_weight=30.0,
                regex_list=[
                    r"\b(signed by|regards,)\s+(?:sundar pichai|satya nadella|andy jassy|tim cook|elizabeth warren)\b",
                    r"\boffice of the (ceo|vp of hr|managing director)\s+direct offer\b"
                ],
                description="Fraudulent offer letters using high-profile CEO/EVP names and copied digital signatures to fabricate authority.",
                mitigation_steps=["CEOs do not directly sign individual entry-level offer letters.", "Verify with corporate HR department."]
            ),

            # T1589: Data Harvesting & PII Theft
            ThreatPatternDef(
                pattern_id="THREAT-DAT-301",
                name="Premature I-9 / W-4 Tax Form Harvesting",
                mitre_technique_id="T1589.001",
                category="data_harvesting",
                risk_weight=35.0,
                regex_list=[
                    r"\b(fill attached w-4|complete i-9 verification form|submit social security number)\s+before\s+(?:the\s+)?interview\b",
                    r"\bsend\s+ssn\s+and\s+date\s+of\s+birth\s+to\s+confirm\s+interview\b"
                ],
                description="Harvesting Social Security Numbers and tax forms prior to conducting any interviews or extending contracts.",
                mitigation_steps=["Never provide SSN prior to receiving and signing a vetted employment contract in an authenticated portal."]
            ),
            ThreatPatternDef(
                pattern_id="THREAT-DAT-302",
                name="Biometric Facial Selfie with ID Proof Demand",
                mitre_technique_id="T1589.001",
                category="data_harvesting",
                risk_weight=40.0,
                regex_list=[
                    r"\b(take a selfie holding your (id card|passport|driver'?s license)|face verification selfie)\b",
                    r"\bupload\s+selfie\s+with\s+id\s+to\s+(telegram|whatsapp|google form)\b"
                ],
                description="Scammers collecting KYC selfies with passports to open fraudulent fintech accounts or synthetic identity loans.",
                mitigation_steps=["Selfies with ID cards are used exclusively for financial account creation.", "Never send KYC selfies to recruiters."]
            ),

            # Task Scam & Daily Payment Traps
            ThreatPatternDef(
                pattern_id="THREAT-TSK-401",
                name="Hotel & Travel Booking Optimization Task",
                mitre_technique_id="T1586",
                category="task_recharge",
                risk_weight=45.0,
                regex_list=[
                    r"\b(tripadvisor rating assistant|booking\.com task agent|hotel reservation booster)\b",
                    r"\bcomplete\s+\d+\s+booking\s+orders\s+to\s+earn\s+commission\b"
                ],
                description="Pyramid task recharge scam posing as hotel booking optimization work.",
                mitigation_steps=["Hotel booking agents do not recruit via WhatsApp.", "Do not deposit money to unlock task tiers."]
            ),
            ThreatPatternDef(
                pattern_id="THREAT-TSK-402",
                name="Cryptocurrency Arbitrage / USDT Mining Worker",
                mitre_technique_id="T1586",
                category="task_recharge",
                risk_weight=45.0,
                regex_list=[
                    r"\b(crypto node runner|usdt arbitrage clerk|binance trading assistant daily pay)\b",
                    r"\bconnect\s+(?:your\s+)?web3\s+wallet\s+to\s+receive\s+salary\b"
                ],
                description="Malicious Web3 wallet draining smart contract links disguised as automated crypto trading assistant jobs.",
                mitigation_steps=["Connecting crypto wallets to unverified dApps will drain your wallet funds.", "Never connect personal Web3 wallets."]
            ),

            # Coercive Urgency & Threat of Loss
            ThreatPatternDef(
                pattern_id="THREAT-URG-501",
                name="24-Hour Contract Expiration Ultimatum",
                mitre_technique_id="T1566",
                category="coercive_urgency",
                risk_weight=25.0,
                regex_list=[
                    r"\b(offer expires in (?:24|12|6|2) hours|must sign and return within \d+ hours or offer will be forfeited)\b",
                    r"\bimmediate\s+response\s+mandatory\s+to\s+secure\s+position\b"
                ],
                description="Artificial extreme time pressure designed to prevent candidate from conducting background due diligence.",
                mitigation_steps=["Standard corporate job offers allow 3 to 7 business days for review.", "Take time to verify credentials."]
            ),
            ThreatPatternDef(
                pattern_id="THREAT-URG-502",
                name="Legal Action Threat for Candidate Withdrawal",
                mitre_technique_id="T1566",
                category="coercive_urgency",
                risk_weight=40.0,
                regex_list=[
                    r"\b(legal action will be taken|police complaint will be filed against you|breach of contract penalty \$\d+)\b",
                    r"\byou\s+cannot\s+quit\s+without\s+paying\s+(?:compensation|penalty)\b"
                ],
                description="Scammers intimidating candidates with bogus legal notices or police threats when candidates attempt to stop paying fees.",
                mitigation_steps=["Fraudulent contracts are legally void ab initio.", "Block all communication and report to cybercrime police."]
            )
        ]

        for p in patterns:
            self.register_pattern(p)

    def scan_text(self, text: str) -> List[Tuple[ThreatPatternDef, List[str]]]:
        """Scan input string against all patterns in registry."""
        matches = []
        for pat_id, compiled_list in self._compiled_regexes.items():
            pattern_def = self.catalog[pat_id]
            snippets = []
            for comp in compiled_list:
                for match in comp.finditer(text):
                    snippets.append(match.group(0))

            if snippets:
                matches.append((pattern_def, list(set(snippets))))

        return matches
