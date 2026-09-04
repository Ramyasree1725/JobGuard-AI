"""
Aetheris Mathematical Foundations Package
"""
from core.math.vectors import Vector3D, VectorND
from core.math.matrices import Matrix3x3, Matrix4x4, MatrixDense
from core.math.quaternions import Quaternion
from core.math.splines import CubicBezier3D, CatmullRomSpline3D
from core.math.integrators import NumericalIntegrator
from core.math.stats import GaussianDistribution, StatisticsHelper
from core.math.geometry import AABB3D, Sphere3D, Ray3D

__all__ = [
    'Vector3D', 'VectorND',
    'Matrix3x3', 'Matrix4x4', 'MatrixDense',
    'Quaternion',
    'CubicBezier3D', 'CatmullRomSpline3D',
    'NumericalIntegrator',
    'GaussianDistribution', 'StatisticsHelper',
    'AABB3D', 'Sphere3D', 'Ray3D'
]
