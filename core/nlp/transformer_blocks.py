"""
Aetheris NLP & Cognitive Engine: Transformer Decoder Blocks & Autoregressive Model
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
import random
from typing import List, Tuple, Sequence, Optional
from core.nlp.attention import MultiHeadAttention, PositionalEncoding


class LayerNorm:
    """Standard Layer Normalization over embedding dimension."""
    def __init__(self, d_model: int, eps: float = 1e-5) -> None:
        self.d_model = d_model
        self.eps = eps
        self.gamma = [1.0] * d_model
        self.beta = [0.0] * d_model

    def forward(self, x: List[List[float]]) -> List[List[float]]:
        out: List[List[float]] = []
        for vec in x:
            mean = sum(vec) / float(self.d_model)
            var = sum((v - mean) ** 2 for v in vec) / float(self.d_model)
            std = math.sqrt(var + self.eps)
            norm_vec = [
                ((vec[i] - mean) / std) * self.gamma[i] + self.beta[i]
                for i in range(self.d_model)
            ]
            out.append(norm_vec)
        return out


class FeedForwardNetwork:
    """Two-layer MLP with GELU / SwiGLU activation."""
    def __init__(self, d_model: int = 64, d_ff: int = 128, seed: Optional[int] = None) -> None:
        self.d_model = d_model
        self.d_ff = d_ff
        self.rng = random.Random(seed)

        self.W1 = self._init_weights(d_ff, d_model)
        self.b1 = [0.0] * d_ff
        self.W2 = self._init_weights(d_model, d_ff)
        self.b2 = [0.0] * d_model

    def _init_weights(self, rows: int, cols: int) -> List[List[float]]:
        bound = math.sqrt(6.0 / (rows + cols))
        return [[self.rng.uniform(-bound, bound) for _ in range(cols)] for _ in range(rows)]

    def _gelu(self, x: float) -> float:
        return 0.5 * x * (1.0 + math.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * x ** 3)))

    def forward(self, x: List[List[float]]) -> List[List[float]]:
        out: List[List[float]] = []
        for vec in x:
            # Layer 1
            hidden = [
                self._gelu(sum(self.W1[r][c] * vec[c] for c in range(self.d_model)) + self.b1[r])
                for r in range(self.d_ff)
            ]
            # Layer 2
            proj = [
                sum(self.W2[r][c] * hidden[c] for c in range(self.d_ff)) + self.b2[r]
                for r in range(self.d_model)
            ]
            out.append(proj)
        return out


class TransformerDecoderBlock:
    """Full Pre-LayerNorm Transformer Decoder Layer."""
    def __init__(self, d_model: int = 64, num_heads: int = 4, d_ff: int = 128, seed: Optional[int] = None) -> None:
        self.attn = MultiHeadAttention(d_model, num_heads, seed=seed)
        self.ln1 = LayerNorm(d_model)
        self.ffn = FeedForwardNetwork(d_model, d_ff, seed=seed)
        self.ln2 = LayerNorm(d_model)
        self.d_model = d_model

    def forward(self, x: List[List[float]]) -> List[List[float]]:
        # Pre-LN Self-Attention with Residual
        norm_x = self.ln1.forward(x)
        attn_out = self.attn.forward(norm_x, norm_x, norm_x, is_causal=True)
        res1 = [[x[r][c] + attn_out[r][c] for c in range(self.d_model)] for r in range(len(x))]

        # Pre-LN FeedForward with Residual
        norm_res1 = self.ln2.forward(res1)
        ffn_out = self.ffn.forward(norm_res1)
        res2 = [[res1[r][c] + ffn_out[r][c] for c in range(self.d_model)] for r in range(len(res1))]

        return res2


class ResearchTransformerLM:
    """Complete Autoregressive Transformer Language Model."""
    def __init__(self, vocab_size: int = 1000, d_model: int = 64, num_layers: int = 3, num_heads: int = 4, seed: Optional[int] = None) -> None:
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.rng = random.Random(seed)

        # Token embedding table (vocab_size x d_model)
        self.token_embeddings = [
            [self.rng.uniform(-0.1, 0.1) for _ in range(d_model)]
            for _ in range(vocab_size)
        ]
        self.pos_enc = PositionalEncoding(d_model=d_model)
        self.layers = [
            TransformerDecoderBlock(d_model, num_heads, seed=seed)
            for _ in range(num_layers)
        ]
        self.final_ln = LayerNorm(d_model)

    def forward(self, token_ids: Sequence[int]) -> List[List[float]]:
        seq_len = len(token_ids)
        if seq_len == 0:
            return []

        # Lookup embeddings + Add positional encoding
        pe = self.pos_enc.get_encoding(seq_len)
        h = [
            [self.token_embeddings[token_ids[i]][c] + pe[i][c] for c in range(self.d_model)]
            for i in range(seq_len)
        ]

        # Pass through decoder blocks
        for layer in self.layers:
            h = layer.forward(h)

        h_norm = self.final_ln.forward(h)

        # Compute output logits: h * W_embed^T (tied weights)
        logits: List[List[float]] = []
        for vec in h_norm:
            token_logits = [
                sum(vec[c] * self.token_embeddings[v_idx][c] for c in range(self.d_model))
                for v_idx in range(self.vocab_size)
            ]
            logits.append(token_logits)

        return logits
