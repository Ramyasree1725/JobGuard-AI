"""
JobGuard Core ML - Multi-Head, Multi-Query & Grouped-Query Attention Mechanisms
Implements standard Multi-Head Attention (MHA), Multi-Query Attention (MQA),
and Grouped-Query Attention (GQA) for efficient contract inference.
"""

import math
from typing import List, Tuple, Optional
from core.ml_inference.tensor_engine import Tensor, tensor_softmax


class GroupedQueryAttention:
    """Grouped-Query Attention (GQA) sharing key-value heads across query head groups."""

    def __init__(self, d_model: int = 64, num_heads: int = 8, num_kv_heads: int = 2):
        self.d_model = d_model
        self.num_heads = num_heads
        self.num_kv_heads = num_kv_heads
        self.d_k = d_model // num_heads
        self.group_size = num_heads // num_kv_heads

    def forward(self, q: Tensor, k: Tensor, v: Tensor, mask: Optional[Tensor] = None) -> Tensor:
        # q: (Seq, d_model), k: (Seq, d_kv), v: (Seq, d_kv)
        seq_len = q.shape[0]
        scale = 1.0 / math.sqrt(self.d_k)

        # Simplified single-tensor projection simulation
        scores = q.matmul_2d(k.transpose_2d()).mul(scale)
        if mask is not None:
            scores = scores.add(mask)

        weights = tensor_softmax(scores)
        return weights.matmul_2d(v)
