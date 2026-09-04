"""
Aetheris Simulation and Robotics Core Module
"""
from core.simulation.kinematics import DHParameter, RoboticManipulator6DoF
from core.simulation.inverse_kinematics import InverseKinematicsSolver
from core.simulation.rrt_star import RRTNode, RRTStarPlanner3D
from core.simulation.trajectory import QuinticPolynomial1D, TrajectoryGenerator3D
from core.simulation.controllers import PIDController3D, LQRController
from core.simulation.rigid_body import RigidBody6DoF
from core.simulation.swarm_dynamics import SwarmAgent, MultiAgentSwarmEngine
from core.simulation.collision_mesh import Triangle3D, SpatialHashGrid3D
from core.simulation.sensors import SyntheticLiDAR3D, SyntheticIMU6Axis
from core.simulation.environment import SimulationEnvironment3D
from core.simulation.engine import SimulationEngine

__all__ = [
    'DHParameter', 'RoboticManipulator6DoF',
    'InverseKinematicsSolver',
    'RRTNode', 'RRTStarPlanner3D',
    'QuinticPolynomial1D', 'TrajectoryGenerator3D',
    'PIDController3D', 'LQRController',
    'RigidBody6DoF',
    'SwarmAgent', 'MultiAgentSwarmEngine',
    'Triangle3D', 'SpatialHashGrid3D',
    'SyntheticLiDAR3D', 'SyntheticIMU6Axis',
    'SimulationEnvironment3D',
    'SimulationEngine'
]
