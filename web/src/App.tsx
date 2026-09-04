import React, { useState } from 'react';
import { Navigation } from './components/Navigation';
import { SimulationViewport } from './components/SimulationViewport';
import { TelemetryDashboard } from './components/TelemetryDashboard';
import { ParetoFrontierView } from './components/ParetoFrontierView';
import { KnowledgeGraphExplorer } from './components/KnowledgeGraphExplorer';
import { BanditPerformanceView } from './components/BanditPerformanceView';
import { ConsensusInspector } from './components/ConsensusInspector';
import { ExperimentStudio } from './components/ExperimentStudio';
import { useTelemetry } from './hooks/useTelemetry';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('simulation');
  const { telemetry, isRunning, toggleSimulation, stepSingle } = useTelemetry();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navigation
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        isRunning={isRunning}
        onToggleSim={toggleSimulation}
        onStepSim={stepSingle}
      />

      <main className="flex-1 p-6 max-w-7xl mx-auto w-full space-y-6">
        {activeTab === 'simulation' && (
          <div className="space-y-6">
            <SimulationViewport telemetry={telemetry} />
            <TelemetryDashboard telemetry={telemetry} />
          </div>
        )}

        {activeTab === 'optimization' && <ParetoFrontierView />}

        {activeTab === 'knowledge' && <KnowledgeGraphExplorer />}

        {activeTab === 'recommendation' && <BanditPerformanceView />}

        {activeTab === 'consensus' && <ConsensusInspector />}

        {activeTab === 'experiments' && <ExperimentStudio />}
      </main>

      <footer className="border-t border-slate-900 bg-slate-950/80 px-6 py-4 text-center text-xs font-mono text-slate-500">
        Aetheris Autonomous Systems & Research Engine &copy; 2026. Non-exclusive AI Research & Licensing Platform.
      </footer>
    </div>
  );
};

export default App;
