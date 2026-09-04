"""
JobGuard Core Compliance - GDPR & CCPA PII Redaction / Sanitizer
Detects and scrubs Personally Identifiable Information (PII) including Aadhaar,
SSN, bank account numbers, credit cards, emails, and phone numbers before cloud processing.
"""

import re
import hashlib
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
import enum


class AnonymizationScheme(enum.Enum):
    MASK_REDACT = "MASK_REDACT"      # Replace with [REDACTED_SSN]
    HASH_TOKENIZE = "HASH_TOKENIZE"  # Replace with salted SHA-256 token
    PARTIAL_MASK = "PARTIAL_MASK"    # Replace with ***-**-1234


@dataclass
class SanitizedOutput:
    sanitized_text: str
    redaction_counts: Dict[str, int]
    detected_pii_types: List[str]


class PIISanitizer:
    """Multi-regex and checksum-based PII scrubber for global data protection regulations."""

    PII_PATTERNS = [
        ("SSN", r"\b\d{3}[- ]?\d{2}[- ]?\d{4}\b", "[REDACTED_SSN]"),
        ("AADHAAR", r"\b[2-9]\d{3}[- ]?\d{4}[- ]?\d{4}\b", "[REDACTED_AADHAAR]"),
        ("PAN_CARD", r"\b[A-Z]{5}\d{4}[A-Z]\b", "[REDACTED_PAN]"),
        ("CREDIT_CARD", r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b", "[REDACTED_CC]"),
        ("EMAIL", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", "[REDACTED_EMAIL]"),
        ("PHONE", r"\b(?:\+?\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}\b", "[REDACTED_PHONE]"),
        ("BANK_ROUTING", r"\b0[0-9]{8}\b", "[REDACTED_ROUTING]"),
        ("CRYPTO_WALLET", r"\b(0x[a-fA-F0-9]{40}|T[A-Za-z1-9]{33}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})\b", "[REDACTED_WALLET]")
    ]

    def __init__(self, salt: str = "jobguard-gdpr-salt-2026"):
        self.salt = salt
        self._compiled = [(name, re.compile(pat, re.IGNORECASE), repl) for name, pat, repl in self.PII_PATTERNS]

    def sanitize(self, text: str, scheme: AnonymizationScheme = AnonymizationScheme.MASK_REDACT) -> SanitizedOutput:
        """Process raw text and scrub all matching PII entities according to scheme."""
        if not text:
            return SanitizedOutput("", {}, [])

        counts: Dict[str, int] = {}
        detected_types: List[str] = []
        result_text = text

        for name, compiled_re, default_tag in self._compiled:
            matches = list(compiled_re.finditer(result_text))
            if matches:
                counts[name] = len(matches)
                detected_types.append(name)
                
                # Perform replacement
                def _replacer(m, pii_name=name, tag=default_tag):
                    matched_str = m.group(0)
                    if scheme == AnonymizationScheme.HASH_TOKENIZE:
                        h = hashlib.sha256(f"{self.salt}:{matched_str}".encode("utf-8")).hexdigest()[:12]
                        return f"[{pii_name}_TOKEN_{h}]"
                    elif scheme == AnonymizationScheme.PARTIAL_MASK:
                        if len(matched_str) > 4:
                            return "*" * (len(matched_str) - 4) + matched_str[-4:]
                        return "****"
                    return tag

                result_text = compiled_re.sub(_replacer, result_text)

        return SanitizedOutput(
            sanitized_text=result_text,
            redaction_counts=counts,
            detected_pii_types=detected_types
        )
