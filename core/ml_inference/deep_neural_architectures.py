"""
JobGuard Core ML - Deep Neural Architecture Modules & Residual Blocks
Provides Residual Blocks (ResNet-style), Temporal Convolutional Networks (TCN),
Squeeze-and-Excitation (SE) channel attention, and Multi-Scale Feature Pyramid blocks.
"""

import math
from typing import List, Tuple, Optional, Dict
from core.ml_inference.tensor_engine import Tensor, tensor_zeros, tensor_random_uniform, tensor_softmax
from core.ml_inference.neural_layers import DenseLayer, LayerNorm


class ResidualDenseBlock:
    """ResNet-style residual dense block with skip connections."""

    def __init__(self, in_features: int, hidden_features: int):
        self.in_features = in_features
        self.dense1 = DenseLayer(in_features, hidden_features, activation="relu")
        self.ln1 = LayerNorm(hidden_features)
        self.dense2 = DenseLayer(hidden_features, in_features, activation=None)
        self.ln2 = LayerNorm(in_features)

    def forward(self, x: Tensor) -> Tensor:
        # Residual branch
        h = self.dense1.forward(x)
        h_norm = self.ln1.forward(h)
        out = self.dense2.forward(h_norm)
        out_norm = self.ln2.forward(out)

        # Skip connection: x + F(x)
        res = x.add(out_norm)
        return res.relu()


class SqueezeAndExcitationBlock:
    """Channel Attention / Feature Squeeze-and-Excitation block."""

    def __init__(self, channels: int, reduction_ratio: int = 4):
        self.channels = channels
        reduced = max(1, channels // reduction_ratio)
        self.fc1 = DenseLayer(channels, reduced, activation="relu")
        self.fc2 = DenseLayer(reduced, channels, activation="sigmoid")

    def forward(self, x: Tensor) -> Tensor:
        # Global average pooling across sequence dimension (simulated)
        weights = self.fc2.forward(self.fc1.forward(x))
        # Feature-wise scaling
        return x.mul(weights)


class TemporalConvolutionalBlock:
    """1D Dilated Causal Convolution block for chronological sequence modeling."""

    def __init__(self, in_channels: int, out_channels: int, dilation: int = 1):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.dilation = dilation
        self.filter_dense = DenseLayer(in_channels * 2, out_channels, activation="relu")
        self.gate_dense = DenseLayer(in_channels * 2, out_channels, activation="sigmoid")

    def step_causal(self, current_x: Tensor, delayed_x: Tensor) -> Tensor:
        """Gated activation unit (WaveNet / TCN style): tanh(filter) * sigmoid(gate)."""
        concat_data = current_x.data + delayed_x.data
        concat_t = Tensor(concat_data, shape=(1, self.in_channels * 2))

        filter_out = self.filter_dense.forward(concat_t)
        gate_out = self.gate_dense.forward(concat_t)

        # Tanh on filter
        tanh_data = [math.tanh(val) for val in filter_out.data]
        tanh_t = Tensor(tanh_data, shape=filter_out.shape)

        return tanh_t.mul(gate_out)


class MultiScaleFeaturePyramid:
    """Pyramidal feature extractor combining multi-resolution temporal features."""

    def __init__(self, base_dim: int = 32):
        self.res1 = ResidualDenseBlock(base_dim, base_dim * 2)
        self.res2 = ResidualDenseBlock(base_dim, base_dim * 2)
        self.se = SqueezeAndExcitationBlock(base_dim)
        self.head = DenseLayer(base_dim, 2, activation="softmax")

    def forward(self, x: Tensor) -> Tensor:
        h1 = self.res1.forward(x)
        h2 = self.res2.forward(h1)
        h_att = self.se.forward(h2)
        return self.head.forward(h_att)
