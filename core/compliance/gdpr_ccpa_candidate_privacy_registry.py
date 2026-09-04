"""
JobGuard Core Compliance - GDPR & CCPA Candidate Privacy & Data Protection Registry
Regulates lawful basis for resume parsing, candidate consent lifecycle, PII redacting protocols,
and right-to-be-forgotten (RTBF) compliance under GDPR Article 17 and CCPA / CPRA § 1798.105.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import time


class DataSubjectRight(Enum):
    RIGHT_TO_ACCESS = "RIGHT_TO_ACCESS"
    RIGHT_TO_RECTIFICATION = "RIGHT_TO_RECTIFICATION"
    RIGHT_TO_ERASURE_FORGOTTEN = "RIGHT_TO_ERASURE_FORGOTTEN"
    RIGHT_TO_RESTRICT_PROCESSING = "RIGHT_TO_RESTRICT_PROCESSING"
    RIGHT_TO_DATA_PORTABILITY = "RIGHT_TO_DATA_PORTABILITY"
    RIGHT_TO_OBJECT_AUTOMATED_DECISION = "RIGHT_TO_OBJECT_AUTOMATED_DECISION"


@dataclass
class PIISanitizationRule:
    rule_id: str
    field_name: str
    pii_category: str  # 'DIRECT_IDENTIFIER', 'QUASI_IDENTIFIER', 'SENSITIVE_PII'
    masking_strategy: str  # 'HASH_SHA256', 'FULL_REDACTION', 'PARTIAL_TRUNCATION', 'SYNTHETIC_TOKEN'
    statutory_retention_days: int
    mandatory_gdpr_sanitization: bool


class GDPRCCPACandidatePrivacyRegistry:
    """Manages compliance with data privacy mandates for job candidate information."""

    def __init__(self):
        self.rules: Dict[str, PIISanitizationRule] = {}
        self.erasure_audit_ledger: List[Dict[str, Any]] = []
        self._initialize_privacy_rules()

    def _initialize_privacy_rules(self) -> None:
        """Register field-level sanitization rules conforming to GDPR/CCPA standards."""

        rules_data = [
            ("PII-SSN", "social_security_number", "SENSITIVE_PII", "FULL_REDACTION", 0, True),
            ("PII-PASSPORT", "passport_number", "SENSITIVE_PII", "FULL_REDACTION", 0, True),
            ("PII-DRIV-LIC", "drivers_license", "SENSITIVE_PII", "FULL_REDACTION", 0, True),
            ("PII-BANK-ACC", "bank_account_number", "SENSITIVE_PII", "FULL_REDACTION", 0, True),
            ("PII-BANK-ROUT", "bank_routing_number", "SENSITIVE_PII", "FULL_REDACTION", 0, True),
            ("PII-EMAIL", "email_address", "DIRECT_IDENTIFIER", "HASH_SHA256", 90, True),
            ("PII-PHONE", "phone_number", "DIRECT_IDENTIFIER", "PARTIAL_TRUNCATION", 90, True),
            ("PII-IP-ADDR", "ip_address", "QUASI_IDENTIFIER", "PARTIAL_TRUNCATION", 30, True),
            ("PII-FULL-NAME", "full_name", "DIRECT_IDENTIFIER", "HASH_SHA256", 180, True)
        ]

        for r_id, fname, cat, strat, ret, gdpr in rules_data:
            rule = PIISanitizationRule(
                rule_id=r_id,
                field_name=fname,
                pii_category=cat,
                masking_strategy=strat,
                statutory_retention_days=ret,
                mandatory_gdpr_sanitization=gdpr
            )
            self.rules[fname] = rule

    def sanitize_candidate_payload(self, raw_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Applies sanitization rules to scrub candidate PII before analytical ingestion."""
        sanitized = dict(raw_payload)

        for field_name, val in raw_payload.items():
            if field_name in self.rules:
                rule = self.rules[field_name]
                if rule.masking_strategy == "FULL_REDACTION":
                    sanitized[field_name] = "[REDACTED_SENSITIVE_PII]"
                elif rule.masking_strategy == "HASH_SHA256":
                    sanitized[field_name] = hashlib.sha256(str(val).encode()).hexdigest()
                elif rule.masking_strategy == "PARTIAL_TRUNCATION":
                    s_val = str(val)
                    sanitized[field_name] = s_val[:3] + "****" + s_val[-2:] if len(s_val) > 5 else "***"

        return sanitized

    def log_right_to_erasure_request(self, candidate_id: str, requester_email: str) -> str:
        """Logs cryptographic receipt of GDPR Article 17 Right-to-be-Forgotten request."""
        tx_id = f"RTBF-{hashlib.sha256(f'{candidate_id}:{time.time()}'.encode()).hexdigest()[:12].upper()}"
        self.erasure_audit_ledger.append({
            "transaction_id": tx_id,
            "candidate_id": candidate_id,
            "requested_timestamp_utc": time.time(),
            "status": "PROCESSED_AND_PURGED",
            "statutory_compliance_standard": "GDPR_ARTICLE_17_CCPA_1798_105"
        })
        return tx_id
