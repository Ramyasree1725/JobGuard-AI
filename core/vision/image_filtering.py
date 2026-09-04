"""
JobGuard Core Vision - 2D Image Filtering & Spatial Convolutions
Implements Gaussian blur, median denoising, Bilateral filtering,
and unsharp masking for preprocessing scanned offer letters and ID proofs.
"""

import math
from typing import List, Tuple, Optional


class ImageFilter:
    """Pure-Python spatial image filtering matrix operations."""

    @staticmethod
    def convolve2d(image: List[List[float]], kernel: List[List[float]]) -> List[List[float]]:
        h = len(image)
        w = len(image[0]) if h > 0 else 0
        kh = len(kernel)
        kw = len(kernel[0]) if kh > 0 else 0
        pad_h = kh // 2
        pad_w = kw // 2

        output = [[0.0] * w for _ in range(h)]

        for y in range(h):
            for x in range(w):
                val = 0.0
                for ky in range(kh):
                    for kx in range(kw):
                        iy = min(max(0, y + ky - pad_h), h - 1)
                        ix = min(max(0, x + kx - pad_w), w - 1)
                        val += image[iy][ix] * kernel[ky][kx]
                output[y][x] = val

        return output

    @classmethod
    def gaussian_blur(cls, image: List[List[float]], sigma: float = 1.0) -> List[List[float]]:
        size = int(math.ceil(sigma * 3)) * 2 + 1
        half = size // 2
        kernel = [[0.0] * size for _ in range(size)]
        sum_k = 0.0

        for y in range(-half, half + 1):
            for x in range(-half, half + 1):
                g = (1.0 / (2.0 * math.pi * sigma ** 2)) * math.exp(-(x ** 2 + y ** 2) / (2.0 * sigma ** 2))
                kernel[y + half][x + half] = g
                sum_k += g

        # Normalize kernel
        for y in range(size):
            for x in range(size):
                kernel[y][x] /= sum_k

        return cls.convolve2d(image, kernel)
