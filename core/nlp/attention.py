"""
Aetheris NLP & Cognitive Engine: Multi-Head Scaled Dot-Product Attention & Positional Encodings
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
import random
from typing import List, Tuple, Sequence, Optional


class PositionalEncoding:
    """
    Sinusoidal Positional Encoding (Vaswani et al.):
    PE(pos, 2i)   = sin(pos / 10000^(2i / d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i / d_model))
    """
    def __init__(self, d_model: int = 64, max_len: int = 512) -> None:
        self.d_model = d_model
        self.max_len = max_len
        self.pe_table: List[List[float]] = []
        self._build_table()

    def _build_table(self) -> None:
        self.pe_table = [[0.0] * self.d_model for _ in range(self.max_len)]
        for pos in range(self.max_len):
            for i in range(0, self.d_model, 2):
                denom = math.pow(10000.0, float(i) / float(self.d_model))
                self.pe_table[pos][i] = math.sin(pos / denom)
                if i + 1 < self.d_model:
                    self.pe_table[pos][i + 1] = math.cos(pos / denom)

    def get_encoding(self, seq_len: int) -> List[List[float]]:
        return self.pe_table[:seq_len]


class MultiHeadAttention:
    """
    Multi-Head Scaled Dot-Product Attention from scratch:
    Attention(Q, K, V) = softmax(Q * K^T / sqrt(d_k) + Mask) * V
    """
    def __init__(self, d_model: int = 64, num_heads: int = 4, seed: Optional[int] = None) -> None:
        if d_model % num_heads != 0:
            raise ValueError(f"d_model ({d_model}) must be divisible by num_heads ({num_heads})")
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.scale = 1.0 / math.sqrt(float(self.d_k))
        self.rng = random.Random(seed)

        # Weight matrices: W_q, W_k, W_v, W_o (d_model x d_model)
        self.W_q = self._init_weights(d_model, d_model)
        self.W_k = self._init_weights(d_model, d_model)
        self.W_v = self._init_weights(d_model, d_model)
        self.W_o = self._init_weights(d_model, d_model)

    def _init_weights(self, rows: int, cols: int) -> List[List[float]]:
        bound = math.sqrt(6.0 / (rows + cols))
        return [[self.rng.uniform(-bound, bound) for _ in range(cols)] for _ in range(rows)]

    def _matmul_vector(self, mat: List[List[float]], vec: Sequence[float]) -> List[float]:
        return [sum(row[c] * vec[c] for c in range(len(vec))) for row in mat]

    def _softmax(self, logits: List[float], mask_indices: Optional[List[int]] = None) -> List[float]:
        max_val = max(logits)
        exps = [math.exp(v - max_val) for v in logits]
        if mask_indices is not None:
            for idx in mask_indices:
                exps[idx] = 0.0
        sum_exp = sum(exps)
        if sum_exp < 1e-12:
            return [1.0 / len(logits)] * len(logits)
        return [e / sum_exp for e in exps]

    def forward(
        self,
        query: List[List[float]],
        key: List[List[float]],
        value: List[List[float]],
        is_causal: bool = True
    ) -> List[List[float]]:
        """
        Forward pass of Multi-Head Self-Attention.
        Input shapes: (seq_len, d_model)
        """
        seq_len = len(query)
        if seq_len == 0:
            return []

        # Project Q, K, V
        Q_proj = [self._matmul_vector(self.W_q, q_vec) for q_vec in query]
        K_proj = [self._matmul_vector(self.W_k, k_vec) for k_vec in key]
        V_proj = [self._matmul_vector(self.W_v, v_vec) for v_vec in value]

        head_outputs: List[List[List[float]]] = []

        # Compute per-head attention
        for h in range(self.num_heads):
            offset = h * self.d_k
            # Extract head slice (seq_len x d_k)
            Q_h = [vec[offset:offset + self.d_k] for vec in Q_proj]
            K_h = [vec[offset:offset + self.d_k] for vec in K_proj]
            V_h = [vec[offset:offset + self.d_k] for vec in V_proj]

            head_out: List[List[float]] = []

            for i in range(seq_len):
                # Attention scores: Q_h[i] . K_h[j] * scale
                scores: List[float] = []
                mask_indices: List[int] = []
                for j in range(seq_len):
                    if is_causal and j > i:
                        scores.append(-1e9)
                        mask_indices.append(j)
                    else:
                        dot = sum(Q_h[i][k] * K_h[j][k] for k in range(self.d_k))
                        scores.append(dot * self.scale)

                weights = self._softmax(scores, mask_indices if is_causal else None)

                # Weighted sum over V_h
                out_vec = [0.0] * self.d_k
                for j in range(seq_len):
                    for k in range(self.d_k):
                        out_vec[k] += weights[j] * V_h[j][k]
                head_out.append(out_vec)

            head_outputs.append(head_out)

        # Concatenate head outputs along embedding dimension
        concat_out: List[List[float]] = []
        for i in range(seq_len):
            row_concat: List[float] = []
            for h in range(self.num_heads):
                row_concat.extend(head_outputs[h][i])
            # Project through W_o
            final_vec = self._matmul_vector(self.W_o, row_concat)
            concat_out.append(final_vec)

        return concat_out
