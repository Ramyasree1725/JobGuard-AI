"""
Aetheris Recommendation & RL: Two-Tower Dense Embeddings & Ranking Metrics
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
import random
from typing import List, Dict, Tuple, Sequence, Optional


class TwoTowerDenseRetriever:
    """
    Two-Tower Deep Neural Embedding Retrieval Architecture:
    Query Tower: user_context -> embedding u
    Candidate Tower: item_features -> embedding v
    Score = cosine_similarity(u, v)
    """
    def __init__(self, user_dim: int = 16, item_dim: int = 16, embedding_dim: int = 32, seed: Optional[int] = None) -> None:
        self.user_dim = user_dim
        self.item_dim = item_dim
        self.embed_dim = embedding_dim
        self.rng = random.Random(seed)

        # Tower Weights
        self.W_user = self._init_weights(embedding_dim, user_dim)
        self.W_item = self._init_weights(embedding_dim, item_dim)

    def _init_weights(self, rows: int, cols: int) -> List[List[float]]:
        bound = math.sqrt(6.0 / (rows + cols))
        return [[self.rng.uniform(-bound, bound) for _ in range(cols)] for _ in range(rows)]

    def _normalize(self, vec: List[float]) -> List[float]:
        norm = math.sqrt(sum(v * v for v in vec))
        if norm < 1e-9:
            return vec
        return [v / norm for v in vec]

    def encode_user(self, user_features: Sequence[float]) -> List[float]:
        emb = [sum(self.W_user[r][c] * user_features[c] for c in range(self.user_dim)) for r in range(self.embed_dim)]
        return self._normalize(emb)

    def encode_item(self, item_features: Sequence[float]) -> List[float]:
        emb = [sum(self.W_item[r][c] * item_features[c] for c in range(self.item_dim)) for r in range(self.embed_dim)]
        return self._normalize(emb)

    def rank_candidates(
        self,
        user_features: Sequence[float],
        candidate_items: List[Tuple[str, Sequence[float]]],
        top_k: int = 10
    ) -> List[Tuple[str, float]]:
        """Ranks candidates by cosine dot-product similarity."""
        u_emb = self.encode_user(user_features)
        scored: List[Tuple[str, float]] = []

        for item_id, item_feats in candidate_items:
            v_emb = self.encode_item(item_feats)
            sim = sum(u_emb[i] * v_emb[i] for i in range(self.embed_dim))
            scored.append((item_id, sim))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]


class RecommendationMetrics:
    """Standard evaluation metrics for Information Retrieval and Recommender Systems."""

    @staticmethod
    def dcg_at_k(relevance_scores: Sequence[float], k: int) -> float:
        score = 0.0
        for i in range(min(len(relevance_scores), k)):
            rel = relevance_scores[i]
            score += (math.pow(2.0, rel) - 1.0) / math.log2(float(i + 2))
        return score

    @staticmethod
    def ndcg_at_k(relevance_scores: Sequence[float], k: int) -> float:
        dcg = RecommendationMetrics.dcg_at_k(relevance_scores, k)
        ideal_relevance = sorted(relevance_scores, reverse=True)
        idcg = RecommendationMetrics.dcg_at_k(ideal_relevance, k)
        if idcg < 1e-12:
            return 0.0
        return dcg / idcg

    @staticmethod
    def recall_at_k(recommended_ids: Sequence[str], ground_truth_ids: Sequence[str], k: int) -> float:
        if not ground_truth_ids:
            return 0.0
        rec_set = set(recommended_ids[:k])
        gt_set = set(ground_truth_ids)
        hits = len(rec_set.intersection(gt_set))
        return float(hits) / float(len(gt_set))

    @staticmethod
    def mrr(recommended_ids: Sequence[str], target_id: str) -> float:
        for idx, rec_id in enumerate(recommended_ids):
            if rec_id == target_id:
                return 1.0 / float(idx + 1)
        return 0.0
