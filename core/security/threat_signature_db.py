"""
JobGuard Core Security - Threat Signature Database & YARA-Style Matching Engine
High-throughput pattern matcher for recruitment scams, identity theft vectors,
phishing payloads, and money-mule contract indicators.
"""

import re
import math
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class SignatureRule:
    rule_id: str
    name: str
    category: str
    severity: str  # "critical", "high", "medium", "low"
    weight: int
    regex_patterns: List[str]
    required_keywords: List[str] = field(default_factory=list)
    anti_patterns: List[str] = field(default_factory=list)
    description: str = ""
    mitigation: str = ""


@dataclass
class ThreatMatchResult:
    matched_rule_id: str
    rule_name: str
    category: str
    severity: str
    weight: int
    matched_snippets: List[str]
    description: str
    mitigation: str


class ThreatSignatureDatabase:
    """In-memory multi-pattern scanner with compiled regex indexing and entropy analysis."""

    def __init__(self):
        self._rules: Dict[str, SignatureRule] = {}
        self._compiled_regex: Dict[str, List[re.Pattern]] = {}
        self._compiled_anti: Dict[str, List[re.Pattern]] = {}
        self._load_core_signatures()

    def _load_core_signatures(self) -> None:
        """Register the comprehensive suite of verified threat signatures."""
        core_rules = [
            SignatureRule(
                rule_id="SIG-FIN-001",
                name="Fake Check & Equipment Advance Vendor Trap",
                category="Financial Scam",
                severity="critical",
                weight=40,
                regex_patterns=[
                    r"\b(deposit (the|this|our)?\s*check|send (a|the) cashier'?s check|wire (the )?funds? to (our )?vendor|purchase (materials|laptop) from (our )?approved vendor)\b",
                    r"\b(home office equipment fund|reimbursement check will be mailed|advance payment check for supplies)\b"
                ],
                description="Candidate is instructed to deposit a forged check and wire money to an accomplice vendor.",
                mitigation="Do NOT deposit any checks. Cease communication immediately."
            ),
            SignatureRule(
                rule_id="SIG-FEE-002",
                name="Upfront Security Deposit / Registration Fee Extortion",
                category="Fee Demand",
                severity="critical",
                weight=35,
                regex_patterns=[
                    r"\b(registration fee|refundable security deposit|training expense fee|id badge charge|laptop insurance fee|processing fee before joining)\b",
                    r"\b(pay ₹\s?\d{3,}|pay \$\s?\d{2,}\s?for account activation|refundable after (first|1st|\d+) task)\b"
                ],
                description="Demands upfront monetary payment under guise of refundable deposits or onboarding costs.",
                mitigation="Legitimate employers never charge candidates pre-employment fees."
            ),
            SignatureRule(
                rule_id="SIG-COMM-003",
                name="Off-Platform Unverified Chat Channel Hiring",
                category="Suspicious Channel",
                severity="high",
                weight=28,
                regex_patterns=[
                    r"\b(contact (us|me|hr) on (telegram|whatsapp|signal|viber)|message (our )?hiring manager @\w+|t\.me\/\w+|chat via whatsapp)\b",
                    r"\b(interview will be conducted (exclusively|entirely) over (text|telegram|whatsapp))\b"
                ],
                description="Avoids formal corporate video/voice channels in favor of anonymous instant messaging.",
                mitigation="Insist on official corporate email verification (@company.com) and secure video interview."
            ),
            SignatureRule(
                rule_id="SIG-PHISH-004",
                name="Premature Banking Credentials Harvesting",
                category="Identity Theft",
                severity="critical",
                weight=35,
                regex_patterns=[
                    r"\b(online banking (username|password|credentials)|routing number before interview|bank account details for background check)\b",
                    r"\b(send copy of driver'?s license and ssn before offer|share otp to confirm identity)\b"
                ],
                description="Attempts to harvest credentials and SSN/Govt IDs before formal offer acceptance.",
                mitigation="Never provide banking logins or OTPs. Direct deposit is handled post-start date."
            ),
            SignatureRule(
                rule_id="SIG-CRYPTO-005",
                name="Crypto / USDT Task Investment Ploy",
                category="Crypto Fraud",
                severity="critical",
                weight=38,
                regex_patterns=[
                    r"\b(earn (usdt|crypto|bitcoin|tether)|daily payout via usdt wallet|vip task recharge|recharge account to unlock commission)\b",
                    r"\b(like youtube videos to earn ₹\d+|rate products on e-commerce to get daily crypto)\b"
                ],
                description="Task-investment scheme asking victims to deposit crypto to unlock inflated commissions.",
                mitigation="Refuse all cryptocurrency transfers. These are organized cyber fraud syndicates."
            ),
            SignatureRule(
                rule_id="SIG-PRESSURE-006",
                name="Artificial High-Pressure Coercion Window",
                category="Social Engineering",
                severity="medium",
                weight=18,
                regex_patterns=[
                    r"\b(immediate acceptance required within \d+ (hours|hrs)|forfeit job if not signed today|act now limited slots available)\b",
                    r"\b(instant selection without interview|guaranteed placement within 1 hour)\b"
                ],
                description="Applies psychological urgency to bypass rational due diligence.",
                mitigation="Take standard 3-5 business days to review offer letters and consult HR."
            )
        ]

        for rule in core_rules:
            self.add_rule(rule)

    def add_rule(self, rule: SignatureRule) -> None:
        self._rules[rule.rule_id] = rule
        self._compiled_regex[rule.rule_id] = [re.compile(p, re.IGNORECASE) for p in rule.regex_patterns]
        self._compiled_anti[rule.rule_id] = [re.compile(p, re.IGNORECASE) for p in rule.anti_patterns]

    def scan_text(self, text: str) -> List[ThreatMatchResult]:
        """Scan raw document text against all registered threat rules."""
        matches: List[ThreatMatchResult] = []
        if not text:
            return matches

        for rule_id, rule in self._rules.items():
            # Check anti-patterns first
            anti_hit = False
            for anti_pat in self._compiled_anti.get(rule_id, []):
                if anti_pat.search(text):
                    anti_hit = True
                    break
            if anti_hit:
                continue

            # Check required keywords
            if rule.required_keywords:
                has_keywords = any(kw.lower() in text.lower() for kw in rule.required_keywords)
                if not has_keywords:
                    continue

            # Scan regex signatures
            matched_snippets = []
            for pat in self._compiled_regex.get(rule_id, []):
                found = pat.findall(text)
                if found:
                    for item in found:
                        snippet = item[0] if isinstance(item, tuple) else str(item)
                        if snippet not in matched_snippets:
                            matched_snippets.append(snippet)

            if matched_snippets:
                matches.append(ThreatMatchResult(
                    matched_rule_id=rule.rule_id,
                    rule_name=rule.name,
                    category=rule.category,
                    severity=rule.severity,
                    weight=rule.weight,
                    matched_snippets=matched_snippets,
                    description=rule.description,
                    mitigation=rule.mitigation
                ))

        return matches

    @staticmethod
    def calculate_shannon_entropy(data: str) -> float:
        """Compute Shannon entropy to detect obfuscated / base64 payloads."""
        if not data:
            return 0.0
        entropy = 0.0
        length = len(data)
        freq: Dict[str, int] = {}
        for char in data:
            freq[char] = freq.get(char, 0) + 1
        for count in freq.values():
            p_x = count / length
            entropy += -p_x * math.log2(p_x)
        return round(entropy, 4)
