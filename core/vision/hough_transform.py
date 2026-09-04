"""
JobGuard Core Vision - Hough Circle & Line Accumulator
Extracts round seal stamps and signatures from employment documents.
"""

import math
from typing import List, Tuple, Dict


class HoughCircleTransform:
    """Standard Hough Gradient method for circular seal detection."""

    @staticmethod
    def detect_circles(
        edge_image: List[List[int]],
        min_radius: int = 10,
        max_radius: int = 50,
        threshold: int = 15
    ) -> List[Tuple[int, int, int]]:
        """Accumulator voting in parameter space (a, b, r). Returns list of (x, y, radius)."""
        h = len(edge_image)
        w = len(edge_image[0]) if h > 0 else 0
        detected = []

        # Subsampled voting grid
        for r in range(min_radius, max_radius, 5):
            accumulator: Dict[Tuple[int, int], int] = {}
            for y in range(h):
                for x in range(w):
                    if edge_image[y][x] > 0:
                        for theta_deg in range(0, 360, 15):
                            rad = math.radians(theta_deg)
                            a = int(x - r * math.cos(rad))
                            b = int(y - r * math.sin(rad))
                            if 0 <= a < w and 0 <= b < h:
                                accumulator[(a, b)] = accumulator.get((a, b), 0) + 1

            for (a, b), votes in accumulator.items():
                if votes >= threshold:
                    detected.append((a, b, r))

        return detected
