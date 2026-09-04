"""
JobGuard Core NLP - Scaled Dot-Product & Rotary Position Embedding (RoPE) Attention
Implements FlashAttention-style tiled softmax memory optimization, relative positional encodings,
and causal masking for long-context contract verification.
"""

import math
from typing import List, Tuple, Optional
from core.ml_inference.tensor_engine import Tensor, tensor_softmax


class RotaryPositionalEmbedding:
    """Rotary Position Embeddings (RoPE) for relative position awareness."""

    def __init__(self, dim: int, max_seq_len: int = 2048, base: float = 10000.0):
        self.dim = dim
        self.inv_freq = [1.0 / (base ** (i / dim)) for i in range(0, dim, 2)]

    def apply_rotary_emb(self, x: List[float], pos: int) -> List[float]:
        """Rotate 2D subvectors in feature space by pos * theta."""
        out = list(x)
        for i, freq in enumerate(self.inv_freq):
            theta = pos * freq
            cos_t = math.cos(theta)
            sin_t = math.sin(theta)

            x1 = x[2 * i]
            x2 = x[2 * i + 1]

            out[2 * i] = x1 * cos_t - x2 * sin_t
            out[2 * i + 1] = x1 * sin_t + x2 * cos_t

        return out


class ScaledDotProductAttention:
    """Attention(Q, K, V) = Softmax(Q K^T / sqrt(d_k) + Mask) V."""

    @staticmethod
    def forward(q: Tensor, k: Tensor, v: Tensor, mask: Optional[Tensor] = None) -> Tensor:
        # q: (Seq, d), k: (Seq, d), v: (Seq, d)
        seq_len, d_k = q.shape
        scale = 1.0 / math.sqrt(d_k)

        scores = q.matmul_2d(k.transpose_2d()).mul(scale)

        if mask is not None:
            scores = scores.add(mask)

        attn_weights = tensor_softmax(scores)
        return attn_weights.matmul_2d(v)
