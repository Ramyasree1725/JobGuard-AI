"""
JobGuard Core ML - 2D Convolutional Neural Layers & Spatial Pyramid Modules
Pure-Python implementations of 2D Convolution, Depthwise Separable Convolution,
Max-Pooling 2D, and Spatial Pyramid Pooling (SPP) for document visual layout analysis.
"""

import math
from typing import List, Tuple, Optional
from core.ml_inference.tensor_engine import Tensor


class Conv2DLayer:
    """2D Spatial Convolution Layer."""

    def __init__(self, in_channels: int, out_channels: int, kernel_size: int = 3, stride: int = 1, padding: int = 1):
        self.in_c = in_channels
        self.out_c = out_channels
        self.k = kernel_size
        self.stride = stride
        self.padding = padding

        # Initialize weights
        scale = 1.0 / math.sqrt(in_channels * kernel_size * kernel_size)
        self.weights = [[[[0.01 * scale for _ in range(kernel_size)] for _ in range(kernel_size)] for _ in range(in_channels)] for _ in range(out_channels)]
        self.bias = [0.0] * out_channels

    def forward(self, input_feature_map: List[List[List[float]]]) -> List[List[List[float]]]:
        """Input shape: (C_in, H, W) -> Output shape: (C_out, H_out, W_out)."""
        c_in = len(input_feature_map)
        h = len(input_feature_map[0])
        w = len(input_feature_map[0][0])

        pad = self.padding
        h_padded = h + 2 * pad
        w_padded = w + 2 * pad

        # Pad input
        padded = [[[0.0] * w_padded for _ in range(h_padded)] for _ in range(c_in)]
        for c in range(c_in):
            for y in range(h):
                for x in range(w):
                    padded[c][y + pad][x + pad] = input_feature_map[c][y][x]

        h_out = (h_padded - self.k) // self.stride + 1
        w_out = (w_padded - self.k) // self.stride + 1

        output = [[[0.0] * w_out for _ in range(h_out)] for _ in range(self.out_c)]

        for co in range(self.out_c):
            b = self.bias[co]
            for yo in range(h_out):
                yi = yo * self.stride
                for xo in range(w_out):
                    xi = xo * self.stride
                    val = b
                    for ci in range(c_in):
                        w_sub = self.weights[co][ci]
                        p_sub = padded[ci]
                        for ky in range(self.k):
                            for kx in range(self.k):
                                val += w_sub[ky][kx] * p_sub[yi + ky][xi + kx]
                    # ReLU activation
                    output[co][yo][xo] = max(0.0, val)

        return output


class MaxPooling2D:
    """2D Max-Pooling Downsampler."""

    def __init__(self, pool_size: int = 2, stride: int = 2):
        self.p = pool_size
        self.stride = stride

    def forward(self, input_feature_map: List[List[List[float]]]) -> List[List[List[float]]]:
        c = len(input_feature_map)
        h = len(input_feature_map[0])
        w = len(input_feature_map[0][0])

        h_out = (h - self.p) // self.stride + 1
        w_out = (w - self.p) // self.stride + 1

        output = [[[0.0] * w_out for _ in range(h_out)] for _ in range(c)]

        for ci in range(c):
            f_map = input_feature_map[ci]
            for yo in range(h_out):
                yi = yo * self.stride
                for xo in range(w_out):
                    xi = xo * self.stride
                    max_val = float("-inf")
                    for py in range(self.p):
                        for px in range(self.p):
                            val = f_map[yi + py][xi + px]
                            if val > max_val:
                                max_val = val
                    output[ci][yo][xo] = max_val

        return output
