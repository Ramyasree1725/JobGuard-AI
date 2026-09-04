"""
JobGuard Core Knowledge - Named Entity Disambiguation & Cross-Document Entity Linking
Links raw surface mentions in job texts to canonical corporate knowledge base entries
using prior popularity, string similarity, context similarity, and graph coherence models.
"""

import math
import re
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class EntityCandidate:
    kb_id: str
    canonical_name: str
    prior_probability: float
    description: str
    aliases: List[str] = field(default_factory=list)
    types: List[str] = field(default_factory=list)


@dataclass
class Mention:
    surface_form: str
    start_char: int
    end_char: int
    context_tokens: List[str]


@dataclass
class DisambiguationResult:
    mention: Mention
    assigned_entity: Optional[EntityCandidate]
    confidence_score: float
    feature_breakdown: Dict[str, float]


class EntityLinker:
    """Disambiguates corporate mentions to canonical employer knowledge bases."""

    def __init__(self):
        self._kb: Dict[str, EntityCandidate] = {}
        self._alias_index: Dict[str, List[str]] = {}  # alias -> list of kb_ids
        self._load_seed_kb()

    def _load_seed_kb(self) -> None:
        corporations = [
            EntityCandidate(
                kb_id="KB_GOOGLE",
                canonical_name="Google LLC",
                prior_probability=0.9,
                description="Multinational technology company focusing on search engine, cloud computing, and AI.",
                aliases=["Google", "Google Inc", "Alphabet", "Google Cloud", "Google Careers"],
                types=["Technology", "Enterprise", "Fortune500"]
            ),
            EntityCandidate(
                kb_id="KB_AMAZON",
                canonical_name="Amazon.com, Inc.",
                prior_probability=0.92,
                description="American multinational technology company focusing on e-commerce, cloud computing, and digital streaming.",
                aliases=["Amazon", "AWS", "Amazon Logistics", "Amazon Web Services", "Amazon Careers"],
                types=["E-Commerce", "Cloud", "Enterprise", "Fortune500"]
            ),
            EntityCandidate(
                kb_id="KB_MICROSOFT",
                canonical_name="Microsoft Corporation",
                prior_probability=0.88,
                description="American multinational corporation that produces computer software, consumer electronics, and personal computers.",
                aliases=["Microsoft", "MSFT", "Microsoft Azure", "Microsoft Careers"],
                types=["Technology", "Enterprise", "Fortune500"]
            ),
            EntityCandidate(
                kb_id="KB_APPLE",
                canonical_name="Apple Inc.",
                prior_probability=0.89,
                description="American multinational corporation and technology company that designs, develops, and sells consumer electronics.",
                aliases=["Apple", "Apple Computers", "Apple Care", "Apple Careers"],
                types=["Hardware", "Technology", "Enterprise", "Fortune500"]
            ),
            EntityCandidate(
                kb_id="KB_FEDEX",
                canonical_name="FedEx Corporation",
                prior_probability=0.75,
                description="American multinational delivery services company headquartered in Memphis, Tennessee.",
                aliases=["FedEx", "Federal Express", "FedEx Express", "FedEx Ground"],
                types=["Logistics", "Transportation", "Enterprise"]
            )
        ]

        for corp in corporations:
            self.register_entity(corp)

    def register_entity(self, entity: EntityCandidate) -> None:
        self._kb[entity.kb_id] = entity
        # Index canonical name
        clean_name = entity.canonical_name.lower()
        if clean_name not in self._alias_index:
            self._alias_index[clean_name] = []
        self._alias_index[clean_name].append(entity.kb_id)

        # Index aliases
        for alias in entity.aliases:
            clean_alias = alias.lower()
            if clean_alias not in self._alias_index:
                self._alias_index[clean_alias] = []
            if entity.kb_id not in self._alias_index[clean_alias]:
                self._alias_index[clean_alias].append(entity.kb_id)

    def extract_mentions(self, text: str) -> List[Mention]:
        """Extract candidate mention spans using dictionary matching and capitalization rules."""
        mentions = []
        words = text.split()
        context_window = [w.lower() for w in words]

        # Scan text for known aliases
        for alias, kb_ids in self._alias_index.items():
            pattern = r"\b" + re.escape(alias) + r"\b"
            for match in re.finditer(pattern, text, re.IGNORECASE):
                mentions.append(Mention(
                    surface_form=match.group(0),
                    start_char=match.start(),
                    end_char=match.end(),
                    context_tokens=context_window
                ))

        return mentions

    def disambiguate(self, mention: Mention) -> DisambiguationResult:
        """Score candidate KB entities against mention features and context."""
        clean_surface = mention.surface_form.lower()
        candidate_ids = self._alias_index.get(clean_surface, [])

        if not candidate_ids:
            # Fuzzy match
            for alias, ids in self._alias_index.items():
                if clean_surface in alias or alias in clean_surface:
                    candidate_ids.extend(ids)
            candidate_ids = list(set(candidate_ids))

        if not candidate_ids:
            return DisambiguationResult(
                mention=mention,
                assigned_entity=None,
                confidence_score=0.0,
                feature_breakdown={}
            )

        best_entity = None
        best_score = -1.0
        best_features = {}

        for kb_id in candidate_ids:
            candidate = self._kb[kb_id]
            
            # Feature 1: Prior popularity
            prior_score = candidate.prior_probability

            # Feature 2: Surface similarity
            exact_match = 1.0 if clean_surface == candidate.canonical_name.lower() else 0.8

            # Feature 3: Contextual overlap
            desc_tokens = set(candidate.description.lower().split())
            ctx_tokens = set(mention.context_tokens)
            overlap = len(desc_tokens.intersection(ctx_tokens))
            ctx_score = min(1.0, overlap / 5.0)

            # Combined weighted score
            total_score = 0.4 * prior_score + 0.3 * exact_match + 0.3 * ctx_score

            if total_score > best_score:
                best_score = total_score
                best_entity = candidate
                best_features = {
                    "prior_probability": prior_score,
                    "surface_similarity": exact_match,
                    "context_overlap_score": ctx_score,
                    "total_score": round(total_score, 4)
                }

        return DisambiguationResult(
            mention=mention,
            assigned_entity=best_entity,
            confidence_score=round(best_score, 4),
            feature_breakdown=best_features
        )
