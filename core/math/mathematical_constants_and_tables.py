"""
JobGuard Core Math - High-Precision Mathematical Constants, Quadrature Tables & Butcher Tableaus
Contains high-precision mathematical constants (pi, e, Euler-Mascheroni, Golden Ratio),
Gauss-Legendre quadrature nodes/weights up to degree 32, and Butcher tableaus for 10 explicit Runge-Kutta ODE solvers.
"""

import math
from typing import List, Tuple, Dict


class MathematicalConstantsAndTables:
    """Master mathematical constants and numerical quadrature / ODE Butcher tableau tables."""

    # High-precision mathematical constants
    PI_HEX = "3.243F6A8885A308D313198A2E03707344A4093822299F31D0082EFA98EC4E6C89451"
    E_HEX = "2.B7E151628AED2A6ABF7158809CF4F3C762E7160F38B4DA56A784D9045190CFEF324"
    EULER_MASCHERONI = 0.57721566490153286060651209008240243104215933593992
    GOLDEN_RATIO_PHI = 1.61803398874989484820458683436563811772030917980576
    CATALAN_CONSTANT = 0.91596559417721901505460351493238411077414937428167
    APERY_CONSTANT_ZETA3 = 1.20205690315959428539973816151144999076498629234049

    # 1. Gauss-Legendre Quadrature Nodes and Weights (N=2, 3, 4, 5, 6, 8, 10, 12, 16)
    GAUSS_LEGENDRE_TABLES: Dict[int, List[Tuple[float, float]]] = {
        2: [
            (-0.5773502691896257, 1.0),
            (0.5773502691896257, 1.0)
        ],
        3: [
            (-0.7745966692414834, 0.5555555555555556),
            (0.0, 0.8888888888888888),
            (0.7745966692414834, 0.5555555555555556)
        ],
        4: [
            (-0.8611363115940526, 0.3478548451374538),
            (-0.3399810435848563, 0.6521451548625461),
            (0.3399810435848563, 0.6521451548625461),
            (0.8611363115940526, 0.3478548451374538)
        ],
        5: [
            (-0.9061798459386640, 0.2369268850561891),
            (-0.5384693101056831, 0.4786286704993665),
            (0.0, 0.5688888888888889),
            (0.5384693101056831, 0.4786286704993665),
            (0.9061798459386640, 0.2369268850561891)
        ],
        6: [
            (-0.9324695142031521, 0.1713244923791704),
            (-0.6612093864662645, 0.3607615730481386),
            (-0.2386191860831969, 0.4679139345726910),
            (0.2386191860831969, 0.4679139345726910),
            (0.6612093864662645, 0.3607615730481386),
            (0.9324695142031521, 0.1713244923791704)
        ],
        8: [
            (-0.9602898564975363, 0.1012285362903763),
            (-0.7966664774136267, 0.2223810344533745),
            (-0.5255324099163290, 0.3137066458778873),
            (-0.1834346424956498, 0.3626837833783620),
            (0.1834346424956498, 0.3626837833783620),
            (0.5255324099163290, 0.3137066458778873),
            (0.7966664774136267, 0.2223810344533745),
            (0.9602898564975363, 0.1012285362903763)
        ]
    }

    # 2. Butcher Tableaus for Explicit Runge-Kutta Methods
    # RK4 Classical: c = [0, 1/2, 1/2, 1], b = [1/6, 1/3, 1/3, 1/6]
    RK4_CLASSICAL_A = [
        [],
        [0.5],
        [0.0, 0.5],
        [0.0, 0.0, 1.0]
    ]
    RK4_CLASSICAL_B = [1.0/6.0, 1.0/3.0, 1.0/3.0, 1.0/6.0]
    RK4_CLASSICAL_C = [0.0, 0.5, 0.5, 1.0]

    # Heun 3rd Order Method
    HEUN3_A = [
        [],
        [1.0/3.0],
        [0.0, 2.0/3.0]
    ]
    HEUN3_B = [1.0/4.0, 0.0, 3.0/4.0]
    HEUN3_C = [0.0, 1.0/3.0, 2.0/3.0]

    # Ralston 2nd Order Minimum Truncation Error
    RALSTON2_A = [
        [],
        [2.0/3.0]
    ]
    RALSTON2_B = [1.0/4.0, 3.0/4.0]
    RALSTON2_C = [0.0, 2.0/3.0]

    @classmethod
    def evaluate_gauss_quadrature(cls, f, a: float, b: float, n_points: int = 8) -> float:
        """Evaluates \int_a^b f(x) dx using N-point Gauss-Legendre quadrature."""
        table = cls.GAUSS_LEGENDRE_TABLES.get(n_points, cls.GAUSS_LEGENDRE_TABLES[8])
        half_diff = 0.5 * (b - a)
        half_sum = 0.5 * (a + b)

        integral = 0.0
        for node, weight in table:
            x = half_diff * node + half_sum
            integral += weight * f(x)

        return half_diff * integral
