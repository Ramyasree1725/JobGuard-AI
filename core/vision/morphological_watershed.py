"""
JobGuard Core Vision - Marker-Controlled Watershed Segmentation Algorithm
Implements morphological gradient extraction, distance transform, immersion simulation,
and dam construction for isolating overlapping stamped seals on documents.
"""

from typing import List, Tuple, Dict, Set


class MorphologicalWatershed:
    """Meyer's flooding watershed segmentation algorithm."""

    @staticmethod
    def distance_transform_chebyshev(binary_mask: List[List[int]]) -> List[List[int]]:
        """Computes Chebyshev distance transform of binary foreground mask."""
        h = len(binary_mask)
        w = len(binary_mask[0]) if h > 0 else 0
        dist = [[0 if binary_mask[y][x] == 0 else 9999 for x in range(w)] for y in range(h)]

        # Forward pass (top-left to bottom-right)
        for y in range(h):
            for x in range(w):
                if dist[y][x] > 0:
                    min_val = dist[y][x]
                    if y > 0:
                        min_val = min(min_val, dist[y - 1][x] + 1)
                        if x > 0:
                            min_val = min(min_val, dist[y - 1][x - 1] + 1)
                        if x < w - 1:
                            min_val = min(min_val, dist[y - 1][x + 1] + 1)
                    if x > 0:
                        min_val = min(min_val, dist[y][x - 1] + 1)
                    dist[y][x] = min_val

        # Backward pass (bottom-right to top-left)
        for y in range(h - 1, -1, -1):
            for x in range(w - 1, -1, -1):
                if dist[y][x] > 0:
                    min_val = dist[y][x]
                    if y < h - 1:
                        min_val = min(min_val, dist[y + 1][x] + 1)
                        if x > 0:
                            min_val = min(min_val, dist[y + 1][x - 1] + 1)
                        if x < w - 1:
                            min_val = min(min_val, dist[y + 1][x + 1] + 1)
                    if x < w - 1:
                        min_val = min(min_val, dist[y][x + 1] + 1)
                    dist[y][x] = min_val

        return dist
