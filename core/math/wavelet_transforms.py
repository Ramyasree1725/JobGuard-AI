"""
JobGuard Core Math - Discrete Wavelet Transform (DWT) & Multiresolution Analysis
Implements 1D/2D Haar and Daubechies (DB4) Wavelet Transforms for multi-scale signal decomposition.
"""

import math
from typing import List, Tuple


class WaveletTransform:
    """Discrete Wavelet Transform algorithms."""

    # Daubechies 4-tap filter coefficients
    DB4_H0 = (1.0 + math.sqrt(3.0)) / (4.0 * math.sqrt(2.0))
    DB4_H1 = (3.0 + math.sqrt(3.0)) / (4.0 * math.sqrt(2.0))
    DB4_H2 = (3.0 - math.sqrt(3.0)) / (4.0 * math.sqrt(2.0))
    DB4_H3 = (1.0 - math.sqrt(3.0)) / (4.0 * math.sqrt(2.0))

    # Quadrature mirror filter (high-pass)
    DB4_G0 = DB4_H3
    DB4_G1 = -DB4_H2
    DB4_G2 = DB4_H1
    DB4_G3 = -DB4_H0

    @classmethod
    def haar_1d_forward(cls, signal: List[float]) -> Tuple[List[float], List[float]]:
        """1-level 1D Haar Wavelet Transform returning (approximation_cA, detail_cD)."""
        n = len(signal)
        if n % 2 != 0:
            signal = signal + [0.0]
            n += 1

        half = n // 2
        cA = [0.0] * half
        cD = [0.0] * half
        sqrt2 = math.sqrt(2.0)

        for i in range(half):
            cA[i] = (signal[2 * i] + signal[2 * i + 1]) / sqrt2
            cD[i] = (signal[2 * i] - signal[2 * i + 1]) / sqrt2

        return cA, cD

    @classmethod
    def haar_1d_inverse(cls, cA: List[float], cD: List[float]) -> List[float]:
        """Inverse 1D Haar Wavelet Transform."""
        half = len(cA)
        signal = [0.0] * (2 * half)
        sqrt2 = math.sqrt(2.0)

        for i in range(half):
            signal[2 * i] = (cA[i] + cD[i]) / sqrt2
            signal[2 * i + 1] = (cA[i] - cD[i]) / sqrt2

        return signal

    @classmethod
    def db4_1d_forward(cls, signal: List[float]) -> Tuple[List[float], List[float]]:
        """1-level 1D Daubechies-4 Wavelet Transform."""
        n = len(signal)
        if n % 2 != 0:
            signal = signal + [0.0]
            n += 1

        half = n // 2
        cA = [0.0] * half
        cD = [0.0] * half

        h = [cls.DB4_H0, cls.DB4_H1, cls.DB4_H2, cls.DB4_H3]
        g = [cls.DB4_G0, cls.DB4_G1, cls.DB4_G2, cls.DB4_G3]

        for i in range(half):
            sum_a = 0.0
            sum_d = 0.0
            for k in range(4):
                idx = (2 * i + k) % n
                sum_a += h[k] * signal[idx]
                sum_d += g[k] * signal[idx]
            cA[i] = sum_a
            cD[i] = sum_d

        return cA, cD
