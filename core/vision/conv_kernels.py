"""
Aetheris Computer Vision & Spatial: Tensor Convolutions & Feature Extractors
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import math
from typing import List, Tuple, Sequence, Optional


class Tensor2D:
    """2D Spatial Tensor / Matrix container."""
    __slots__ = ('height', 'width', 'data')

    def __init__(self, height: int, width: int, initial_value: float = 0.0) -> None:
        self.height = height
        self.width = width
        self.data = [[float(initial_value)] * width for _ in range(height)]

    @classmethod
    def from_nested(cls, nested: Sequence[Sequence[float]]) -> Tensor2D:
        h = len(nested)
        w = len(nested[0]) if h > 0 else 0
        t = cls(h, w)
        t.data = [[float(val) for val in row] for row in nested]
        return t

    def get(self, r: int, c: int) -> float:
        if 0 <= r < self.height and 0 <= c < self.width:
            return self.data[r][c]
        return 0.0 # Zero padding

    def set(self, r: int, c: int, val: float) -> None:
        if 0 <= r < self.height and 0 <= c < self.width:
            self.data[r][c] = float(val)


class SpatialConv2D:
    """2D Convolution and Spatial Filter engine implemented from first principles."""

    @staticmethod
    def convolve(input_tensor: Tensor2D, kernel: List[List[float]], stride: int = 1, padding: int = 1) -> Tensor2D:
        kh = len(kernel)
        kw = len(kernel[0])
        pad_h = kh // 2 if padding else 0
        pad_w = kw // 2 if padding else 0

        out_h = (input_tensor.height + 2 * pad_h - kh) // stride + 1
        out_w = (input_tensor.width + 2 * pad_w - kw) // stride + 1
        output = Tensor2D(out_h, out_w)

        for out_r in range(out_h):
            in_r = out_r * stride - pad_h
            for out_c in range(out_w):
                in_c = out_c * stride - pad_w
                acc = 0.0
                for kr in range(kh):
                    for kc in range(kw):
                        acc += input_tensor.get(in_r + kr, in_c + kc) * kernel[kr][kc]
                output.set(out_r, out_c, acc)

        return output

    @staticmethod
    def max_pool_2d(input_tensor: Tensor2D, pool_size: int = 2, stride: int = 2) -> Tensor2D:
        out_h = (input_tensor.height - pool_size) // stride + 1
        out_w = (input_tensor.width - pool_size) // stride + 1
        output = Tensor2D(out_h, out_w)

        for out_r in range(out_h):
            in_r = out_r * stride
            for out_c in range(out_w):
                in_c = out_c * stride
                max_val = -float('inf')
                for pr in range(pool_size):
                    for pc in range(pool_size):
                        val = input_tensor.get(in_r + pr, in_c + pc)
                        if val > max_val:
                            max_val = val
                output.set(out_r, out_c, max_val)

        return output

    @staticmethod
    def relu(tensor: Tensor2D) -> Tensor2D:
        out = Tensor2D(tensor.height, tensor.width)
        for r in range(tensor.height):
            for c in range(tensor.width):
                out.set(r, c, max(0.0, tensor.data[r][c]))
        return out

    @staticmethod
    def sobel_edge_detector(input_tensor: Tensor2D) -> Tensor2D:
        sobel_x = [
            [-1.0, 0.0, 1.0],
            [-2.0, 0.0, 2.0],
            [-1.0, 0.0, 1.0]
        ]
        sobel_y = [
            [-1.0, -2.0, -1.0],
            [ 0.0,  0.0,  0.0],
            [ 1.0,  2.0,  1.0]
        ]
        gx = SpatialConv2D.convolve(input_tensor, sobel_x, padding=1)
        gy = SpatialConv2D.convolve(input_tensor, sobel_y, padding=1)

        mag = Tensor2D(input_tensor.height, input_tensor.width)
        for r in range(input_tensor.height):
            for c in range(input_tensor.width):
                val_x = gx.data[r][c]
                val_y = gy.data[r][c]
                mag.set(r, c, math.sqrt(val_x * val_x + val_y * val_y))
        return mag
