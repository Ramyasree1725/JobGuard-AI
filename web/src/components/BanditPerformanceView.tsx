import React, { useState } from 'react';
import { apiClient } from '../services/api';

export const BanditPerformanceView: React.FC = () => {
  const [armStatus, setArmStatus] = useState<any[]>([]);
  const [lastReward, setLastReward] = useState<number | null>(null);
  const [selectedArm, setSelectedArm] = useState<number | null>(null);
  const [pullCount, setPullCount] = useState<number>(0);

  const handlePull = async () => {
    const context = [Math.random(), Math.random(), Math.random(), Math.random()];
    const res = await apiClient.pullBandit(context);
    setSelectedArm(res.selected_arm);
    setLastReward(res.simulated_reward);
    setArmStatus(res.arms_state);
    setPullCount((c) => c + 1);
  };

  return (
    <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div>
          <h3 className="text-sm font-bold text-emerald-400 uppercase font-mono">
            LinUCB Contextual Multi-Armed Bandit
          </h3>
          <p className="text-xs text-slate-400 font-mono">Disjoint Ridge Regression Confidence Bounds</p>
        </div>
        <div className="flex items-center space-x-3">
          <span className="text-xs font-mono text-slate-400">Total Pulls: {pullCount}</span>
          <button onClick={handlePull} className="btn-primary text-xs">
            Pull Bandit Arm
          </button>
        </div>
      </div>

      {lastReward !== null && (
        <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg text-xs font-mono flex items-center justify-between">
          <span>Chosen Arm: <strong className="text-cyan-400">Arm #{selectedArm}</strong></span>
          <span>Reward Received: <strong className="text-emerald-400">+{lastReward.toFixed(2)}</strong></span>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
        {[0, 1, 2, 3, 4].map((armId) => {
          const armInfo = armStatus.find((a) => a.arm_id === armId);
          const isCurrent = selectedArm === armId;
          return (
            <div
              key={armId}
              className={`p-4 rounded-xl border transition-all ${
                isCurrent
                  ? 'bg-cyan-950/40 border-cyan-500 shadow-lg shadow-cyan-500/20'
                  : 'bg-slate-950 border-slate-800'
              }`}
            >
              <div className="text-xs font-mono font-bold text-slate-300">Arm {armId}</div>
              <div className="mt-3 text-xs font-mono space-y-1 text-slate-400">
                <div>Pulls: <span className="text-slate-200">{armInfo?.pull_count ?? 0}</span></div>
                <div>ThetaNorm: <span className="text-slate-200">{armInfo?.theta_norm?.toFixed(2) ?? '0.00'}</span></div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
