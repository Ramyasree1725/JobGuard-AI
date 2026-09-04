import React, { useState, useEffect } from 'react';

export const ExperimentStudio: React.FC = () => {
  const [experiments, setExperiments] = useState<any[]>([]);

  useEffect(() => {
    fetch('/api/experiments/list')
      .then((res) => res.json())
      .then((data) => {
        if (data && data.experiments) setExperiments(data.experiments);
      })
      .catch(() => {});
  }, []);

  return (
    <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <h3 className="text-sm font-bold text-cyan-400 uppercase font-mono">
          Research Experiment Catalog & Checkpoints
        </h3>
        <span className="text-xs font-mono text-slate-400">SQLite Logged Runs</span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs font-mono">
          <thead className="bg-slate-800/80 text-slate-400 border-b border-slate-700">
            <tr>
              <th className="p-3">Experiment ID</th>
              <th className="p-3">Algorithm</th>
              <th className="p-3">Status</th>
              <th className="p-3">Metrics / Summary</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 text-slate-300">
            {experiments.length === 0 ? (
              <tr>
                <td colSpan={4} className="p-4 text-center text-slate-500">
                  No previous experiments found in database. Run optimization jobs to populate catalog.
                </td>
              </tr>
            ) : (
              experiments.map((exp, idx) => (
                <tr key={idx} className="hover:bg-slate-800/30">
                  <td className="p-3 font-bold text-cyan-400">{exp.experiment_id}</td>
                  <td className="p-3 text-slate-200">{exp.algorithm}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      {exp.status}
                    </span>
                  </td>
                  <td className="p-3 text-slate-400">{JSON.stringify(exp.metrics)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
