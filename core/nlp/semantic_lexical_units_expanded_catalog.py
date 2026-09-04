"""
JobGuard Core NLP - Semantic Lexical Units & Synset Expanded Catalog
Provides extensive synonym rings, hyponym trees, and adversarial lexical variants
for deep linguistic decomposition and semantic parsing of recruitment fraud.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class LexicalSynset:
    synset_id: str
    canonical_lemma: str
    part_of_speech: str  # 'NOUN', 'VERB', 'ADJ', 'ADV'
    synonyms: List[str]
    hyponyms: List[str]
    threat_valence: float  # -1.0 (benign) to 1.0 (heavily associated with fraud)
    definition: str


class SemanticLexicalUnitsExpandedCatalog:
    """Master expanded lexical knowledge base for recruitment semantic parsing."""

    def __init__(self):
        self.synsets: Dict[str, LexicalSynset] = {}
        self.lemma_to_synset: Dict[str, str] = {}
        self._initialize_synsets()

    def _initialize_synsets(self) -> None:
        """Register lexical synsets."""

        synsets_data = [
            ("SYN-FEE-01", "onboarding_fee", "NOUN", ["registration fee", "processing charge", "application deposit", "setup cost", "clearance fee"], ["insurance deposit", "laptop fee"], 0.95, "A monetary amount demanded from an applicant prior to employment."),
            ("SYN-CHK-01", "counterfeit_check", "NOUN", ["cashier check", "official bank draft", "certified e-check", "advance cheque", "equipment draft"], ["corporate cashier order", "pre-printed check"], 0.98, "A fraudulent commercial paper instrument used in overpayment schemes."),
            ("SYN-VND-01", "approved_vendor", "NOUN", ["authorized supplier", "certified IT provider", "designated equipment merchant", "hardware vendor"], ["laptop dispatch merchant", "home office supplier"], 0.90, "A third-party entity controlled by scammers to receive check surplus wire transfers."),
            ("SYN-MSG-01", "instant_messaging", "NOUN", ["telegram", "whatsapp", "signal", "google chat", "hangouts", "wire app"], ["telegram channel", "whatsapp group"], 0.75, "Consumer messaging applications used to evade enterprise email verification."),
            ("SYN-WAG-01", "compensation_rate", "NOUN", ["hourly rate", "daily wage", "weekly salary", "annual compensation", "remuneration"], ["base pay", "stipend"], 0.10, "The legal monetary remuneration promised to a worker for employment services.")
        ]

        for s_id, lemma, pos, syns, hypos, val, defn in synsets_data:
            synset = LexicalSynset(
                synset_id=s_id,
                canonical_lemma=lemma,
                part_of_speech=pos,
                synonyms=syns,
                hyponyms=hypos,
                threat_valence=val,
                definition=defn
            )
            self.synsets[s_id] = synset
            self.lemma_to_synset[lemma.lower()] = s_id
            for s in syns:
                self.lemma_to_synset[s.lower()] = s_id

    def lookup_lemma(self, phrase: str) -> Optional[LexicalSynset]:
        """Finds matching synset for an input phrase."""
        s_id = self.lemma_to_synset.get(phrase.lower().strip())
        return self.synsets.get(s_id) if s_id else None
