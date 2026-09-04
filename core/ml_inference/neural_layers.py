"""
JobGuard Core ML - Neural Network Layers & Architecture Blocks
Fully vectorized implementations of Linear/Dense, LayerNorm, MultiHeadAttention,
and Recurrent Gated Units (GRU) for text classification and scam scoring.
"""

import math
from typing import List, Optional, Tuple, Dict, Any
from .tensor_engine import Tensor, tensor_zeros, tensor_random_uniform, tensor_softmax, tensor_matmul


class Layer:
    """Base neural network layer abstract interface."""
    def forward(self, input_tensor: Tensor) -> Tensor:
        raise NotImplementedError

    def get_weights(self) -> Dict[str, Tensor]:
        return {}


class DenseLayer(Layer):
    """Fully-connected Dense Layer with bias and optional activation."""

    def __init__(self, in_features: int, out_features: int, activation: Optional[str] = "relu"):
        self.in_features = in_features
        self.out_features = out_features
        self.activation = activation
        
        # Xavier/He initialization
        scale = math.sqrt(2.0 / in_features)
        self.weights = tensor_random_uniform((in_features, out_features), low=-scale, high=scale)
        self.bias = tensor_zeros((1, out_features))

    def forward(self, x: Tensor) -> Tensor:
        # x is (Batch, in_features)
        if len(x.shape) == 1:
            x = x.reshape((1, len(x.data)))
            
        out = x.matmul_2d(self.weights)
        
        # Broadcast bias across batch dimension
        batch_size = out.shape[0]
        bias_tiled_data = self.bias.data * batch_size
        out = out.add(Tensor(bias_tiled_data, shape=out.shape))

        if self.activation == "relu":
            return out.relu()
        elif self.activation == "sigmoid":
            return out.sigmoid()
        elif self.activation == "softmax":
            return tensor_softmax(out)
        return out

    def get_weights(self) -> Dict[str, Tensor]:
        return {"weights": self.weights, "bias": self.bias}


class LayerNorm(Layer):
    """Layer Normalization over feature dimension."""

    def __init__(self, features: int, eps: float = 1e-5):
        self.features = features
        self.eps = eps
        self.gamma = Tensor([1.0] * features, shape=(1, features))
        self.beta = Tensor([0.0] * features, shape=(1, features))

    def forward(self, x: Tensor) -> Tensor:
        if len(x.shape) != 2:
            raise ValueError("LayerNorm currently expects 2D tensor (Batch, Features)")
        
        batch_size, num_feats = x.shape
        out_data = [0.0] * (batch_size * num_feats)

        for i in range(batch_size):
            row = x.data[i * num_feats:(i + 1) * num_feats]
            mean = sum(row) / num_feats
            var = sum((val - mean) ** 2 for val in row) / num_feats
            std = math.sqrt(var + self.eps)

            for j in range(num_feats):
                norm_val = (row[j] - mean) / std
                scaled = norm_val * self.gamma.data[j] + self.beta.data[j]
                out_data[i * num_feats + j] = scaled

        return Tensor(out_data, shape=(batch_size, num_feats))


class MultiHeadAttentionLayer(Layer):
    """Simplified Multi-Head Self Attention layer."""

    def __init__(self, embed_dim: int, num_heads: int = 4):
        if embed_dim % num_heads != 0:
            raise ValueError("embed_dim must be divisible by num_heads")
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads

        self.w_q = DenseLayer(embed_dim, embed_dim, activation=None)
        self.w_k = DenseLayer(embed_dim, embed_dim, activation=None)
        self.w_v = DenseLayer(embed_dim, embed_dim, activation=None)
        self.out_proj = DenseLayer(embed_dim, embed_dim, activation=None)

    def forward(self, x: Tensor) -> Tensor:
        # x shape: (seq_len, embed_dim)
        q = self.w_q.forward(x)
        k = self.w_k.forward(x)
        v = self.w_v.forward(x)

        # Scaled dot-product attention
        # Scores = (Q @ K.T) / sqrt(d_k)
        scores = q.matmul_2d(k.transpose_2d())
        scale = 1.0 / math.sqrt(self.head_dim)
        scores = scores.mul(scale)

        attn_weights = tensor_softmax(scores)
        context = attn_weights.matmul_2d(v)
        
        return self.out_proj.forward(context)


class GRULayer(Layer):
    """Gated Recurrent Unit (GRU) cell for sequential text analysis."""

    def __init__(self, input_dim: int, hidden_dim: int):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim

        # Combined gate weights for update (z) and reset (r) gates
        self.w_z = DenseLayer(input_dim + hidden_dim, hidden_dim, activation="sigmoid")
        self.w_r = DenseLayer(input_dim + hidden_dim, hidden_dim, activation="sigmoid")
        self.w_h = DenseLayer(input_dim + hidden_dim, hidden_dim, activation=None)

    def step(self, x_t: Tensor, h_prev: Tensor) -> Tensor:
        # Concatenate x_t and h_prev
        concat_data = x_t.data + h_prev.data
        concat_t = Tensor(concat_data, shape=(1, self.input_dim + self.hidden_dim))

        z_t = self.w_z.forward(concat_t)
        r_t = self.w_r.forward(concat_t)

        # Reset hidden state candidate
        r_h_data = [r * h for r, h in zip(r_t.data, h_prev.data)]
        concat_cand_data = x_t.data + r_h_data
        concat_cand_t = Tensor(concat_cand_data, shape=(1, self.input_dim + self.hidden_dim))
        
        h_cand_raw = self.w_h.forward(concat_cand_t)
        # Tanh activation
        h_cand_data = [math.tanh(val) for val in h_cand_raw.data]

        # New hidden state: (1 - z) * h_prev + z * h_cand
        h_new_data = [(1.0 - z) * h + z * c for z, h, c in zip(z_t.data, h_prev.data, h_cand_data)]
        return Tensor(h_new_data, shape=(1, self.hidden_dim))


class SequentialModel:
    """Container for executing a sequential chain of neural layers."""

    def __init__(self, layers: Optional[List[Layer]] = None):
        self.layers = list(layers or [])

    def add(self, layer: Layer) -> "SequentialModel":
        self.layers.append(layer)
        return self

    def forward(self, x: Tensor) -> Tensor:
        curr = x
        for layer in self.layers:
            curr = layer.forward(curr)
        return curr
