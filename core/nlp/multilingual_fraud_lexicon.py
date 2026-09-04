"""
JobGuard Core NLP - Multilingual Recruitment Fraud Lexicon
Maintains comprehensive multilingual threat keywords across English, Spanish,
French, German, Portuguese, Hindi, Arabic, and Tagalog for global candidate defense.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class LexiconEntry:
    phrase: str
    language_iso: str
    threat_category: str
    severity_weight: float
    english_translation: str


class MultilingualFraudLexicon:
    """Multi-language keyword and idiom repository for cross-border scam detection."""

    def __init__(self):
        self.entries: List[LexiconEntry] = []
        self._compiled_regexes: Dict[str, List[Tuple[re.Pattern, LexiconEntry]]] = {}
        self._initialize_multilingual_lexicon()

    def _initialize_multilingual_lexicon(self) -> None:
        """Seed verified fraudulent recruitment phrases across major global languages."""

        # Spanish (ES)
        self._add_entry("tarifa de registro", "es", "UPFRONT_FEE", 0.85, "registration fee")
        self._add_entry("cheque de equipo", "es", "COUNTERFEIT_CHECK", 0.90, "equipment check")
        self._add_entry("entrevista por telegram", "es", "CHAT_INTERVIEW", 0.75, "telegram interview")
        self._add_entry("recargar saldo usdt", "es", "CRYPTO_TASK", 0.95, "recharge usdt balance")

        # French (FR)
        self._add_entry("frais de dossier", "fr", "UPFRONT_FEE", 0.85, "application/file fee")
        self._add_entry("chèque pour matériel", "fr", "COUNTERFEIT_CHECK", 0.90, "equipment check")
        self._add_entry("entretien sur telegram", "fr", "CHAT_INTERVIEW", 0.75, "telegram interview")

        # German (DE)
        self._add_entry("anmeldegebühr vorab", "de", "UPFRONT_FEE", 0.85, "upfront registration fee")
        self._add_entry("ausstattungsscheck einlösen", "de", "COUNTERFEIT_CHECK", 0.90, "cash equipment check")
        self._add_entry("vorabüberweisung für schulung", "de", "UPFRONT_FEE", 0.90, "advance transfer for training")

        # Portuguese (PT)
        self._add_entry("taxa de inscrição", "pt", "UPFRONT_FEE", 0.85, "registration fee")
        self._add_entry("depósito para treinamento", "pt", "UPFRONT_FEE", 0.90, "training deposit")
        self._add_entry("entrevista pelo whatsapp", "pt", "CHAT_INTERVIEW", 0.70, "whatsapp interview")

        # Hindi / Hinglish (HI)
        self._add_entry("registration fees jama kare", "hi", "UPFRONT_FEE", 0.90, "deposit registration fees")
        self._add_entry("daily task earning usdt", "hi", "CRYPTO_TASK", 0.95, "daily task earning usdt")
        self._add_entry("telegram par contact kare", "hi", "CHAT_INTERVIEW", 0.80, "contact on telegram")

        # Tagalog (TL)
        self._add_entry("bayad sa pagproseso", "tl", "UPFRONT_FEE", 0.85, "processing payment")
        self._add_entry("online tasking araw araw", "tl", "CRYPTO_TASK", 0.90, "daily online tasking")

    def _add_entry(self, phrase: str, lang: str, cat: str, weight: float, trans: str) -> None:
        entry = LexiconEntry(phrase, lang, cat, weight, trans)
        self.entries.append(entry)
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
        self._compiled_regexes.setdefault(lang, []).append((pattern, entry))

    def scan_multilingual_text(self, text: str, language_hint: Optional[str] = None) -> List[LexiconEntry]:
        """Scans text against multilingual lexicon patterns."""
        matches: List[LexiconEntry] = []
        
        langs_to_scan = [language_hint] if language_hint and language_hint in self._compiled_regexes else list(self._compiled_regexes.keys())

        for lang in langs_to_scan:
            for pattern, entry in self._compiled_regexes.get(lang, []):
                if pattern.search(text):
                    matches.append(entry)

        return matches
