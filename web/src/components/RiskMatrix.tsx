import React from 'react';

interface RiskMatrixProps {
  score: number;
  verdict: string;
  threatDistribution: {
    paymentDemands: number;
    contactImpersonation: number;
    urgencyPressure: number;
    salaryRealism: number;
    jobSpecifications: number;
  };
}

export const RiskMatrix: React.FC<RiskMatrixProps> = ({ score, verdict, threatDistribution }) => {
  const getBadgeClass = () => {
    if (score >= 60) return 'bg-rose-100 text-rose-800 border-rose-300';
    if (score >= 25) return 'bg-amber-100 text-amber-800 border-amber-300';
    return 'bg-emerald-100 text-emerald-800 border-emerald-300';
  };

  return (
    <div className="rounded-2xl p-6 bg-white border border-[#e8dfd2] shadow-sm space-y-4">
      <div className="flex items-center justify-between border-b border-[#e8dfd2] pb-3">
        <div>
          <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase border ${getBadgeClass()}`}>
            {verdict}
          </span>
          <h3 className="text-lg font-bold text-stone-900 mt-2">Threat Vector Analysis</h3>
        </div>
        <div className="text-right">
          <span className="text-xs font-bold text-stone-500 uppercase">Fraud Score</span>
          <div className="text-3xl font-extrabold font-mono text-stone-800">{score}%</div>
        </div>
      </div>

      <div className="space-y-3">
        {Object.entries(threatDistribution).map(([vector, val]) => (
          <div key={vector} className="space-y-1">
            <div className="flex items-center justify-between text-xs text-stone-700 font-medium">
              <span className="capitalize">{vector.replace(/([A-Z])/g, ' $1')}</span>
              <span className="font-mono font-bold">{val}%</span>
            </div>
            <div className="w-full bg-[#f2eee6] rounded-full h-2 overflow-hidden">
              <div
                className={`h-full rounded-full transition-all duration-500 ${
                  val >= 60 ? 'bg-rose-600' : val >= 25 ? 'bg-amber-500' : 'bg-emerald-600'
                }`}
                style={{ width: `${val}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
