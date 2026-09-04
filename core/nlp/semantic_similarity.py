"""
JobGuard Core NLP - Semantic Similarity & Sentence Cosine Embeddings
Computes dense semantic cosine similarities, Jaccard token overlaps,
and Word Mover's Distance (WMD) approximations between job posts.
"""

import math
from typing import List, Dict, Set, Tuple, Optional


class SemanticSimilarityEvaluator:
    """Semantic comparison engine for detecting plagiarized scam templates."""

    @staticmethod
    def jaccard_similarity(s1: str, s2: str) -> float:
        set1 = set(s1.lower().split())
        set2 = set(s2.lower().split())
        if not set1 or not set2:
            return 0.0
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return round(intersection / union, 4)

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        if len(v1) != len(v2) or not v1:
            return 0.0
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return round(dot / (norm1 * norm2), 4)
