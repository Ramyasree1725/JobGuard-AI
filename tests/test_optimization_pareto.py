"""
Unit Tests: Aetheris Optimization & Neural-Symbolic Solvers
"""
import pytest
from core.optimization.pareto_nsga2 import NSGA2Optimizer
from core.optimization.bayesian_gp import BayesianOptimizer
from core.optimization.symbolic_regression import SymbolicRegressionEngine
from core.optimization.benchmarks import OptimizationBenchmarks


def test_nsga2_pareto_domination():
    opt = NSGA2Optimizer(population_size=20, num_variables=2)
    front = opt.step_generation(OptimizationBenchmarks.zdt1_multiobjective)
    assert len(front) > 0
    # Pareto front items must have valid objective dimensions
    assert len(front[0].objectives) == 2


def test_bayesian_optimizer_tell_ask():
    bayes = BayesianOptimizer(bounds_min=[-2.0, -2.0], bounds_max=[2.0, 2.0])
    cand1 = bayes.ask()
    assert len(cand1) == 2
    bayes.tell(cand1, -OptimizationBenchmarks.sphere(cand1))
    cand2 = bayes.ask()
    assert len(cand2) == 2


def test_symbolic_regression_step():
    X = [{"x0": float(i) * 0.5} for i in range(10)]
    y_true = [d["x0"] * 2.0 for d in X]
    engine = SymbolicRegressionEngine(variable_names=["x0"], population_size=20)
    best = engine.step_generation(X, y_true)
    assert best is not None
    assert best.root is not None
