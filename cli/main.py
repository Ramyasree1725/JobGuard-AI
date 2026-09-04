"""
Aetheris Command Line Interface: Master CLI Entrypoint
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import sys
import argparse
import time
from cli.formatters import TerminalFormatter
from core.simulation.engine import SimulationEngine
from core.optimization.pareto_nsga2 import NSGA2Optimizer
from core.optimization.benchmarks import OptimizationBenchmarks


def main() -> None:
    parser = argparse.ArgumentParser(description="Aetheris Research Platform CLI")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Command: run-sim
    sim_parser = subparsers.add_parser("run-sim", help="Run standalone simulation benchmark")
    sim_parser.add_argument("--ticks", type=int, default=100, help="Number of ticks to step")

    # Command: optimize
    opt_parser = subparsers.add_parser("optimize", help="Run multi-objective NSGA-II optimization")
    opt_parser.add_argument("--generations", type=int, default=20, help="Generations to evolve")

    args = parser.parse_args()

    TerminalFormatter.print_banner()

    if args.command == "run-sim":
        print(f"[*] Initializing 60Hz Simulation Engine (Ticks: {args.ticks})...")
        engine = SimulationEngine()
        start = time.time()
        for i in range(args.ticks):
            telemetry = engine.step()
        elapsed = time.time() - start
        fps = float(args.ticks) / max(0.001, elapsed)

        print(f"[+] Simulation Completed in {elapsed:.3f}s ({fps:.1f} ticks/sec)")
        TerminalFormatter.print_table(
            ["Metric", "Value"],
            [
                ["Total Ticks", str(engine.tick_count)],
                ["Sim Time", f"{engine.sim_time:.2f}s"],
                ["Drone Pos", str(engine.rigid_body.position)],
                ["Drone Speed", f"{engine.rigid_body.linear_velocity.norm():.2f} m/s"],
                ["Swarm Count", str(len(engine.swarm.agents))]
            ]
        )

    elif args.command == "optimize":
        print(f"[*] Starting NSGA-II Pareto Optimization (Generations: {args.generations})...")
        optimizer = NSGA2Optimizer(population_size=40, num_variables=4)
        for g in range(args.generations):
            front = optimizer.step_generation(OptimizationBenchmarks.zdt1_multiobjective)
            print(f"  -> Gen {g+1:02d}: Pareto Front Size = {len(front)}")

        rows = [[f"Sol #{idx+1}", f"{ind.objectives[0]:.4f}", f"{ind.objectives[1]:.4f}", str([round(g, 3) for g in ind.genes])] for idx, ind in enumerate(front[:10])]
        TerminalFormatter.print_table(["Solution", "Obj 1 (f1)", "Obj 2 (f2)", "Variables"], rows)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
