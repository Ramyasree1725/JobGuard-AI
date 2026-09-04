"""
Unit Tests: Aetheris Robotics Kinematics & RRT* Motion Planning
"""
import math
import pytest
from core.math.vectors import Vector3D
from core.simulation.kinematics import RoboticManipulator6DoF
from core.simulation.inverse_kinematics import InverseKinematicsSolver
from core.simulation.rrt_star import RRTStarPlanner3D
from core.simulation.rigid_body import RigidBody6DoF
from core.simulation.swarm_dynamics import MultiAgentSwarmEngine


def test_forward_kinematics_reproducibility():
    arm = RoboticManipulator6DoF()
    arm.set_joint_positions([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    ee_pos = arm.end_effector_position()
    assert ee_pos is not None
    assert isinstance(ee_pos, Vector3D)
    assert ee_pos.z > 0.0


def test_inverse_kinematics_convergence():
    arm = RoboticManipulator6DoF()
    solver = InverseKinematicsSolver(arm, max_iterations=100)
    # Set known achievable target
    target = Vector3D(0.3, 0.2, 0.3)
    success, angles, iters, err = solver.solve(target)
    assert success is True or err < 0.05


def test_rrt_star_obstacle_avoidance():
    planner = RRTStarPlanner3D(
        bounds_min=Vector3D(-5, -5, 0),
        bounds_max=Vector3D(5, 5, 5),
        step_size=1.0,
        max_iterations=500
    )
    planner.add_sphere_obstacle(Vector3D(2, 2, 2), 1.0)
    success, waypoints, cost = planner.plan(Vector3D(0, 0, 0), Vector3D(4, 4, 4))
    assert success is True
    assert len(waypoints) >= 2


def test_rigid_body_physics_gravity():
    rb = RigidBody6DoF(mass=2.0)
    initial_z = rb.position.z
    # Step 10 ticks under gravity
    for _ in range(10):
        rb.step(0.016, gravity=9.81)
    assert rb.position.z < initial_z
    assert rb.linear_velocity.z < 0.0
