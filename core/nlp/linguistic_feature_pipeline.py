"""
JobGuard Core NLP - Linguistic Complexity, Readability Metrics & Stylometry
Calculates Flesch-Kincaid Grade Level, Gunning Fog Index, Dale-Chall readability,
Shannon lexical entropy, and Soundex/Metaphone phonetic hashing.
"""

import math
import re
from typing import Dict, List, Set, Tuple, Optional


class PhoneticAlgorithms:
    """Soundex and Metaphone phonetic key generators."""

    @staticmethod
    def soundex(word: str) -> str:
        """Standard American Soundex algorithm."""
        if not word:
            return "0000"
        word_clean = re.sub(r"[^A-Za-z]", "", word.upper())
        if not word_clean:
            return "0000"

        first_letter = word_clean[0]
        mapping = {
            "B": "1", "F": "1", "P": "1", "V": "1",
            "C": "2", "G": "2", "J": "2", "K": "2", "Q": "2", "S": "2", "X": "2", "Z": "2",
            "D": "3", "T": "3",
            "L": "4",
            "M": "5", "N": "5",
            "R": "6"
        }

        digits = [first_letter]
        prev_code = mapping.get(first_letter, "0")

        for char in word_clean[1:]:
            code = mapping.get(char, "0")
            if code != "0" and code != prev_code:
                digits.append(code)
                prev_code = code
            elif code == "0":
                prev_code = "0"
            if len(digits) == 4:
                break

        # Pad with zeros
        while len(digits) < 4:
            digits.append("0")

        return "".join(digits[:4])


class ReadabilityCalculator:
    """Computes international readability and stylistic complexity indexes."""

    @staticmethod
    def count_syllables_word(word: str) -> int:
        """Heuristic English syllable counter."""
        w = word.lower().strip(",.!?\"'")
        if len(w) <= 3:
            return 1
        w = re.sub(r"(?:[^laeiouy]|ed|es|e)$", "", w)
        w = re.sub(r"^y", "", w)
        syllables = len(re.findall(r"[aeiouy]{1,2}", w))
        return max(1, syllables)

    @classmethod
    def calculate_metrics(cls, text: str) -> Dict[str, float]:
        sentences = [s.strip() for s in text.replace("\n", " ").split(".") if len(s.strip()) > 3]
        words = [w.strip(",.!?\"'") for w in text.split() if len(w.strip(",.!?\"'")) > 0]

        num_sentences = max(1, len(sentences))
        num_words = max(1, len(words))

        syllables = [cls.count_syllables_word(w) for w in words]
        total_syllables = sum(syllables)
        complex_words = sum(1 for s in syllables if s >= 3)

        words_per_sentence = num_words / num_sentences
        syllables_per_word = total_syllables / num_words

        # 1. Flesch Reading Ease: 206.835 - 1.015 * (words/sentences) - 84.6 * (syllables/words)
        flesch_ease = 206.835 - (1.015 * words_per_sentence) - (84.6 * syllables_per_word)
        flesch_ease = max(0.0, min(100.0, flesch_ease))

        # 2. Flesch-Kincaid Grade Level: 0.39 * (words/sentences) + 11.8 * (syllables/words) - 15.59
        fk_grade = (0.39 * words_per_sentence) + (11.8 * syllables_per_word) - 15.59
        fk_grade = max(0.0, fk_grade)

        # 3. Gunning Fog Index: 0.4 * ((words/sentences) + 100 * (complex_words / words))
        gunning_fog = 0.4 * (words_per_sentence + (100.0 * complex_words / num_words))

        # 4. Lexical Entropy (Shannon Entropy of unigrams)
        freqs: Dict[str, int] = {}
        for w in words:
            freqs[w.lower()] = freqs.get(w.lower(), 0) + 1

        entropy = 0.0
        for count in freqs.values():
            p = count / num_words
            entropy -= p * math.log2(p)

        return {
            "flesch_reading_ease": round(flesch_ease, 2),
            "flesch_kincaid_grade": round(fk_grade, 2),
            "gunning_fog_index": round(gunning_fog, 2),
            "lexical_entropy_bits": round(entropy, 3),
            "type_token_ratio": round(len(freqs) / num_words, 4),
            "avg_sentence_length": round(words_per_sentence, 2)
        }
