"""
JobGuard Backend Service - Multi-Tier Scam Detection Orchestrator
Master coordinator executing all statistical, neural, signature, and graph layers.
"""

import time
from typing import Dict, List, Any, Optional
from core.security.threat_signature_db import ThreatSignatureDatabase
from core.compliance.legal_rules import LegalRuleEvaluator
from core.nlp.sentiment_lexicon import UrgencySentimentAnalyzer
from backend.services.domain_reputation import DomainReputationService


class ScamDetectionOrchestrator:
    """Enterprise end-to-end multi-layer detection pipeline."""

    def __init__(self):
        self.threat_db = ThreatSignatureDatabase()
        self.legal_evaluator = LegalRuleEvaluator()
        self.sentiment = UrgencySentimentAnalyzer()
        self.domain_service = DomainReputationService()

    def evaluate_payload(self, job_title: str, company: str, salary: str, description: str, recruiter_email: str) -> Dict[str, Any]:
        start_time = time.monotonic()
        full_text = f"{job_title}\n{company}\n{salary}\n{description}\n{recruiter_email}"

        # 1. Threat signatures
        matches = self.threat_db.scan_text(full_text)
        threat_penalty = sum(m.weight for m in matches)

        # 2. Legal rules
        legal_checks = self.legal_evaluator.evaluate(full_text)
        violations = [v for c in legal_checks for v in c.violations]
        legal_penalty = len(violations) * 20.0

        # 3. Urgency analysis
        urgency_res = self.sentiment.analyze_pressure_score(full_text)
        urgency_penalty = urgency_res["pressure_score"] * 0.3

        # 4. Domain check
        domain_penalty = 0.0
        if recruiter_email and "@" in recruiter_email:
            domain = recruiter_email.split("@")[1].strip()
            d_res = self.domain_service.evaluate_domain(domain)
            domain_penalty = d_res.risk_score * 0.35

        # Synthesis
        total_risk = min(100.0, threat_penalty + legal_penalty + urgency_penalty + domain_penalty)
        elapsed = (time.monotonic() - start_time) * 1000.0

        return {
            "fraud_risk_score": round(total_risk, 1),
            "legitimacy_score": round(100.0 - total_risk, 1),
            "verdict": "CRITICAL FRAUD" if total_risk >= 60 else "SUSPICIOUS" if total_risk >= 25 else "SAFE",
            "threat_matches_count": len(matches),
            "statutory_violations_count": len(violations),
            "urgency_score": urgency_res["pressure_score"],
            "domain_risk": round(domain_penalty, 1),
            "audit_latency_ms": round(elapsed, 2)
        }
