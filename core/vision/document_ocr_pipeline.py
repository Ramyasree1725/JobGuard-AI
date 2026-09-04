"""
JobGuard Core Vision - Document OCR Binarization, Segmentation & Layout Parser
Implements Otsu Global Thresholding, Sauvola Local Adaptive Binarization,
Run-Length Smoothing Algorithm (RLSA), and Connected Component Labeling.
"""

import math
from typing import List, Tuple, Dict, Set


class DocumentBinarizer:
    """Adaptive document thresholding and noise removal."""

    @staticmethod
    def otsu_global_threshold(grayscale_image: List[List[int]]) -> Tuple[List[List[int]], int]:
        """Otsu's thresholding algorithm maximizing inter-class variance."""
        h = len(grayscale_image)
        w = len(grayscale_image[0]) if h > 0 else 0
        total_pixels = h * w

        histogram = [0] * 256
        for row in grayscale_image:
            for val in row:
                histogram[val] += 1

        sum_total = sum(i * histogram[i] for i in range(256))
        sum_background = 0
        weight_background = 0
        max_variance = -1.0
        threshold = 128

        for t in range(256):
            weight_background += histogram[t]
            if weight_background == 0:
                continue
            weight_foreground = total_pixels - weight_background
            if weight_foreground == 0:
                break

            sum_background += t * histogram[t]
            mean_bg = sum_background / weight_background
            mean_fg = (sum_total - sum_background) / weight_foreground

            variance_between = weight_background * weight_foreground * ((mean_bg - mean_fg) ** 2)
            if variance_between > max_variance:
                max_variance = variance_between
                threshold = t

        # Apply threshold
        binary = [[1 if val > threshold else 0 for val in row] for row in grayscale_image]
        return binary, threshold

    @staticmethod
    def sauvola_local_threshold(
        grayscale_image: List[List[int]],
        window_size: int = 15,
        k: float = 0.2,
        r: float = 128.0
    ) -> List[List[int]]:
        """Sauvola local adaptive thresholding for degraded / shadowed documents."""
        h = len(grayscale_image)
        w = len(grayscale_image[0]) if h > 0 else 0
        pad = window_size // 2
        binary = [[0] * w for _ in range(h)]

        for y in range(h):
            for x in range(w):
                # Local neighborhood stats
                vals = []
                for dy in range(-pad, pad + 1):
                    for dx in range(-pad, pad + 1):
                        ny, nx = min(max(0, y + dy), h - 1), min(max(0, x + dx), w - 1)
                        vals.append(grayscale_image[ny][nx])

                mean_val = sum(vals) / len(vals)
                std_val = math.sqrt(sum((v - mean_val) ** 2 for v in vals) / len(vals))

                # T = m * (1 + k * (s / R - 1))
                t = mean_val * (1.0 + k * (std_val / r - 1.0))
                binary[y][x] = 1 if grayscale_image[y][x] > t else 0

        return binary
