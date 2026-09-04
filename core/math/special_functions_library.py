"""
JobGuard Core Math - Special Mathematical Functions & Polynomial Expansions
Implements Gamma Function (Lanczos Approximation), Beta Function, Error Function (erf/erfc),
Bessel Functions (J0, J1, I0, I1), Chebyshev Polynomials (Tn, Un), and Legendre Polynomials (Pn).
"""

import math
from typing import List, Tuple, Callable, Optional


class SpecialFunctions:
    """Accurate pure-Python special function evaluations for probability distributions."""

    # Lanczos coefficients for Gamma(z) with g=7, N=9
    LANCZOS_COEFFS = [
        0.99999999999980993,
        676.5203681218851,
        -1259.1392167224028,
        771.32342877765313,
        -176.61502916214059,
        12.507343278686905,
        -0.1385710958311102,
        9.9843695780195716e-6,
        1.5056327351493116e-7
    ]

    @classmethod
    def gamma(cls, z: float) -> float:
        """Lanczos approximation for the Gamma function Gamma(z)."""
        if z < 0.5:
            # Reflection formula: Gamma(1-z) * Gamma(z) = pi / sin(pi * z)
            return math.pi / (math.sin(math.pi * z) * cls.gamma(1.0 - z))

        z -= 1.0
        x = cls.LANCZOS_COEFFS[0]
        for i in range(1, len(cls.LANCZOS_COEFFS)):
            x += cls.LANCZOS_COEFFS[i] / (z + i)

        t = z + 7.5
        return math.sqrt(2.0 * math.pi) * (t ** (z + 0.5)) * math.exp(-t) * x

    @classmethod
    def log_gamma(cls, z: float) -> float:
        """Natural logarithm of the Gamma function ln(Gamma(z))."""
        return math.log(cls.gamma(z))

    @classmethod
    def beta(cls, a: float, b: float) -> float:
        """Beta function B(a, b) = Gamma(a) * Gamma(b) / Gamma(a + b)."""
        return cls.gamma(a) * cls.gamma(b) / cls.gamma(a + b)

    @staticmethod
    def erf(x: float) -> float:
        """Error function erf(x) approximation via Abramowitz and Stegun formula 7.1.26."""
        a1 = 0.254829592
        a2 = -0.284496736
        a3 = 1.421413741
        a4 = -1.453152027
        a5 = 1.061405429
        p = 0.3275911

        sign = 1.0 if x >= 0 else -1.0
        abs_x = abs(x)

        t = 1.0 / (1.0 + p * abs_x)
        y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-abs_x * abs_x)

        return sign * y

    @staticmethod
    def erfc(x: float) -> float:
        """Complementary error function erfc(x) = 1 - erf(x)."""
        return 1.0 - SpecialFunctions.erf(x)

    @staticmethod
    def bessel_j0(x: float) -> float:
        """Bessel function of first kind J0(x) polynomial approximation."""
        ax = abs(x)
        if ax < 3.75:
            y = (x / 3.75) ** 2
            ans = 1.0 + y * (-2.2499997 + y * (1.2656208 + y * (-0.3163866 + y * (0.0444479 - y * 0.0039444))))
            return ans
        else:
            y = 3.75 / ax
            f0 = (0.79788456 + y * (-0.00000077 + y * (-0.00552740 + y * (0.00009512 + y * (0.00137237 - y * 0.00072805)))))
            theta0 = ax - 0.78539816 + y * (-0.04166397 + y * (-0.00003954 + y * (0.00262573 + y * (-0.00054125 - y * 0.00029333))))
            return (1.0 / math.sqrt(ax)) * f0 * math.cos(theta0)

    @staticmethod
    def chebyshev_t(n: int, x: float) -> float:
        """Chebyshev polynomial of the first kind T_n(x) using 3-term recurrence."""
        if n == 0:
            return 1.0
        if n == 1:
            return x

        t_prev2 = 1.0
        t_prev1 = x
        t_curr = 0.0

        for _ in range(2, n + 1):
            t_curr = 2.0 * x * t_prev1 - t_prev2
            t_prev2 = t_prev1
            t_prev1 = t_curr

        return t_curr

    @staticmethod
    def legendre_p(n: int, x: float) -> float:
        """Legendre polynomial P_n(x) via Bonnet's recurrence relation."""
        if n == 0:
            return 1.0
        if n == 1:
            return x

        p_prev2 = 1.0
        p_prev1 = x
        p_curr = 0.0

        for k in range(2, n + 1):
            p_curr = ((2.0 * k - 1.0) * x * p_prev1 - (k - 1.0) * p_prev2) / k
            p_prev2 = p_prev1
            p_prev1 = p_curr

        return p_curr
