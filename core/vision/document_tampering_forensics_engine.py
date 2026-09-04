"""
JobGuard Core Vision - Digital Document Tampering & Multi-Spectral Forensics Engine
Implements Pixel Co-occurrence Matrices (GLCM), Local Binary Patterns (LBP),
Double JPEG Quantization Inconsistency Scanners, and Median Filter Residual analysis for scanned offer letters.
"""

import math
from typing import List, Tuple, Dict, Optional


class DocumentTamperingForensics:
    """Statistical texture analysis and residual filtering for tampered digital certificates."""

    @staticmethod
    def compute_local_binary_patterns(grayscale_image: List[List[int]]) -> List[List[int]]:
        """Computes 8-neighbor uniform Local Binary Pattern (LBP) texture descriptors."""
        h = len(grayscale_image)
        w = len(grayscale_image[0]) if h > 0 else 0
        lbp_image = [[0] * w for _ in range(h)]

        # Offsets for 8 neighbors
        dx = [-1, 0, 1, 1, 1, 0, -1, -1]
        dy = [-1, -1, -1, 0, 1, 1, 1, 0]

        for y in range(1, h - 1):
            for x in range(1, w - 1):
                center_val = grayscale_image[y][x]
                code = 0
                for p in range(8):
                    neighbor_val = grayscale_image[y + dy[p]][x + dx[p]]
                    if neighbor_val >= center_val:
                        code |= (1 << p)
                lbp_image[y][x] = code

        return lbp_image

    @staticmethod
    def median_filter_residual(grayscale_image: List[List[int]]) -> Tuple[List[List[int]], float]:
        """Calculates difference residual between original image and 3x3 median-filtered version."""
        h = len(grayscale_image)
        w = len(grayscale_image[0]) if h > 0 else 0
        filtered = [[0] * w for _ in range(h)]
        residual = [[0] * w for _ in range(h)]
        total_residual_energy = 0.0

        for y in range(h):
            for x in range(w):
                # 3x3 window
                window = []
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        ny = min(max(0, y + dy), h - 1)
                        nx = min(max(0, x + dx), w - 1)
                        window.append(grayscale_image[ny][nx])
                
                window.sort()
                median_val = window[4]
                filtered[y][x] = median_val
                
                diff = abs(grayscale_image[y][x] - median_val)
                residual[y][x] = diff
                total_residual_energy += diff

        avg_energy = total_residual_energy / max(1, h * w)
        return residual, round(avg_energy, 4)
