import React from 'react';

interface NavigationProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  isRunning: boolean;
  onToggleSim: () => void;
  onStepSim: () => void;
}

export const Navigation: React.FC<NavigationProps> = ({
  activeTab,
  setActiveTab,
  isRunning,
  onToggleSim,
  onStepSim,
}) => {
  const navItems = [
    { id: 'simulation', label: '3D Simulation & Robotics' },
    { id: 'optimization', label: 'Neural-Symbolic & Pareto' },
    { id: 'knowledge', label: 'Knowledge Graph & NLP' },
    { id: 'recommendation', label: 'Bandits & Retrieval' },
    { id: 'consensus', label: 'Distributed Merkle Ledger' },
    { id: 'experiments', label: 'Experiment Studio' },
  ];

  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50 px-6 py-3.5 flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center font-bold text-white shadow-lg shadow-cyan-500/30">
          A
        </div>
        <div>
          <h1 className="text-lg font-bold tracking-tight text-white flex items-center gap-2">
            Aetheris <span className="text-xs px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-mono">v1.0.0</span>
          </h1>
          <p className="text-xs text-slate-400">Autonomous Research Platform</p>
        </div>
      </div>

      <nav className="flex items-center space-x-1 bg-slate-950/60 p-1 rounded-lg border border-slate-800/80">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setActiveTab(item.id)}
            className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
              activeTab === item.id
                ? 'bg-slate-800 text-cyan-400 shadow-sm border border-slate-700'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/50'
            }`}
          >
            {item.label}
          </button>
        ))}
      </nav>

      <div className="flex items-center space-x-2">
        <button
          onClick={onStepSim}
          className="px-3 py-1.5 rounded-md bg-slate-800 text-xs font-medium text-slate-300 hover:bg-slate-700 border border-slate-700"
        >
          Step Tick
        </button>
        <button
          onClick={onToggleSim}
          className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
            isRunning
              ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30 hover:bg-amber-500/30'
              : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-500/30'
          }`}
        >
          {isRunning ? 'Pause Engine' : 'Resume Engine'}
        </button>
      </div>
    </header>
  );
};
