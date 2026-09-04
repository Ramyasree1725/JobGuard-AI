"""
Aetheris Optimization and Neural-Symbolic Reasoning Core Module
"""
from core.optimization.gp_kernels import BaseKernel, RBFKernel, Matern52Kernel, PeriodicKernel
from core.optimization.bayesian_gp import GaussianProcessRegressor, BayesianOptimizer
from core.optimization.pareto_nsga2 import Individual, NSGA2Optimizer
from core.optimization.ast_genetic_trees import (
    ASTNode, ConstantNode, VariableNode, BinaryOpNode, UnaryOpNode, TreeGenerator
)
from core.optimization.symbolic_regression import SymbolicProgram, SymbolicRegressionEngine
from core.optimization.particle_swarm import Particle, ParticleSwarmOptimizer, SimulatedAnnealingOptimizer
from core.optimization.benchmarks import OptimizationBenchmarks

__all__ = [
    'BaseKernel', 'RBFKernel', 'Matern52Kernel', 'PeriodicKernel',
    'GaussianProcessRegressor', 'BayesianOptimizer',
    'Individual', 'NSGA2Optimizer',
    'ASTNode', 'ConstantNode', 'VariableNode', 'BinaryOpNode', 'UnaryOpNode', 'TreeGenerator',
    'SymbolicProgram', 'SymbolicRegressionEngine',
    'Particle', 'ParticleSwarmOptimizer', 'SimulatedAnnealingOptimizer',
    'OptimizationBenchmarks'
]
