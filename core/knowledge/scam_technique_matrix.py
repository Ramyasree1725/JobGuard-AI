"""
JobGuard Core Knowledge - Recruitment Scam Technique Matrix
Provides an ontological framework mapped to adversarial tactics, techniques,
and procedures (TTPs) for employment scams, advance-fee schemes, and impersonation fraud.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import re


class ThreatTactic(Enum):
    RECONNAISSANCE = "TA0001_RECONNAISSANCE"
    INITIAL_CONTACT = "TA0002_INITIAL_CONTACT"
    SOCIAL_ENGINEERING = "TA0003_SOCIAL_ENGINEERING"
    FAKE_INTERVIEW = "TA0004_FAKE_INTERVIEW"
    CONTRACT_FABRICATION = "TA0005_CONTRACT_FABRICATION"
    FINANCIAL_EXPLOITATION = "TA0006_FINANCIAL_EXPLOITATION"
    CREDENTIAL_HARVESTING = "TA0007_CREDENTIAL_HARVESTING"
    RESIDUAL_HARASSMENT = "TA0008_RESIDUAL_HARASSMENT"


class ThreatSeverity(Enum):
    INFORMATIONAL = "INFORMATIONAL"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class ScamTechnique:
    technique_id: str
    name: str
    tactic: ThreatTactic
    severity: ThreatSeverity
    description: str
    detection_heuristics: List[str]
    regex_signatures: List[str]
    mitigation_advice: str
    historical_loss_range_usd: Tuple[float, float]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TechniqueMatchResult:
    technique: ScamTechnique
    matched_phrases: List[str]
    confidence: float
    threat_contribution: float
    mitigation_steps: List[str]


class ScamTechniqueMatrix:
    """Master repository and pattern matcher for job fraud tactics and indicators."""

    def __init__(self):
        self.techniques: Dict[str, ScamTechnique] = {}
        self._compiled_regexes: Dict[str, List[re.Pattern]] = {}
        self._build_technique_matrix()

    def _build_technique_matrix(self) -> None:
        """Populate the comprehensive taxonomy of recruitment fraud techniques."""
        
        # 1. Advance Fee / Registration Schemes
        self._register_technique(ScamTechnique(
            technique_id="T1001",
            name="Upfront Onboarding & Equipment Fee Demand",
            tactic=ThreatTactic.FINANCIAL_EXPLOITATION,
            severity=ThreatSeverity.CRITICAL,
            description="Demanding upfront payment for laptop shipping, onboarding materials, security clearance, or background checks.",
            detection_heuristics=[
                "Payment required before official work begins",
                "Requesting wire transfer, crypto, or gift cards for equipment",
                "Promising immediate reimbursement in first paycheck"
            ],
            regex_signatures=[
                r"(?:registration|processing|onboarding|equipment|training)\s+(?:fee|cost|charge|deposit)",
                r"pay\s+\$(?:\d+)\s+for\s+(?:laptop|equipment|software|verification)",
                r"reimbursed?\s+in\s+your\s+(?:first|1st)\s+(?:paycheck|salary)",
                r"(?:crypto|bitcoin|gift\s*card|zelle|cashapp|venmo)\s+(?:payment|transfer|deposit)"
            ],
            mitigation_advice="Legitimate employers provide equipment and training at zero cost to the employee. Never send funds to an employer.",
            historical_loss_range_usd=(250.0, 3500.0)
        ))

        # 2. Counterfeit Check / Overpayment Trap
        self._register_technique(ScamTechnique(
            technique_id="T1002",
            name="Counterfeit Check Overpayment & Vendor Kickback",
            tactic=ThreatTactic.FINANCIAL_EXPLOITATION,
            severity=ThreatSeverity.CRITICAL,
            description="Mailing a fraudulent cashier's check to deposit, with instructions to wire money back to an 'approved home office vendor'.",
            detection_heuristics=[
                "Check issued before any completed work",
                "Instructions to forward surplus funds to third-party vendor",
                "Urgent request to deposit via mobile banking app"
            ],
            regex_signatures=[
                r"(?:deposit|cash)\s+(?:the|this|a)\s+(?:check|cheque|e-check)",
                r"send\s+(?:the\s+remaining|surplus|rest|balance)\s+(?:money|funds|amount)\s+to\s+(?:our|the)\s+vendor",
                r"home\s+office\s+(?:vendor|supplier|setup)\s+(?:payment|wire|transfer)",
                r"mobile\s+(?:deposit|banking)\s+(?:immediately|asap|within\s+24\s+hours)"
            ],
            mitigation_advice="Deposited fake checks appear cleared for several days before bouncing. The candidate is legally liable for all bounced funds.",
            historical_loss_range_usd=(1500.0, 8000.0)
        ))

        # 3. Chat-Only Anonymous Hiring
        self._register_technique(ScamTechnique(
            technique_id="T1003",
            name="Chat-Only Unverified Interview Process",
            tactic=ThreatTactic.FAKE_INTERVIEW,
            severity=ThreatSeverity.HIGH,
            description="Conducting recruitment entirely via text on Telegram, WhatsApp, Signal, or Google Chat without audio/video or in-person evaluation.",
            detection_heuristics=[
                "Interview conducted purely via instant messaging text",
                "Immediate hiring decision within 15-30 minutes of text chat",
                "Refusal or avoidance of live video conferencing"
            ],
            regex_signatures=[
                r"interview\s+will\s+be\s+conducted\s+(?:via|on|through)\s+(?:telegram|whatsapp|signal|google\s+chat|hangouts)",
                r"download\s+(?:telegram|signal)\s+and\s+add\s+(?:the\s+hiring\s+manager|our\s+hr|mr\.|mrs\.)",
                r"contact\s+@[a-zA-Z0-9_]+\s+on\s+telegram\s+for\s+brief\s+interview",
                r"instant\s+(?:hiring|selection|appointment)\s+after\s+(?:chat|questionnaire)"
            ],
            mitigation_advice="Real organizations conduct live structured video or in-person interviews before issuing formal employment offers.",
            historical_loss_range_usd=(0.0, 500.0)
        ))

        # 4. Premature Sensitive PII Harvesting
        self._register_technique(ScamTechnique(
            technique_id="T1004",
            name="Premature Identity & Banking Harvesting",
            tactic=ThreatTactic.CREDENTIAL_HARVESTING,
            severity=ThreatSeverity.CRITICAL,
            description="Demanding SSN, passport photos, driver's license scans, or bank direct deposit details prior to formal verification or interviews.",
            detection_heuristics=[
                "SSN requested on initial application questionnaire",
                "Banking credentials requested via unencrypted email/form",
                "Driver's license photo upload required before interview"
            ],
            regex_signatures=[
                r"(?:social\s+security\s+number|ssn|tax\s+id)\s+(?:required|needed)\s+for\s+(?:application|initial\s+screening)",
                r"send\s+(?:a\s+copy|photo)\s+of\s+your\s+(?:driver'?s?\s+license|passport|id\s+card)",
                r"(?:bank\s+account\s+number|routing\s+number|online\s+banking\s+login)\s+for\s+(?:payroll\s+setup|direct\s+deposit)",
                r"fill\s+out\s+(?:the\s+attached|this)\s+(?:direct\s+deposit|banking|w4)\s+form\s+before\s+interview"
            ],
            mitigation_advice="Do not provide banking or government ID details until formal employment verification on an authenticated enterprise portal.",
            historical_loss_range_usd=(500.0, 15000.0)
        ))

        # 5. Task Optimization / Crypto Rating Scheme
        self._register_technique(ScamTechnique(
            technique_id="T1005",
            name="Task Optimization & Crypto Escrow Scam",
            tactic=ThreatTactic.FINANCIAL_EXPLOITATION,
            severity=ThreatSeverity.CRITICAL,
            description="Deceptive micro-task scheme requiring users to 'recharge' or deposit USDT/crypto balances to unlock task completion payouts.",
            detection_heuristics=[
                "Work involves clicking buttons to 'optimize' products/hotels/apps",
                "Negative balance requires cryptocurrency deposit to resume work",
                "Tiered VIP commission structure with daily crypto payouts"
            ],
            regex_signatures=[
                r"(?:optimize|rate|review)\s+(?:products|apps|hotels|data)\s+(?:daily|commission)",
                r"(?:recharge|deposit)\s+(?:usdt|crypto|wallet)\s+to\s+(?:unlock|continue|withdraw)",
                r"daily\s+profit\s+of\s+(?:\$|usd)?\d+\s*-\s*(?:\$|usd)?\d+\s+(?:guaranteed|usdt)",
                r"level\s+[1-5]\s+vip\s+(?:account|upgrade|commission)"
            ],
            mitigation_advice="No legitimate job requires employees to deposit money into a crypto wallet to complete work tasks.",
            historical_loss_range_usd=(500.0, 50000.0)
        ))

        # 6. Artificial Urgency & Coercive Timelines
        self._register_technique(ScamTechnique(
            technique_id="T1006",
            name="Artificial Pressure & Hyper-Compressed Timeline",
            tactic=ThreatTactic.SOCIAL_ENGINEERING,
            severity=ThreatSeverity.MEDIUM,
            description="Manufacturing false urgency (e.g. 'Must sign within 2 hours or offer voided') to prevent candidate from consulting peers.",
            detection_heuristics=[
                "Exploding offer window under 24 hours",
                "Threats of forfeiting position if not signed immediately",
                "Aggressive repeated messaging"
            ],
            regex_signatures=[
                r"offer\s+(?:expires|void|cancelled)\s+within\s+(?:1|2|3|4|6|12|24)\s+hours",
                r"sign\s+and\s+return\s+(?:immediately|within\s+the\s+hour|today\s+before\s+\d+)",
                r"limited\s+slots\s+available,\s+first\s+come\s+first\s+serve",
                r"urgent\s+response\s+required\s+to\s+secure\s+your\s+slot"
            ],
            mitigation_advice="Legitimate corporate offers provide reasonable time (typically 3 to 7 business days) to review contract terms.",
            historical_loss_range_usd=(0.0, 1000.0)
        ))

    def _register_technique(self, technique: ScamTechnique) -> None:
        self.techniques[technique.technique_id] = technique
        self._compiled_regexes[technique.technique_id] = [
            re.compile(pattern, re.IGNORECASE) for pattern in technique.regex_signatures
        ]

    def scan_content(self, text: str) -> List[TechniqueMatchResult]:
        """Scans input text against all scam technique signatures and calculates threat contributions."""
        results: List[TechniqueMatchResult] = []

        for tech_id, patterns in self._compiled_regexes.items():
            technique = self.techniques[tech_id]
            matched_phrases: List[str] = []

            for pattern in patterns:
                matches = pattern.findall(text)
                if matches:
                    for m in matches:
                        matched_phrases.append(m if isinstance(m, str) else m[0])

            if matched_phrases:
                # Calculate confidence based on distinct pattern matches
                confidence = min(1.0, 0.5 + 0.2 * len(set(matched_phrases)))
                
                # Weight by severity
                severity_weights = {
                    ThreatSeverity.INFORMATIONAL: 0.1,
                    ThreatSeverity.LOW: 0.25,
                    ThreatSeverity.MEDIUM: 0.5,
                    ThreatSeverity.HIGH: 0.8,
                    ThreatSeverity.CRITICAL: 1.0
                }
                threat_contribution = severity_weights.get(technique.severity, 0.5) * confidence

                results.append(TechniqueMatchResult(
                    technique=technique,
                    matched_phrases=list(set(matched_phrases)),
                    confidence=confidence,
                    threat_contribution=threat_contribution,
                    mitigation_steps=[technique.mitigation_advice]
                ))

        return sorted(results, key=lambda x: x.threat_contribution, reverse=True)

    def get_technique_by_id(self, technique_id: str) -> Optional[ScamTechnique]:
        return self.techniques.get(technique_id)
