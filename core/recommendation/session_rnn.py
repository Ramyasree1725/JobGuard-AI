"""
JobGuard Core Recommendation - GRU4Rec Session-Based Candidate Trajectory Engine
Predicts next verified career recommendations based on short-term browsing sequences.
"""

from typing import List, Dict, Tuple, Optional
from core.ml_inference.tensor_engine import Tensor
from core.ml_inference.neural_layers import GRULayer, DenseLayer


class SessionRNNRecommender:
    """Recurrent sequence predictor for sequential job interactions."""

    def __init__(self, item_count: int = 100, embed_dim: int = 16, hidden_dim: int = 32):
        self.item_count = item_count
        self.embed_dim = embed_dim
        self.hidden_dim = hidden_dim
        self.gru = GRULayer(embed_dim, hidden_dim)
        self.output_proj = DenseLayer(hidden_dim, item_count, activation="softmax")

    def predict_next_items(self, item_sequence: List[int]) -> List[Tuple[int, float]]:
        """Return top recommended item IDs and predicted probabilities."""
        h = Tensor([0.0] * self.hidden_dim, shape=(1, self.hidden_dim))
        
        for item_id in item_sequence:
            # One-hot / dense embedding lookup simulation
            x = Tensor([1.0 if i == (item_id % self.embed_dim) else 0.0 for i in range(self.embed_dim)], shape=(1, self.embed_dim))
            h = self.gru.step(x, h)

        logits = self.output_proj.forward(h)
        probs = [(idx, round(prob, 4)) for idx, prob in enumerate(logits.data)]
        probs.sort(key=lambda x: x[1], reverse=True)
        return probs[:5]
