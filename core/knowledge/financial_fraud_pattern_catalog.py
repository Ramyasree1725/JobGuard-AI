"""
JobGuard Core Knowledge - Financial Fraud & Payment Pattern Catalog
Provides comprehensive detection logic for advance fees, check overpayments,
wire routing spoofing, cryptocurrency drainer wallets, and predatory contract stipulations.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import re


class PaymentChannelType(Enum):
    PAPER_CHECK = "PAPER_CHECK"
    WIRE_TRANSFER = "WIRE_TRANSFER"
    P2P_PAYMENT_APP = "P2P_PAYMENT_APP"
    CRYPTOCURRENCY = "CRYPTOCURRENCY"
    GIFT_CARD = "GIFT_CARD"
    PREPAID_DEBIT = "PREPAID_DEBIT"
    PAYROLL_DIRECT_DEPOSIT = "PAYROLL_DIRECT_DEPOSIT"


class FinancialRiskRating(Enum):
    SAFE_STANDARD = "SAFE_STANDARD"
    SUSPICIOUS_CLAUSE = "SUSPICIOUS_CLAUSE"
    SEVERE_PREDATORY = "SEVERE_PREDATORY"
    CONFIRMED_FRAUD_PATTERN = "CONFIRMED_FRAUD_PATTERN"


@dataclass
class FinancialPatternDefinition:
    pattern_id: str
    name: str
    channel: PaymentChannelType
    risk_rating: FinancialRiskRating
    regex_indicators: List[str]
    typical_victim_cost_usd: float
    regulatory_statute: str
    explanation: str
    immediate_safety_step: str


@dataclass
class FinancialAuditReport:
    flagged_patterns: List[FinancialPatternDefinition]
    highest_severity: FinancialRiskRating
    composite_financial_risk_score: float  # 0 to 100
    detected_payment_channels: List[PaymentChannelType]
    statutory_violations: List[str]
    candidate_protective_actions: List[str]


class FinancialFraudPatternCatalog:
    """Catalog and signature matching engine for monetary manipulation and predatory payment schemes."""

    def __init__(self):
        self.patterns: Dict[str, FinancialPatternDefinition] = {}
        self._compiled: Dict[str, List[re.Pattern]] = {}
        self._build_pattern_database()

    def _build_pattern_database(self) -> None:
        """Register extensive financial scam patterns."""

        # 1. Counterfeit Check Overpayment
        self._register_pattern(FinancialPatternDefinition(
            pattern_id="FIN-001",
            name="Counterfeit Equipment Check & Vendor Surplus Kickback",
            channel=PaymentChannelType.PAPER_CHECK,
            risk_rating=FinancialRiskRating.CONFIRMED_FRAUD_PATTERN,
            regex_indicators=[
                r"(?:we\s+will\s+send|mailing|issuing)\s+(?:a\s+check|cheque)\s+(?:for|worth|amounting\s+to)\s+\$(?:\d+(?:,\d{3})*(?:\.\d{2})?)",
                r"(?:deposit|cash)\s+(?:the|this)\s+check\s+and\s+(?:wire|zelle|send|forward)\s+(?:the\s+rest|balance|vendor)",
                r"(?:approved|designated|authorized)\s+(?:home\s+office|equipment)\s+vendor",
                r"keep\s+\$(?:\d+)\s+as\s+your\s+(?:sign-on|first\s+week)\s+(?:bonus|salary)"
            ],
            typical_victim_cost_usd=3250.00,
            regulatory_statute="18 U.S. Code § 1344 - Bank Fraud; UCC § 3-404 Impostors",
            explanation="The scammer sends a fake check, instructing the candidate to deposit it and wire the difference to a 'supplier'. When the check bounces 5-10 days later, the candidate owes the bank the entire amount.",
            immediate_safety_step="Do not deposit the check. If already deposited, notify your bank fraud department immediately."
        ))

        # 2. Cryptocurrency Task Optimization Recharge
        self._register_pattern(FinancialPatternDefinition(
            pattern_id="FIN-002",
            name="Cryptocurrency Wallet Task Deposit / Recharge Scheme",
            channel=PaymentChannelType.CRYPTOCURRENCY,
            risk_rating=FinancialRiskRating.CONFIRMED_FRAUD_PATTERN,
            regex_indicators=[
                r"(?:deposit|recharge|top\s*up)\s+(?:usdt|trc20|erc20|bitcoin|eth)\s+to\s+(?:complete|unlock|continue)",
                r"negative\s+(?:account\s+)?balance\s+(?:requires|needs)\s+(?:reset|deposit)",
                r"(?:wallet\s+address|deposit\s+link):\s*(?:0x[a-fA-F0-9]{40}|T[A-Za-z1-9]{33})",
                r"(?:crypto|usdt)\s+(?:withdrawal|profit)\s+(?:tax|unlock\s+fee)"
            ],
            typical_victim_cost_usd=8500.00,
            regulatory_statute="18 U.S. Code § 1343 - Wire Fraud; SEC Securities Enforcement",
            explanation="Requires the candidate to transfer cryptocurrency to a fraudulent 'platform' to unlock commission tasks or withdraw alleged earnings.",
            immediate_safety_step="Cease all transfers immediately. Do not pay any 'withdrawal tax' or 'unlock fee'."
        ))

        # 3. P2P Payment App Onboarding Fee
        self._register_pattern(FinancialPatternDefinition(
            pattern_id="FIN-003",
            name="P2P App Registration & Identity Verification Fee",
            channel=PaymentChannelType.P2P_PAYMENT_APP,
            risk_rating=FinancialRiskRating.CONFIRMED_FRAUD_PATTERN,
            regex_indicators=[
                r"send\s+\$(?:\d+)\s+via\s+(?:zelle|cashapp|venmo|apple\s+cash)\s+to\s+(?:verify|reserve|register)",
                r"(?:zelle|cashapp)\s+(?:email|phone|tag):\s*[a-zA-Z0-9_@.\-]+",
                r"processing\s+fee\s+is\s+100%\s+refundable\s+(?:on|upon)\s+(?:start|onboarding)"
            ],
            typical_victim_cost_usd=450.00,
            regulatory_statute="FTC Act Section 5(a) - Unfair or Deceptive Business Practices",
            explanation="Directs candidate to use peer-to-peer instant apps which provide zero consumer fraud protection for employment fees.",
            immediate_safety_step="Block the requester. File an unauthorized transaction report with the payment app provider."
        ))

        # 4. Gift Card Equipment Procurement Trap
        self._register_pattern(FinancialPatternDefinition(
            pattern_id="FIN-004",
            name="Retail Gift Card Procurement Mandate",
            channel=PaymentChannelType.GIFT_CARD,
            risk_rating=FinancialRiskRating.CONFIRMED_FRAUD_PATTERN,
            regex_indicators=[
                r"purchase\s+(?:apple|target|steam|amazon|google\s+play|vanilla\s+visa)\s+gift\s+cards?",
                r"scratch\s+(?:the\s+back|pin)\s+and\s+send\s+(?:photos?|codes?|numbers?)",
                r"software\s+licensing\s+requires\s+(?:gift\s+cards?|prepaid\s+cards?)"
            ],
            typical_victim_cost_usd=1200.00,
            regulatory_statute="18 U.S. Code § 1029 - Fraud and Related Activity in Connection with Access Devices",
            explanation="Demands purchase of untraceable retail gift cards for 'software licensing' or 'initial supplies'.",
            immediate_safety_step="Never buy gift cards for an employer. Gift cards are exclusively for personal gifts."
        ))

        # 5. Premature Direct Deposit Banking Capture
        self._register_pattern(FinancialPatternDefinition(
            pattern_id="FIN-005",
            name="Premature Direct Deposit & Online Banking Hijack",
            channel=PaymentChannelType.PAYROLL_DIRECT_DEPOSIT,
            risk_rating=FinancialRiskRating.SEVERE_PREDATORY,
            regex_indicators=[
                r"(?:provide|send)\s+your\s+(?:online\s+banking\s+username|login|password)\s+for\s+(?:payroll|verification)",
                r"voided\s+check\s+and\s+ssn\s+(?:before|prior\s+to)\s+(?:the\s+interview|formal\s+offer)",
                r"verify\s+your\s+account\s+by\s+confirming\s+the\s+micro-deposit\s+codes"
            ],
            typical_victim_cost_usd=5000.00,
            regulatory_statute="18 U.S. Code § 1028 - Identity Theft and Aggravated Identity Theft",
            explanation="Attempts to capture online banking credentials or complete identity dossiers to initiate unauthorized ACH transfers.",
            immediate_safety_step="Never share banking passwords or two-factor authentication codes with anyone."
        ))

    def _register_pattern(self, pattern: FinancialPatternDefinition) -> None:
        self.patterns[pattern.pattern_id] = pattern
        self._compiled[pattern.pattern_id] = [
            re.compile(p, re.IGNORECASE) for p in pattern.regex_indicators
        ]

    def audit_financial_clauses(self, text: str) -> FinancialAuditReport:
        """Audits job offer or chat transcripts for known predatory financial manipulation patterns."""
        flagged: List[FinancialPatternDefinition] = []
        channels: Set[PaymentChannelType] = set()
        statutes: Set[str] = set()
        actions: List[str] = []

        for pat_id, regexes in self._compiled.items():
            pattern = self.patterns[pat_id]
            for r in regexes:
                if r.search(text):
                    flagged.append(pattern)
                    channels.add(pattern.channel)
                    statutes.add(pattern.regulatory_statute)
                    actions.append(pattern.immediate_safety_step)
                    break

        if not flagged:
            return FinancialAuditReport(
                flagged_patterns=[],
                highest_severity=FinancialRiskRating.SAFE_STANDARD,
                composite_financial_risk_score=0.0,
                detected_payment_channels=[],
                statutory_violations=[],
                candidate_protective_actions=["No predatory financial mechanisms detected in reviewed text."]
            )

        # Calculate composite score
        severity_order = {
            FinancialRiskRating.SAFE_STANDARD: 0,
            FinancialRiskRating.SUSPICIOUS_CLAUSE: 1,
            FinancialRiskRating.SEVERE_PREDATORY: 2,
            FinancialRiskRating.CONFIRMED_FRAUD_PATTERN: 3
        }

        max_sev = max(flagged, key=lambda x: severity_order[x.risk_rating]).risk_rating
        base_score = 90.0 if max_sev == FinancialRiskRating.CONFIRMED_FRAUD_PATTERN else 60.0
        composite_score = min(100.0, base_score + (len(flagged) - 1) * 5.0)

        return FinancialAuditReport(
            flagged_patterns=flagged,
            highest_severity=max_sev,
            composite_financial_risk_score=composite_score,
            detected_payment_channels=list(channels),
            statutory_violations=list(statutes),
            candidate_protective_actions=list(set(actions))
        )
