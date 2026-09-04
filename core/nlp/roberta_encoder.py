"""
JobGuard Core NLP - RoBERTa-Style Deep Transformer Text Encoder
Implements self-attention head pooling, byte-level positional embeddings,
and fine-tuned linear classification heads for fake job classification.
"""

import math
from typing import List, Tuple, Dict, Optional
from core.ml_inference.tensor_engine import Tensor, tensor_zeros, tensor_random_uniform, tensor_softmax
from core.ml_inference.neural_layers import DenseLayer, LayerNorm, MultiHeadAttentionLayer


class TransformerBlock:
    """Standard pre-LayerNorm Transformer Encoder block."""

    def __init__(self, embed_dim: int = 64, num_heads: int = 4, ffn_dim: int = 128):
        self.embed_dim = embed_dim
        self.ln1 = LayerNorm(embed_dim)
        self.attn = MultiHeadAttentionLayer(embed_dim, num_heads=num_heads)
        self.ln2 = LayerNorm(embed_dim)
        self.ffn1 = DenseLayer(embed_dim, ffn_dim, activation="relu")
        self.ffn2 = DenseLayer(ffn_dim, embed_dim, activation=None)

    def forward(self, x: Tensor) -> Tensor:
        # Residual + Attention
        norm1 = self.ln1.forward(x)
        attn_out = self.attn.forward(norm1)
        x = x.add(attn_out)

        # Residual + FFN
        norm2 = self.ln2.forward(x)
        ffn_out = self.ffn2.forward(self.ffn1.forward(norm2))
        return x.add(ffn_out)


class RoBERTaJobClassifier:
    """Full Transformer Encoder architecture for job scam detection."""

    def __init__(self, vocab_size: int = 5000, embed_dim: int = 64, num_layers: int = 3):
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        
        # Embedding tables (simulated)
        self.token_embeddings = tensor_random_uniform((vocab_size, embed_dim), low=-0.1, high=0.1)
        self.position_embeddings = tensor_random_uniform((512, embed_dim), low=-0.1, high=0.1)
        
        self.blocks = [TransformerBlock(embed_dim=embed_dim) for _ in range(num_layers)]
        self.pooler = DenseLayer(embed_dim, embed_dim, activation="relu")
        self.classifier_head = DenseLayer(embed_dim, 2, activation="softmax")  # [P(Safe), P(Scam)]

    def forward(self, token_ids: List[int]) -> Tensor:
        seq_len = min(len(token_ids), 512)
        if seq_len == 0:
            return Tensor([1.0, 0.0], shape=(1, 2))

        # Look up embeddings
        embed_data = []
        for pos in range(seq_len):
            t_id = min(token_ids[pos], self.vocab_size - 1)
            t_emb = self.token_embeddings.data[t_id * self.embed_dim:(t_id + 1) * self.embed_dim]
            p_emb = self.position_embeddings.data[pos * self.embed_dim:(pos + 1) * self.embed_dim]
            combined = [t + p for t, p in zip(t_emb, p_emb)]
            embed_data.extend(combined)

        x = Tensor(embed_data, shape=(seq_len, self.embed_dim))

        for block in self.blocks:
            x = block.forward(x)

        # Mean pooling over sequence
        pooled_data = [0.0] * self.embed_dim
        for i in range(seq_len):
            for j in range(self.embed_dim):
                pooled_data[j] += x.data[i * self.embed_dim + j]
        for j in range(self.embed_dim):
            pooled_data[j] /= seq_len

        pooled_tensor = Tensor(pooled_data, shape=(1, self.embed_dim))
        pooled_repr = self.pooler.forward(pooled_tensor)
        probabilities = self.classifier_head.forward(pooled_repr)
        return probabilities
