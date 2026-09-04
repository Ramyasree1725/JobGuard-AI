"""
JobGuard Core NLP - WordNet Domain Synsets & Hyponym/Hypernym Semantic Hierarchy
Maintains semantic synsets, definitions, hypernym trees, and meronym relations
for recruitment terminology, financial demands, and legal contracts.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class SynsetDefinition:
    synset_id: str  # e.g., "fee.n.01"
    lemma_names: List[str]
    pos: str  # "n", "v", "a", "r"
    definition: str
    examples: List[str]
    hypernym_ids: List[str] = field(default_factory=list)
    hyponym_ids: List[str] = field(default_factory=list)
    meronym_ids: List[str] = field(default_factory=list)


class WordNetSemanticLexicon:
    """Master repository containing WordNet-structured lexical relations."""

    def __init__(self):
        self.synsets: Dict[str, SynsetDefinition] = {}
        self._lemma_to_synsets: Dict[str, List[str]] = {}
        self._populate_domain_synsets()

    def register(self, s: SynsetDefinition) -> None:
        self.synsets[s.synset_id] = s
        for lemma in s.lemma_names:
            clean = lemma.lower()
            if clean not in self._lemma_to_synsets:
                self._lemma_to_synsets[clean] = []
            self._lemma_to_synsets[clean].append(s.synset_id)

    def _populate_domain_synsets(self) -> None:
        """Populate synset definitions."""
        entries = [
            SynsetDefinition(
                synset_id="charge.n.01",
                lemma_names=["charge", "fee", "cost", "price"],
                pos="n",
                definition="A fixed financial demand or price asked for goods or services.",
                examples=["The recruiter requested an upfront registration fee."],
                hypernym_ids=["payment.n.01"],
                hyponym_ids=["registration_fee.n.01", "deposit.n.01"]
            ),
            SynsetDefinition(
                synset_id="deposit.n.01",
                lemma_names=["deposit", "security_deposit", "caution_money"],
                pos="n",
                definition="A sum of money placed or kept in a bank account, usually to gain interest or as a pledge.",
                examples=["A refundable security deposit was required before laptop dispatch."],
                hypernym_ids=["charge.n.01"]
            ),
            SynsetDefinition(
                synset_id="check.n.01",
                lemma_names=["check", "cheque", "bank_check", "cashier_check"],
                pos="n",
                definition="A written order directing a bank to pay money as instructed.",
                examples=["The company sent a check for purchasing home office hardware."],
                hypernym_ids=["negotiable_instrument.n.01"]
            ),
            SynsetDefinition(
                synset_id="impersonation.n.01",
                lemma_names=["impersonation", "personation", "identity_theft"],
                pos="n",
                definition="Pretending to be another person for the purpose of fraud or deception.",
                examples=["The scam involved impersonation of executive talent recruiters."],
                hypernym_ids=["fraud.n.01"]
            ),
            SynsetDefinition(
                synset_id="contract.n.01",
                lemma_names=["contract", "agreement", "offer_letter", "covenant"],
                pos="n",
                definition="A binding agreement between two or more persons that is enforceable by law.",
                examples=["The formal employment contract was verified for compliance."],
                hypernym_ids=["legal_document.n.01"]
            )
        ]

        for e in entries:
            self.register(e)

    def get_synsets(self, word: str) -> List[SynsetDefinition]:
        ids = self._lemma_to_synsets.get(word.strip().lower(), [])
        return [self.synsets[sid] for sid in ids]
