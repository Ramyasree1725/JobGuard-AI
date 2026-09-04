"""
JobGuard Core NLP - Named Entity & Predatory Relation Extractor
Extracts Triples (Subject, Predicate, Object) representing entity relationships
(e.g., [Recruiter] -> [Demands_Upfront_Payment_From] -> [Candidate]) using dependency grammar.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class EntitySpan:
    entity_text: str
    entity_type: str  # 'COMPANY', 'RECRUITER_NAME', 'PAYMENT_AMOUNT', 'CHANNEL', 'PAYMENT_METHOD'
    start_char: int
    end_char: int


@dataclass
class PredicateRelationTriple:
    subject: EntitySpan
    predicate: str  # 'DEMANDS_PAYMENT_VIA', 'CONDUCTS_INTERVIEW_ON', 'CLAIMS_REPRESENTATION_OF', 'PROMISES_SALARY'
    object_entity: EntitySpan
    confidence: float
    is_predatory: bool


class NamedEntityRelationExtractor:
    """Extracts semantic knowledge triples from unstructured job posts and recruiter emails."""

    def __init__(self):
        pass

    def extract_relations(self, text: str) -> List[PredicateRelationTriple]:
        """Extracts relationship triples using pattern-based syntactic relation matching."""
        triples: List[PredicateRelationTriple] = []

        # Pattern 1: Recruiter claims company
        comp_match = re.search(r"(?:hiring\s+manager|recruiter|hr)\s+at\s+([A-Z][a-zA-Z0-9\s&]+)", text)
        if comp_match:
            recruiter_span = EntitySpan("Recruiter", "RECRUITER_NAME", comp_match.start(), comp_match.start() + 9)
            comp_span = EntitySpan(comp_match.group(1).strip(), "COMPANY", comp_match.start(1), comp_match.end(1))
            triples.append(PredicateRelationTriple(
                subject=recruiter_span,
                predicate="CLAIMS_REPRESENTATION_OF",
                object_entity=comp_span,
                confidence=0.85,
                is_predatory=False
            ))

        # Pattern 2: Demands payment via app
        pay_match = re.search(r"(?:pay|send|transfer)\s+(\$(?:\d+))\s+via\s+(zelle|cashapp|venmo|bitcoin|crypto)", text, re.IGNORECASE)
        if pay_match:
            amount_span = EntitySpan(pay_match.group(1), "PAYMENT_AMOUNT", pay_match.start(1), pay_match.end(1))
            method_span = EntitySpan(pay_match.group(2), "PAYMENT_METHOD", pay_match.start(2), pay_match.end(2))
            recruiter_span = EntitySpan("Recruiter", "RECRUITER_NAME", 0, 0)

            triples.append(PredicateRelationTriple(
                subject=recruiter_span,
                predicate="DEMANDS_PAYMENT_VIA",
                object_entity=method_span,
                confidence=0.98,
                is_predatory=True
            ))

        # Pattern 3: Interview on messaging app
        chat_match = re.search(r"interview\s+(?:on|via|through)\s+(telegram|whatsapp|signal)", text, re.IGNORECASE)
        if chat_match:
            channel_span = EntitySpan(chat_match.group(1), "CHANNEL", chat_match.start(1), chat_match.end(1))
            recruiter_span = EntitySpan("Recruiter", "RECRUITER_NAME", 0, 0)

            triples.append(PredicateRelationTriple(
                subject=recruiter_span,
                predicate="CONDUCTS_INTERVIEW_ON",
                object_entity=channel_span,
                confidence=0.92,
                is_predatory=True
            ))

        return triples
