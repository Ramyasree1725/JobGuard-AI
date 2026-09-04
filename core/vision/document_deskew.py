"""
JobGuard Core Vision - Hough Line Transform & Document Deskewing
Detects rotational skew angles in scanned offer letter PDFs and rotates documents to 0 degrees.
"""

import math
from typing import List, Tuple, Dict, Optional


class DocumentDeskewer:
    """Standard Hough Transform for detecting dominant text line orientation."""

    @staticmethod
    def detect_skew_angle(binary_image: List[List[int]], angle_range_deg: float = 15.0, angle_step_deg: float = 0.5) -> float:
        """Find the dominant skew angle using Radon/Hough projection variance."""
        h = len(binary_image)
        w = len(binary_image[0]) if h > 0 else 0

        best_angle = 0.0
        max_variance = -1.0

        angle = -angle_range_deg
        while angle <= angle_range_deg:
            rad = math.radians(angle)
            cos_a = math.cos(rad)
            sin_a = math.sin(rad)

            # Horizontal projection profile
            profile = [0] * h
            for y in range(h):
                for x in range(w):
                    if binary_image[y][x] > 0:
                        proj_y = int(y * cos_a - x * sin_a)
                        if 0 <= proj_y < h:
                            profile[proj_y] += 1

            # Variance of profile
            mean_p = sum(profile) / h
            var = sum((p - mean_p) ** 2 for p in profile) / h

            if var > max_variance:
                max_variance = var
                best_angle = angle

            angle += angle_step_deg

        return round(best_angle, 2)
