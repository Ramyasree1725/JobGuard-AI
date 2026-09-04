import React from 'react';

interface NetworkNode {
  id: string;
  label: string;
  type: 'recruiter' | 'domain' | 'payment_channel' | 'safe_corp';
  riskScore: number;
}

interface NetworkGraphProps {
  nodes?: NetworkNode[];
}

export const NetworkGraph: React.FC<NetworkGraphProps> = ({ nodes = [] }) => {
  const defaultNodes: NetworkNode[] = [
    { id: '1', label: 'Recruiter Domain', type: 'domain', riskScore: 85 },
    { id: '2', label: 'Telegram Bot Gateway', type: 'payment_channel', riskScore: 90 },
    { id: '3', label: 'Corporate Portal (Workday)', type: 'safe_corp', riskScore: 0 },
    { id: '4', label: 'Unverified Free Mail (@gmail)', type: 'recruiter', riskScore: 70 },
  ];

  const activeNodes = nodes.length > 0 ? nodes : defaultNodes;

  return (
    <div className="rounded-2xl p-6 bg-white border border-[#e8dfd2] shadow-sm space-y-4">
      <div className="flex items-center justify-between border-b border-[#e8dfd2] pb-3">
        <h3 className="text-sm font-bold text-stone-900 uppercase tracking-wider">
          Entity Interconnection Graph
        </h3>
        <span className="text-xs text-stone-500 font-mono">4 Connected Entities</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {activeNodes.map((node) => (
          <div
            key={node.id}
            className={`p-3.5 rounded-xl border flex items-center justify-between transition-all ${
              node.riskScore >= 60
                ? 'bg-rose-50 border-rose-200 text-rose-900'
                : node.riskScore >= 20
                ? 'bg-amber-50 border-amber-200 text-amber-900'
                : 'bg-emerald-50 border-emerald-200 text-emerald-900'
            }`}
          >
            <div>
              <span className="text-xs font-bold block">{node.label}</span>
              <span className="text-[10px] text-stone-500 uppercase font-mono">{node.type}</span>
            </div>
            <span className="text-xs font-extrabold font-mono px-2 py-1 rounded bg-white border">
              {node.riskScore}% Risk
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
