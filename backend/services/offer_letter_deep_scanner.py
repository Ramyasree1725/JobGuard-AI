"""
JobGuard Backend Service - Offer Letter & Contract Deep Scanner
Executes multi-vector forensic evaluation on employment contracts, appointment letters,
and consulting agreements to detect advance fee traps, fake checks, and identity theft.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re
import hashlib


@dataclass
class ForensicClauseFinding:
    clause_id: str
    clause_text: str
    risk_category: str
    severity: str  # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    confidence: float
    explanation: str
    statutory_violation: Optional[str] = None


@dataclass
class OfferScanResult:
    scan_id: str
    document_hash: str
    overall_fraud_score: float  # 0.0 to 100.0
    threat_level: str  # 'AUTHENTIC', 'ELEVATED_RISK', 'CRITICAL_FRAUD'
    findings: List[ForensicClauseFinding]
    detected_payment_traps: List[str]
    recruiter_channel_assessment: str
    recommended_candidate_action: str
    is_safe_to_sign: bool


class OfferLetterDeepScanner:
    """Multi-vector forensic contract analysis service."""

    def __init__(self):
        self._initialize_signature_rules()

    def _initialize_signature_rules(self) -> None:
        """Configures regex heuristic patterns for contract clauses."""
        self.trap_patterns = [
            (
                r"(?:check|cheque)\s+(?:will\s+be\s+sent|mailed|issued)\s+for\s+(?:equipment|supplies|laptop)",
                "EQUIPMENT_CHECK_OVERPAYMENT",
                "CRITICAL",
                0.95,
                "Clause stipulates mailing a check for equipment purchase. Classic counterfeit check kickback scheme.",
                "18 U.S.C. § 1344 - Bank Fraud"
            ),
            (
                r"(?:deposit|forward|wire|refund)\s+(?:excess|remaining|surplus)\s+(?:funds|balance)\s+to\s+(?:our|the)\s+vendor",
                "SURPLUS_FUNDS_TRANSFER",
                "CRITICAL",
                0.98,
                "Mandates transferring check surplus to a third-party vendor. Once check bounces, victim is legally liable.",
                "18 U.S.C. § 1343 - Wire Fraud"
            ),
            (
                r"(?:refundable|security|onboarding|registration)\s+(?:deposit|fee)\s+of\s+\$(?:\d+)",
                "UPFRONT_SECURITY_DEPOSIT",
                "HIGH",
                0.90,
                "Requires upfront monetary deposit before start of work. Genuine corporate employers never charge employees.",
                "FTC Act § 5"
            ),
            (
                r"(?:telegram|whatsapp|signal)\s+(?:username|channel|chat)\s+is\s+the\s+official\s+workspace",
                "MESSAGING_APP_WORKPLACE",
                "MEDIUM",
                0.75,
                "Specifies consumer messaging app as official corporate workplace without corporate SSO infrastructure.",
                None
            ),
            (
                r"(?:provide|fill\s+in)\s+your\s+(?:online\s+banking\s+password|login\s+credentials|atm\s+pin)",
                "BANKING_CREDENTIAL_HARVEST",
                "CRITICAL",
                0.99,
                "Directly demands online banking credentials or PIN under guise of payroll setup. Blatant identity theft.",
                "18 U.S.C. § 1028 - Aggravated Identity Theft"
            )
        ]

    def scan_offer_document(self, text: str, document_name: str = "offer_letter.pdf") -> OfferScanResult:
        """Executes full syntactic, lexical, and predatory clause analysis on contract text."""
        doc_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        scan_id = f"SCAN-{doc_hash[:12].upper()}"

        findings: List[ForensicClauseFinding] = []
        payment_traps: List[str] = []
        total_risk = 0.0

        for pattern, cat, sev, conf, expl, stat in self.trap_patterns:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            if matches:
                payment_traps.append(cat)
                severity_weight = {"LOW": 10.0, "MEDIUM": 25.0, "HIGH": 50.0, "CRITICAL": 85.0}[sev]
                total_risk += severity_weight * conf

                for m in matches:
                    snippet = text[max(0, m.start() - 30): min(len(text), m.end() + 30)].strip()
                    findings.append(ForensicClauseFinding(
                        clause_id=f"FIND-{len(findings) + 1:03d}",
                        clause_text=f"...{snippet}...",
                        risk_category=cat,
                        severity=sev,
                        confidence=conf,
                        explanation=expl,
                        statutory_violation=stat
                    ))

        # Additional domain / channel heuristics
        has_chat = bool(re.search(r"telegram|whatsapp", text, re.IGNORECASE))
        recruiter_assessment = "Unverified messaging channel used." if has_chat else "Standard documentation format."

        normalized_score = min(100.0, max(0.0, total_risk))

        if normalized_score >= 60.0:
            threat_level = "CRITICAL_FRAUD"
            action = "DO NOT SIGN. Immediately terminate communication. File report with JobGuard and FTC."
            is_safe = False
        elif normalized_score >= 25.0:
            threat_level = "ELEVATED_RISK"
            action = "CAUTION: Suspicious contract clauses detected. Independently verify with company HR before signing."
            is_safe = False
        else:
            threat_level = "AUTHENTIC"
            action = "Contract terms align with standard employment agreements."
            is_safe = True

        return OfferScanResult(
            scan_id=scan_id,
            document_hash=doc_hash,
            overall_fraud_score=normalized_score,
            threat_level=threat_level,
            findings=findings,
            detected_payment_traps=list(set(payment_traps)),
            recruiter_channel_assessment=recruiter_assessment,
            recommended_candidate_action=action,
            is_safe_to_sign=is_safe
        )
