"""
JobGuard Core NLP - Cross-Attention Alignment & Clause Matching
Computes cross-attention alignment matrices between job description requirements
and uploaded offer letter clauses to detect unprompted discrepancies.
"""

import math
from typing import List, Tuple, Dict, Optional
from core.ml_inference.tensor_engine import Tensor, tensor_softmax


class CrossAttentionAligner:
    """Computes cross-attention matrix between Job Posting tokens and Offer Letter tokens."""

    def __init__(self, embed_dim: int = 32):
        self.embed_dim = embed_dim

    def compute_alignment_matrix(self, job_embeddings: Tensor, offer_embeddings: Tensor) -> Tensor:
        """Alignment = Softmax((Job_emb @ Offer_emb.T) / sqrt(d))."""
        # job_embeddings: (M, d), offer_embeddings: (N, d)
        raw_scores = job_embeddings.matmul_2d(offer_embeddings.transpose_2d())
        scale = 1.0 / math.sqrt(self.embed_dim)
        scaled_scores = raw_scores.mul(scale)
        return tensor_softmax(scaled_scores)

    def compute_clause_discrepancy_score(self, alignment_matrix: Tensor) -> float:
        """Measures maximum mismatch across clause alignments."""
        # Mean entropy across rows of alignment matrix
        m, n = alignment_matrix.shape
        total_entropy = 0.0
        
        for i in range(m):
            row = alignment_matrix.data[i * n:(i + 1) * n]
            row_entropy = -sum(p * math.log(max(1e-9, p)) for p in row)
            total_entropy += row_entropy

        avg_entropy = total_entropy / max(1, m)
        return round(min(100.0, avg_entropy * 25.0), 2)
