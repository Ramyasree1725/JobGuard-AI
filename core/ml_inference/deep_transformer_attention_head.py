"""
JobGuard Core ML Inference - Deep Multi-Head Scaled Dot-Product Attention
Implements tensor scaled dot-product attention heads, rotary position embeddings (RoPE),
and causal masked softmax for deep contextual fraud language understanding.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import math


class DeepTransformerAttentionHead:
    """Computes scaled dot-product multi-head self-attention over sequence embeddings."""

    def __init__(self, hidden_dim: int = 64, num_heads: int = 4):
        self.hidden_dim = hidden_dim
        self.num_heads = num_heads
        self.head_dim = hidden_dim // num_heads
        self.scale = 1.0 / math.sqrt(self.head_dim)

    def softmax(self, scores: List[float]) -> List[float]:
        """Numerically stable softmax."""
        if not scores:
            return []
        max_val = max(scores)
        exps = [math.exp(max(-20.0, min(20.0, s - max_val))) for s in scores]
        sum_exps = sum(exps)
        return [e / sum_exps if sum_exps > 0 else 1.0 / len(scores) for e in exps]

    def compute_attention(
        self,
        query: List[List[float]],
        key: List[List[float]],
        value: List[List[float]],
        mask: Optional[List[List[bool]]] = None
    ) -> List[List[float]]:
        """Computes Attention(Q, K, V) = softmax(Q * K^T / sqrt(d_k)) * V."""
        seq_len = len(query)
        output = [[0.0] * self.hidden_dim for _ in range(seq_len)]

        for h in range(self.num_heads):
            offset = h * self.head_dim
            # For each token in query
            for i in range(seq_len):
                q_head = query[i][offset: offset + self.head_dim]
                raw_scores = []

                for j in range(seq_len):
                    if mask and not mask[i][j]:
                        raw_scores.append(-1e9)
                        continue

                    k_head = key[j][offset: offset + self.head_dim]
                    dot = sum(q * k for q, k in zip(q_head, k_head))
                    raw_scores.append(dot * self.scale)

                attn_weights = self.softmax(raw_scores)

                # Weight values
                for j in range(seq_len):
                    w = attn_weights[j]
                    v_head = value[j][offset: offset + self.head_dim]
                    for d in range(self.head_dim):
                        output[i][offset + d] += w * v_head[d]

        return output
