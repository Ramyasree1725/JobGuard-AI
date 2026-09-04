"""
JobGuard Backend Service - Scam Signature In-Memory Vector Database
Implements high-dimensional dense vector embeddings index, cosine similarity search,
and nearest-neighbor clustering for real-time scam message semantic classification.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import math
import hashlib


@dataclass
class VectorDocument:
    doc_id: str
    text_snippet: str
    category: str
    vector: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchResult:
    document: VectorDocument
    similarity_score: float  # -1.0 to 1.0 (Cosine similarity)
    distance: float


class ScamSignatureVectorDB:
    """In-memory dense vector index with cosine similarity and k-NN search."""

    def __init__(self, dimension: int = 128):
        self.dimension = dimension
        self.documents: Dict[str, VectorDocument] = {}
        self._seed_reference_embeddings()

    def _seed_reference_embeddings(self) -> None:
        """Seeds known scam patterns with simulated deterministic dense embeddings."""
        patterns = [
            ("VEC-001", "We will mail you a check for home office supplies. Deposit and send remaining funds to vendor.", "COUNTERFEIT_CHECK"),
            ("VEC-002", "Kindly download Telegram and message our hiring manager for immediate text interview.", "TELEGRAM_INTERVIEW"),
            ("VEC-003", "Earn $500 daily rating apps on our platform. Deposit USDT to unlock VIP level 1.", "TASK_CRYPTO_SCHEME"),
            ("VEC-004", "Pay upfront $200 onboarding fee for laptop insurance, 100% refundable on first paycheck.", "UPFRONT_FEE"),
            ("VEC-005", "Please send front and back of your driver license and SSN for initial screening questionnaire.", "PII_HARVEST")
        ]

        for doc_id, text, cat in patterns:
            vec = self._embed_text(text)
            self.insert(doc_id, text, cat, vec)

    def _embed_text(self, text: str) -> List[float]:
        """Generates a deterministic pseudo-embedding vector for text similarity matching."""
        words = text.lower().split()
        vec = [0.0] * self.dimension
        for word in words:
            h = int(hashlib.md5(word.encode()).hexdigest(), 16)
            for i in range(self.dimension):
                # Hash feature projection
                bit = (h >> (i % 32)) & 1
                vec[i] += 1.0 if bit else -1.0

        # L2 Normalize
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec

    def insert(self, doc_id: str, text: str, category: str, vector: Optional[List[float]] = None) -> None:
        """Inserts a document embedding into the index."""
        if vector is None:
            vector = self._embed_text(text)
        self.documents[doc_id] = VectorDocument(
            doc_id=doc_id,
            text_snippet=text,
            category=category,
            vector=vector
        )

    def search_nearest(self, query_text: str, top_k: int = 3) -> List[SearchResult]:
        """Finds top-k nearest semantic matches using cosine similarity."""
        query_vec = self._embed_text(query_text)
        results: List[SearchResult] = []

        for doc in self.documents.values():
            sim = self._cosine_similarity(query_vec, doc.vector)
            dist = 1.0 - sim
            results.append(SearchResult(
                document=doc,
                similarity_score=sim,
                distance=dist
            ))

        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:top_k]

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """Computes dot product of two unit-normalized vectors."""
        dot = sum(a * b for a, b in zip(v1, v2))
        return max(-1.0, min(1.0, dot))
