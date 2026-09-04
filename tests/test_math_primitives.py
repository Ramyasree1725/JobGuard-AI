"""
Unit Tests: Aetheris Mathematical Foundations
"""
import math
import pytest
from core.math.vectors import Vector3D, VectorND
from core.math.matrices import Matrix3x3, Matrix4x4, MatrixDense
from core.math.quaternions import Quaternion
from core.math.splines import CubicBezier3D
from core.math.geometry import AABB3D, Sphere3D, Ray3D


def test_vector3d_operations():
    v1 = Vector3D(1.0, 2.0, 3.0)
    v2 = Vector3D(4.0, 5.0, 6.0)

    # Addition
    v_add = v1 + v2
    assert v_add == Vector3D(5.0, 7.0, 9.0)

    # Dot Product
    dot = v1.dot(v2)
    assert math.isclose(dot, 32.0, abs_tol=1e-6)

    # Cross Product: [2*6 - 3*5, 3*4 - 1*6, 1*5 - 2*4] = [-3, 6, -3]
    cross = v1.cross(v2)
    assert cross == Vector3D(-3.0, 6.0, -3.0)

    # Norm & Normalize
    norm = v1.norm()
    assert math.isclose(norm, math.sqrt(14.0), abs_tol=1e-6)
    v_norm = v1.normalize()
    assert math.isclose(v_norm.norm(), 1.0, abs_tol=1e-6)


def test_matrix3x3_inverse_and_multiplication():
    # Rotation 90 deg around Z
    r_z = Matrix3x3.rotation_z(math.pi / 2.0)
    v_x = Vector3D(1.0, 0.0, 0.0)
    v_rot = r_z * v_x
    assert math.isclose(v_rot.x, 0.0, abs_tol=1e-6)
    assert math.isclose(v_rot.y, 1.0, abs_tol=1e-6)

    # Invert
    inv_r = r_z.inverse()
    identity_approx = r_z * inv_r
    assert math.isclose(identity_approx[0][0], 1.0, abs_tol=1e-6)
    assert math.isclose(identity_approx[1][1], 1.0, abs_tol=1e-6)


def test_quaternion_rotations():
    q_z = Quaternion.from_axis_angle(Vector3D(0.0, 0.0, 1.0), math.pi / 2.0)
    v = Vector3D(1.0, 0.0, 0.0)
    v_rot = q_z.rotate_vector(v)
    assert math.isclose(v_rot.x, 0.0, abs_tol=1e-6)
    assert math.isclose(v_rot.y, 1.0, abs_tol=1e-6)


def test_geometry_intersections():
    sphere = Sphere3D(Vector3D(0.0, 0.0, 5.0), 2.0)
    ray = Ray3D(Vector3D(0.0, 0.0, 0.0), Vector3D(0.0, 0.0, 1.0))
    t_hit = ray.intersect_sphere(sphere)
    assert t_hit is not None
    assert math.isclose(t_hit, 3.0, abs_tol=1e-5)
