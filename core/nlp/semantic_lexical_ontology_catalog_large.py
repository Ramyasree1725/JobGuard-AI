"""
JobGuard Core NLP - Semantic Lexical Ontology & Concept Taxonomy Large
Provides hierarchical hypernyms, meronyms, and semantic entailment relations
for contextual fraud discourse analysis and deception detection in job postings.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class SemanticConceptNode:
    concept_id: str
    concept_name: str
    hypernym_parents: List[str]
    hyponym_children: List[str]
    related_lexical_tokens: List[str]
    is_predatory_intent: bool
    contextual_weight: float


class SemanticLexicalOntologyCatalogLarge:
    """Master expanded concept ontology for recruitment deception parsing."""

    def __init__(self):
        self.concepts: Dict[str, SemanticConceptNode] = {}
        self._seed_concepts()

    def _seed_concepts(self) -> None:
        """Register extensive conceptual taxonomy nodes."""

        concepts_data = [
            (
                "CONCEPT-001",
                "Predatory_Advance_Payment",
                ["Financial_Transaction"],
                ["Equipment_Deposit", "Registration_Fee", "Training_Charge"],
                ["fee", "deposit", "pay upfront", "registration cost", "onboarding charge", "wire money"],
                True,
                0.95
            ),
            (
                "CONCEPT-002",
                "Counterfeit_Disbursement_Instrument",
                ["Commercial_Paper"],
                ["Cashier_Check_Fraud", "Electronic_Check_Kickback"],
                ["cashier check", "certified check", "mail check", "e-check", "deposit check", "surplus funds"],
                True,
                0.98
            ),
            (
                "CONCEPT-003",
                "Encrypted_Anonymous_Channel",
                ["Communication_Medium"],
                ["Telegram_Chat", "WhatsApp_Group", "Signal_Chat"],
                ["telegram", "whatsapp", "signal", "chat interview", "download telegram", "dm hiring manager"],
                True,
                0.78
            ),
            (
                "CONCEPT-004",
                "Authentic_Employment_Agreement",
                ["Legal_Contract"],
                ["Standard_Offer_Letter", "Consulting_Agreement"],
                ["formal offer", "employment agreement", "health benefits", "annual salary", "401k matching"],
                False,
                0.05
            ),
            (
                "CONCEPT-005",
                "Identity_Credential_Harvesting",
                ["Information_Exfiltration"],
                ["SSN_Solicitation", "Banking_Login_Capture"],
                ["social security number", "ssn", "passport copy", "banking password", "atm pin"],
                True,
                0.99
            )
        ]

        for c_id, name, parents, children, tokens, is_pred, weight in concepts_data:
            self.concepts[name] = SemanticConceptNode(
                concept_id=c_id,
                concept_name=name,
                hypernym_parents=parents,
                hyponym_children=children,
                related_lexical_tokens=tokens,
                is_predatory_intent=is_pred,
                contextual_weight=weight
            )

    def get_concept(self, concept_name: str) -> Optional[SemanticConceptNode]:
        return self.concepts.get(concept_name)
