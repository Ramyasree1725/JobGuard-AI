"""
JobGuard Core Knowledge - Entity Resolution & Duplicate Recruiter Disambiguation
Fuzzy Jaro-Winkler, Levenshtein distance, TF-IDF cosine matching, and
record linkage algorithms to cluster aliases and spoofed corporate identities.
"""

import math
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, field


@dataclass
class EntityRecord:
    entity_id: str
    canonical_name: str
    aliases: List[str] = field(default_factory=list)
    email_domains: List[str] = field(default_factory=list)
    phone_numbers: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)


class StringDistance:
    """String similarity metrics for name and domain disambiguation."""

    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,      # Deletion
                    dp[i][j - 1] + 1,      # Insertion
                    dp[i - 1][j - 1] + cost # Substitution
                )

        return dp[m][n]

    @classmethod
    def normalized_levenshtein_similarity(cls, s1: str, s2: str) -> float:
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 1.0
        dist = cls.levenshtein_distance(s1, s2)
        return round(1.0 - (dist / max_len), 4)

    @staticmethod
    def jaro_winkler_similarity(s1: str, s2: str, p: float = 0.1) -> float:
        if s1 == s2:
            return 1.0
        len1, len2 = len(s1), len(s2)
        if len1 == 0 or len2 == 0:
            return 0.0

        match_distance = max(len1, len2) // 2 - 1
        s1_matches = [False] * len1
        s2_matches = [False] * len2
        matches = 0

        for i in range(len1):
            start = max(0, i - match_distance)
            end = min(i + match_distance + 1, len2)
            for j in range(start, end):
                if not s2_matches[j] and s1[i] == s2[j]:
                    s1_matches[i] = True
                    s2_matches[j] = True
                    matches += 1
                    break

        if matches == 0:
            return 0.0

        # Count transpositions
        t = 0
        k = 0
        for i in range(len1):
            if s1_matches[i]:
                while not s2_matches[k]:
                    k += 1
                if s1[i] != s2[k]:
                    t += 1
                k += 1
        transpositions = t / 2.0

        # Jaro similarity
        jaro = (matches / len1 + matches / len2 + (matches - transpositions) / matches) / 3.0

        # Common prefix length up to 4 chars
        l = 0
        for i in range(min(4, min(len1, len2))):
            if s1[i] == s2[i]:
                l += 1
            else:
                break

        return round(jaro + l * p * (1.0 - jaro), 4)


class EntityResolver:
    """Disambiguates and clusters entity mentions into canonical entity clusters."""

    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold
        self.canonical_entities: Dict[str, EntityRecord] = {}

    def register_canonical_entity(self, entity: EntityRecord) -> None:
        self.canonical_entities[entity.entity_id] = entity

    def resolve_entity(self, name: str, domain: Optional[str] = None) -> Optional[Tuple[EntityRecord, float]]:
        """Find best matching canonical entity for an observed recruiter name/domain."""
        best_match = None
        highest_score = 0.0

        name_clean = name.strip().lower()

        for entity in self.canonical_entities.values():
            # Name similarity
            score_canonical = StringDistance.jaro_winkler_similarity(name_clean, entity.canonical_name.lower())
            
            alias_scores = [
                StringDistance.jaro_winkler_similarity(name_clean, alias.lower())
                for alias in entity.aliases
            ]
            max_name_score = max([score_canonical] + alias_scores)

            # Domain bonus/penalty
            domain_bonus = 0.0
            if domain:
                if any(d.lower() == domain.lower() for d in entity.email_domains):
                    domain_bonus = 0.15
                elif any(domain.lower() in d.lower() for d in entity.email_domains):
                    domain_bonus = 0.05

            total_score = min(1.0, max_name_score + domain_bonus)

            if total_score > highest_score and total_score >= self.threshold:
                highest_score = total_score
                best_match = entity

        if best_match:
            return best_match, round(highest_score, 4)
        return None
