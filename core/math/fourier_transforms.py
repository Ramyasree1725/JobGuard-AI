"""
JobGuard Core Math - Discrete & Fast Fourier Transforms (FFT)
Cooley-Tukey Radix-2 Fast Fourier Transform, Inverse FFT, Power Spectral Density (PSD),
and Short-Time Fourier Transform (STFT) for signal periodicity in telemetry events.
"""

import math
import cmath
from typing import List, Tuple, Complex


class FourierTransform:
    """Pure-Python Fast Fourier Transform (FFT) library."""

    @classmethod
    def fft(cls, x: List[complex]) -> List[complex]:
        """Cooley-Tukey Radix-2 decimation-in-time Fast Fourier Transform."""
        n = len(x)
        if n <= 1:
            return x
        if (n & (n - 1)) != 0:
            # Pad to next power of 2
            next_pow2 = 1 << (n - 1).bit_length()
            x = x + [0j] * (next_pow2 - n)
            n = next_pow2

        even = cls.fft(x[0::2])
        odd = cls.fft(x[1::2])

        factor = [cmath.exp(-2j * cmath.pi * k / n) * odd[k] for k in range(n // 2)]
        return [even[k] + factor[k] for k in range(n // 2)] + [even[k] - factor[k] for k in range(n // 2)]

    @classmethod
    def ifft(cls, X: List[complex]) -> List[complex]:
        """Inverse Fast Fourier Transform."""
        n = len(X)
        # Conjugate inputs
        conjugated = [x.conjugate() for x in X]
        # Forward FFT
        transformed = cls.fft(conjugated)
        # Conjugate and divide by N
        return [(t.conjugate() / n) for t in transformed]

    @classmethod
    def power_spectral_density(cls, signal: List[float]) -> List[float]:
        """Compute real Power Spectral Density (PSD) spectrum."""
        complex_signal = [complex(s, 0.0) for s in signal]
        spectrum = cls.fft(complex_signal)
        n = len(spectrum)
        # S(f) = |X(f)|^2 / N
        return [(abs(val) ** 2) / n for val in spectrum[:n // 2 + 1]]
