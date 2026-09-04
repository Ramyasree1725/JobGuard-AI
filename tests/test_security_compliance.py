"""
Unit Tests for Core Security & Compliance Modules
"""

import unittest
from core.security.crypto_primitives import HKDF, ConstantTime, ChaCha20Poly1305AEAD, TokenGenerator
from core.security.rate_limiter import TokenBucketRateLimiter, SlidingWindowRateLimiter
from core.compliance.gdpr_sanitizer import PIISanitizer, AnonymizationScheme
from core.compliance.legal_rules import LegalRuleEvaluator


class TestSecurityCompliance(unittest.TestCase):

    def test_constant_time_equals(self):
        self.assertTrue(ConstantTime.equals(b"secret", b"secret"))
        self.assertFalse(ConstantTime.equals(b"secret1", b"secret2"))

    def test_pii_sanitization(self):
        sanitizer = PIISanitizer()
        raw = "Contact recruiter at hr@techfirm.com with SSN 123-45-6789 or phone 123-456-7890."
        res = sanitizer.sanitize(raw)
        self.assertIn("[REDACTED_SSN]", res.sanitized_text)
        self.assertIn("[REDACTED_EMAIL]", res.sanitized_text)
        self.assertIn("[REDACTED_PHONE]", res.sanitized_text)

    def test_token_bucket_rate_limiter(self):
        limiter = TokenBucketRateLimiter(capacity=5, refill_rate_per_sec=1.0)
        self.assertTrue(limiter.allow_request(1))
        self.assertTrue(limiter.allow_request(4))
        self.assertFalse(limiter.allow_request(1))  # Exhausted

    def test_legal_rule_evaluation(self):
        evaluator = LegalRuleEvaluator()
        scam_text = "Please deposit the check and wire transfer $500 to our approved equipment vendor."
        checks = evaluator.evaluate(scam_text)
        violations = [v for c in checks for v in c.violations]
        self.assertTrue(len(violations) > 0)


if __name__ == "__main__":
    unittest.main()
