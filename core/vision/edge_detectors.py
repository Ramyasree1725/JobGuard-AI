"""
JobGuard Core Vision - Sobel, Scharr, and Canny Edge Detection
Extracts document boundaries, watermark boundaries, and seal contours.
"""

import math
from typing import List, Tuple
from .image_filtering import ImageFilter


class EdgeDetector:
    """Sobel and Canny edge gradient extraction routines."""

    SOBEL_X = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    SOBEL_Y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    @classmethod
    def sobel_gradients(cls, image: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
        """Compute gradient magnitude and orientation angle matrices."""
        gx = ImageFilter.convolve2d(image, cls.SOBEL_X)
        gy = ImageFilter.convolve2d(image, cls.SOBEL_Y)
        h = len(image)
        w = len(image[0]) if h > 0 else 0

        magnitude = [[0.0] * w for _ in range(h)]
        orientation = [[0.0] * w for _ in range(h)]

        for y in range(h):
            for x in range(w):
                mag = math.sqrt(gx[y][x] ** 2 + gy[y][x] ** 2)
                angle = math.atan2(gy[y][x], gx[y][x])
                magnitude[y][x] = mag
                orientation[y][x] = angle

        return magnitude, orientation
