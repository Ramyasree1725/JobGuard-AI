import React, { useState } from 'react';
import { apiClient } from '../services/api';
import { OptimizationResult } from '../types';

export const ParetoFrontierView: React.FC = () => {
  const [algorithm, setAlgorithm] = useState<'nsga2' | 'bayesian' | 'symbolic' | 'pso'>('nsga2');
  const [iterations, setIterations] = useState<number>(30);
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<OptimizationResult | null>(null);

  const handleRun = async () => {
    setLoading(true);
    try {
      const res = await apiClient.runOptimization(algorithm, iterations);
      setResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between p-4 bg-slate-900 border border-slate-800 rounded-xl">
        <div className="flex items-center space-x-4">
          <div>
            <label className="text-xs text-slate-400 uppercase font-mono block mb-1">Algorithm</label>
            <select
              value={algorithm}
              onChange={(e) => setAlgorithm(e.target.value as any)}
              className="bg-slate-800 text-xs font-mono border border-slate-700 rounded-md px-3 py-1.5 text-slate-200"
            >
              <option value="nsga2">NSGA-II (Multi-Objective Pareto)</option>
              <option value="bayesian">Bayesian Optimization (GP-UCB)</option>
              <option value="symbolic">AST Symbolic Regression</option>
              <option value="pso">Particle Swarm Optimization (PSO)</option>
            </select>
          </div>

          <div>
            <label className="text-xs text-slate-400 uppercase font-mono block mb-1">Iterations / Gens</label>
            <input
              type="number"
              value={iterations}
              onChange={(e) => setIterations(Math.max(1, parseInt(e.target.value) || 1))}
              className="bg-slate-800 text-xs font-mono border border-slate-700 rounded-md px-3 py-1.5 text-slate-200 w-24"
            />
          </div>
        </div>

        <button
          onClick={handleRun}
          disabled={loading}
          className="btn-primary text-xs flex items-center gap-2"
        >
          {loading ? 'Optimizing...' : 'Execute Research Job'}
        </button>
      </div>

      {result && (
        <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <h3 className="text-sm font-bold text-cyan-400">{result.algorithm}</h3>
              <p className="text-xs font-mono text-slate-400">Job ID: {result.experiment_id}</p>
            </div>
            {result.discovered_formula && (
              <div className="px-3 py-1 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-bold">
                Formula: {result.discovered_formula}
              </div>
            )}
            {result.best_score !== undefined && (
              <div className="px-3 py-1 rounded bg-purple-500/10 border border-purple-500/30 text-purple-300 text-xs font-mono">
                Best Score: {result.best_score.toFixed(4)}
              </div>
            )}
          </div>

          {result.pareto_front && (
            <div>
              <h4 className="text-xs font-semibold uppercase text-slate-400 font-mono mb-2">
                Pareto Non-Dominated Frontier (ZDT1 Minimization f1 vs f2)
              </h4>
              <div className="h-64 bg-slate-950 border border-slate-800 rounded-lg p-4 relative flex items-end">
                {result.pareto_front.map((sol, idx) => {
                  const left = Math.min(95, Math.max(5, sol.objectives[0] * 90));
                  const bottom = Math.min(95, Math.max(5, (1.0 - Math.min(1.0, sol.objectives[1])) * 90));
                  return (
                    <div
                      key={idx}
                      style={{ left: `${left}%`, bottom: `${bottom}%` }}
                      className="absolute w-3 h-3 bg-cyan-400 rounded-full hover:scale-150 transition-all cursor-pointer shadow-md shadow-cyan-500/50"
                      title={`f1: ${sol.objectives[0].toFixed(3)}, f2: ${sol.objectives[1].toFixed(3)}`}
                    />
                  );
                })}
              </div>
            </div>
          )}

          <div className="overflow-x-auto max-h-48">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-slate-800 text-slate-400 border-b border-slate-700">
                <tr>
                  <th className="p-2">Step</th>
                  <th className="p-2">Telemetry Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-300">
                {result.history.map((h, i) => (
                  <tr key={i} className="hover:bg-slate-800/30">
                    <td className="p-2 font-bold text-cyan-400">{i + 1}</td>
                    <td className="p-2">{JSON.stringify(h)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
