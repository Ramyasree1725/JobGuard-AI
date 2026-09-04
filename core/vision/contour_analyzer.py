"""
JobGuard Core Vision - Border Following & Contour Topology Analysis
Suzuki-Abe border following algorithm for extracting nested contours from document masks.
"""

from typing import List, Tuple, Dict, Set


class ContourAnalyzer:
    """Extracts connected component contours and geometric properties."""

    @staticmethod
    def polygon_area(points: List[Tuple[float, float]]) -> float:
        """Shoelace formula for polygon area."""
        n = len(points)
        if n < 3:
            return 0.0
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += points[i][0] * points[j][1]
            area -= points[j][0] * points[i][1]
        return abs(area) / 2.0

    @staticmethod
    def polygon_perimeter(points: List[Tuple[float, float]]) -> float:
        """Computes Euclidean perimeter."""
        n = len(points)
        if n < 2:
            return 0.0
        perim = 0.0
        for i in range(n):
            j = (i + 1) % n
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            perim += (dx ** 2 + dy ** 2) ** 0.5
        return perim
