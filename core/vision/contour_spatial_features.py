"""
JobGuard Core Vision - Hu Moments & Invariant Shape Descriptors
Calculates 7 translation, scale, and rotation invariant Hu Moments
from raw spatial central moments for verifying corporate seal geometry.
"""

import math
from typing import List, Tuple, Dict


class HuMomentsExtractor:
    """Computes 7 invariant Hu Moments from binary image masks."""

    @staticmethod
    def calculate_hu_moments(binary_image: List[List[int]]) -> List[float]:
        h = len(binary_image)
        w = len(binary_image[0]) if h > 0 else 0

        # Raw spatial moments m_pq
        m00 = sum(sum(row) for row in binary_image)
        if m00 == 0:
            return [0.0] * 7

        m10 = sum(x * binary_image[y][x] for y in range(h) for x in range(w))
        m01 = sum(y * binary_image[y][x] for y in range(h) for x in range(w))

        # Centroid
        x_bar = m10 / m00
        y_bar = m01 / m00

        # Central moments mu_pq
        def mu(p: int, q: int) -> float:
            val = 0.0
            for y in range(h):
                for x in range(w):
                    if binary_image[y][x] > 0:
                        val += ((x - x_bar) ** p) * ((y - y_bar) ** q)
            return val

        mu20 = mu(2, 0)
        mu02 = mu(0, 2)
        mu11 = mu(1, 1)
        mu30 = mu(3, 0)
        mu03 = mu(0, 3)
        mu21 = mu(2, 1)
        mu12 = mu(1, 2)

        # Normalized central moments eta_pq = mu_pq / mu00^(1 + (p+q)/2)
        def eta(p: int, q: int, m_val: float) -> float:
            return m_val / (m00 ** (1.0 + (p + q) / 2.0))

        e20, e02, e11 = eta(2, 0, mu20), eta(0, 2, mu02), eta(1, 1, mu11)
        e30, e03, e21, e12 = eta(3, 0, mu30), eta(0, 3, mu03), eta(2, 1, mu21), eta(1, 2, mu12)

        # 7 Hu Invariants
        h1 = e20 + e02
        h2 = (e20 - e02) ** 2 + 4.0 * (e11 ** 2)
        h3 = (e30 - 3.0 * e12) ** 2 + (3.0 * e21 - e03) ** 2
        h4 = (e30 + e12) ** 2 + (e21 + e03) ** 2
        h5 = (e30 - 3.0 * e12) * (e30 + e12) * ((e30 + e12) ** 2 - 3.0 * (e21 + e03) ** 2) + \
             (3.0 * e21 - e03) * (e21 + e03) * (3.0 * (e30 + e12) ** 2 - (e21 + e03) ** 2)
        h6 = (e20 - e02) * ((e30 + e12) ** 2 - (e21 + e03) ** 2) + 4.0 * e11 * (e30 + e12) * (e21 + e03)
        h7 = (3.0 * e21 - e03) * (e30 + e12) * ((e30 + e12) ** 2 - 3.0 * (e21 + e03) ** 2) - \
             (e30 - 3.0 * e12) * (e21 + e03) * (3.0 * (e30 + e12) ** 2 - (e21 + e03) ** 2)

        # Log transform for scale readability
        moments = [h1, h2, h3, h4, h5, h6, h7]
        log_moments = []
        for m in moments:
            if abs(m) > 1e-15:
                sign = 1.0 if m >= 0 else -1.0
                log_moments.append(round(-sign * math.log10(abs(m)), 4))
            else:
                log_moments.append(0.0)

        return log_moments
