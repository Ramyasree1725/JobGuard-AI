import React from 'react';

interface RadarProps {
  scores: {
    paymentDemands: number;
    impersonation: number;
    urgency: number;
    salaryBait: number;
    vagueSpecs: number;
  };
}

export const ThreatRadarChart: React.FC<RadarProps> = ({ scores }) => {
  return (
    <div className="rounded-2xl p-6 bg-white border border-[#e8dfd2] shadow-sm space-y-4">
      <h3 className="text-sm font-bold text-stone-900 uppercase tracking-wider border-b border-[#e8dfd2] pb-3">
        Multi-Vector Threat Radar Distribution
      </h3>
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 text-center">
        {Object.entries(scores).map(([k, v]) => (
          <div key={k} className="p-3 rounded-xl bg-[#f7f4ed] border border-[#e8dfd2]">
            <span className="text-[10px] uppercase font-bold text-stone-500 block truncate">
              {k.replace(/([A-Z])/g, ' $1')}
            </span>
            <span
              className={`text-xl font-extrabold font-mono mt-1 block ${
                v >= 60 ? 'text-rose-600' : v >= 25 ? 'text-amber-600' : 'text-emerald-600'
              }`}
            >
              {v}%
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
