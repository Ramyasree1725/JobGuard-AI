"""
Aetheris Server Engine: Optimization & Neural-Symbolic REST Endpoints
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import uuid
from fastapi import APIRouter
from server.models import OptimizationRunRequest
from core.optimization.pareto_nsga2 import NSGA2Optimizer
from core.optimization.bayesian_gp import BayesianOptimizer
from core.optimization.symbolic_regression import SymbolicRegressionEngine
from core.optimization.particle_swarm import ParticleSwarmOptimizer
from core.optimization.benchmarks import OptimizationBenchmarks
from server.storage.db_engine import db

router = APIRouter(prefix="/api/optimization", tags=["Optimization"])


@router.post("/run")
async def run_optimization(req: OptimizationRunRequest):
    """Executes multi-objective or global optimization experiment."""
    exp_id = f"opt_{uuid.uuid4().hex[:8]}"

    if req.algorithm == "nsga2":
        optimizer = NSGA2Optimizer(population_size=40, num_variables=4)
        history = []
        for gen in range(req.num_iterations):
            pareto_front = optimizer.step_generation(OptimizationBenchmarks.zdt1_multiobjective)
            history.append({
                "generation": gen + 1,
                "front_size": len(pareto_front),
                "sample_objectives": [ind.objectives for ind in pareto_front[:15]]
            })

        db.record_experiment(exp_id, "NSGA2-Pareto", "COMPLETED", {"generations": req.num_iterations, "final_front_size": len(pareto_front)})
        return {
            "experiment_id": exp_id,
            "algorithm": "NSGA-II Multi-Objective",
            "history": history,
            "pareto_front": [
                {"genes": ind.genes, "objectives": ind.objectives}
                for ind in pareto_front
            ]
        }

    elif req.algorithm == "bayesian":
        bayes = BayesianOptimizer(bounds_min=[-5.0, -5.0], bounds_max=[5.0, 5.0], acquisition="ucb")
        history = []
        for step in range(req.num_iterations):
            cand = bayes.ask()
            score = -OptimizationBenchmarks.ackley(cand) # Maximizing negative Ackley
            bayes.tell(cand, score)
            history.append({"iteration": step + 1, "point": cand, "score": score})

        db.record_experiment(exp_id, "Bayesian-GP", "COMPLETED", {"iterations": req.num_iterations})
        return {
            "experiment_id": exp_id,
            "algorithm": "Bayesian Optimization (Gaussian Process)",
            "history": history
        }

    elif req.algorithm == "pso":
        pso = ParticleSwarmOptimizer(
            cost_func=OptimizationBenchmarks.rastrigin,
            dim=4,
            bounds_min=[-5.12] * 4,
            bounds_max=[5.12] * 4,
            num_particles=30
        )
        history = []
        for it in range(req.num_iterations):
            best_pos, best_score = pso.step()
            history.append({"iteration": it + 1, "best_pos": best_pos, "best_score": best_score})

        db.record_experiment(exp_id, "PSO", "COMPLETED", {"best_score": best_score})
        return {
            "experiment_id": exp_id,
            "algorithm": "Particle Swarm Optimization",
            "best_position": best_pos,
            "best_score": best_score,
            "history": history
        }

    elif req.algorithm == "symbolic":
        # Synthetic dataset: y = x0^2 + sin(x1)
        X = [{"x0": (i * 0.2 - 2.0), "x1": (i * 0.1)} for i in range(25)]
        y_true = [d["x0"]**2 + (d["x1"] * 0.5) for d in X]

        sym_engine = SymbolicRegressionEngine(variable_names=["x0", "x1"], population_size=50)
        history = []
        for gen in range(req.num_iterations):
            best_prog = sym_engine.step_generation(X, y_true)
            history.append({
                "generation": gen + 1,
                "fitness": best_prog.fitness,
                "mse": best_prog.mse_loss,
                "formula": best_prog.root.to_expression_string()
            })

        db.record_experiment(exp_id, "Symbolic-Regression", "COMPLETED", {"final_formula": best_prog.root.to_expression_string()})
        return {
            "experiment_id": exp_id,
            "algorithm": "AST Symbolic Regression",
            "discovered_formula": best_prog.root.to_expression_string(),
            "final_mse": best_prog.mse_loss,
            "history": history
        }

    return {"error": f"Unknown algorithm: {req.algorithm}"}
