"""
JobGuard Core ML - Dynamic & Static Quantization Engine
Compresses FP32 weight tensors to 8-bit integers (INT8) and FP16 approximations
for low-latency CPU inference pipelines.
"""

import enum
import struct
import math
from typing import List, Tuple, Dict, Any, Optional
from .tensor_engine import Tensor


class QuantizationScheme(enum.Enum):
    AFFINE_ASYMMETRIC = "AFFINE_ASYMMETRIC"
    SYMMETRIC = "SYMMETRIC"
    FP16_EMULATED = "FP16_EMULATED"


class QuantizedTensor:
    """Represents an INT8 quantized tensor with scale and zero-point calibration parameters."""

    def __init__(self, int8_data: List[int], shape: Tuple[int, ...], scale: float, zero_point: int):
        self.int8_data = int8_data
        self.shape = shape
        self.scale = scale
        self.zero_point = zero_point

    def dequantize(self) -> Tensor:
        """Reconstruct approximate FP32 floating point tensor."""
        fp32_data = [float((q - self.zero_point) * self.scale) for q in self.int8_data]
        return Tensor(fp32_data, shape=self.shape)

    def memory_footprint_bytes(self) -> int:
        return len(self.int8_data) + 16  # 1 byte per int8 element + header metadata


class DynamicQuantizer:
    """Dynamic INT8 Quantizer for weight matrices and activations."""

    @staticmethod
    def quantize_tensor(t: Tensor, scheme: QuantizationScheme = QuantizationScheme.AFFINE_ASYMMETRIC) -> QuantizedTensor:
        """Convert float Tensor to QuantizedTensor."""
        if not t.data:
            return QuantizedTensor([], t.shape, scale=1.0, zero_point=0)

        min_val = min(t.data)
        max_val = max(t.data)

        if scheme == QuantizationScheme.SYMMETRIC:
            abs_max = max(abs(min_val), abs(max_val), 1e-8)
            scale = abs_max / 127.0
            zero_point = 0
            int8_data = [max(-128, min(127, round(val / scale))) for val in t.data]
        else:
            # Asymmetric quantization: maps [min_val, max_val] -> [0, 255] or [-128, 127]
            val_range = max(max_val - min_val, 1e-8)
            scale = val_range / 255.0
            zero_point = round(-min_val / scale) - 128
            zero_point = max(-128, min(127, zero_point))
            
            int8_data = [max(-128, min(127, round(val / scale) + zero_point)) for val in t.data]

        return QuantizedTensor(int8_data, t.shape, scale=scale, zero_point=zero_point)

    @staticmethod
    def compute_quantization_error(original: Tensor, quantized: QuantizedTensor) -> Dict[str, float]:
        """Measure mean squared error (MSE) and Signal-to-Quantization-Noise Ratio (SQNR)."""
        reconstructed = quantized.dequantize()
        mse = sum((o - r) ** 2 for o, r in zip(original.data, reconstructed.data)) / len(original.data)
        signal_power = sum(o ** 2 for o in original.data) / len(original.data)
        
        sqnr_db = 10.0 * math.log10(max(1e-12, signal_power / max(1e-12, mse)))
        compression_ratio = (len(original.data) * 4.0) / quantized.memory_footprint_bytes()

        return {
            "mse": round(mse, 6),
            "sqnr_db": round(sqnr_db, 2),
            "compression_ratio": round(compression_ratio, 2)
        }
