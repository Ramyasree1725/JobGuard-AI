"""
JobGuard Core NLP - Coercive Sentiment & Urgency Lexicon Analyzer
Computes psychological pressure scores, high-urgency language indexes,
and deceptive enthusiasm indicators across recruitment messages.
"""

from typing import Dict, List, Tuple, Optional


class UrgencySentimentAnalyzer:
    """Evaluates psychological pressure and coercive urgency in recruitment texts."""

    URGENCY_WORDS: Dict[str, float] = {
        "immediate": 2.5,
        "urgent": 3.0,
        "urgently": 3.2,
        "now": 1.5,
        "today": 1.8,
        "hurry": 3.5,
        "limited": 2.2,
        "expires": 2.8,
        "deadline": 2.0,
        "forfeit": 3.0,
        "instant": 2.4,
        "fast": 1.5,
        "quick": 1.5,
        "last chance": 3.8
    }

    ENTHUSIASM_BAIT_WORDS: Dict[str, float] = {
        "guaranteed": 3.0,
        "unlimited": 2.5,
        "dream job": 3.2,
        "easy money": 4.0,
        "passive income": 3.5,
        "congratulations": 2.0,
        "selected": 2.2,
        "blessings": 2.5
    }

    def analyze_pressure_score(self, text: str) -> Dict[str, Any]:
        """Compute aggregate psychological urgency and manipulative tone score."""
        text_lower = text.lower()
        words = text_lower.split()
        word_count = max(1, len(words))

        urgency_score = 0.0
        detected_urgency = []

        for word, weight in self.URGENCY_WORDS.items():
            if word in text_lower:
                urgency_score += weight
                detected_urgency.append(word)

        bait_score = 0.0
        detected_bait = []
        for word, weight in self.ENTHUSIASM_BAIT_WORDS.items():
            if word in text_lower:
                bait_score += weight
                detected_bait.append(word)

        total_pressure = min(100.0, (urgency_score * 10.0) + (bait_score * 8.0))

        return {
            "pressure_score": round(total_pressure, 1),
            "is_coercive": total_pressure >= 30.0,
            "detected_urgency_cues": detected_urgency,
            "detected_bait_cues": detected_bait,
            "density": round((len(detected_urgency) + len(detected_bait)) / word_count, 4)
        }
