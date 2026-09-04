"""
JobGuard Core ML Inference Engine
Pure-Python, zero-external-dependency tensor math, neural layer primitives,
quantization, feature vectorization, and probability calibration.
"""

from .tensor_engine import Tensor, tensor_zeros, tensor_ones, tensor_matmul, tensor_softmax
from .neural_layers import DenseLayer, LayerNorm, MultiHeadAttentionLayer, GRULayer, SequentialModel
from .quantization import DynamicQuantizer, QuantizedTensor, QuantizationScheme
from .feature_encoder import TFIDFVectorizer, TextFeatureExtractor, ScalerNormalizer
from .calibration_layers import TemperatureScaling, PlattScaling, IsotonicCalibrator

__all__ = [
    "Tensor",
    "tensor_zeros",
    "tensor_ones",
    "tensor_matmul",
    "tensor_softmax",
    "DenseLayer",
    "LayerNorm",
    "MultiHeadAttentionLayer",
    "GRULayer",
    "SequentialModel",
    "DynamicQuantizer",
    "QuantizedTensor",
    "QuantizationScheme",
    "TFIDFVectorizer",
    "TextFeatureExtractor",
    "ScalerNormalizer",
    "TemperatureScaling",
    "PlattScaling",
    "IsotonicCalibrator",
]
