import React from 'react';

interface AuditReportProps {
  reportId: string;
  candidateName: string;
  companyName: string;
  roleTitle: string;
  verdict: string;
  riskScore: number;
  zeroRiskGuaranteed: boolean;
  researchCheckpoints: Array<{
    title: string;
    status: 'PASSED' | 'FAILED';
    summary: string;
  }>;
}

export const AuditReportView: React.FC<AuditReportProps> = ({
  reportId,
  candidateName,
  companyName,
  roleTitle,
  verdict,
  riskScore,
  zeroRiskGuaranteed,
  researchCheckpoints,
}) => {
  return (
    <div className="rounded-2xl p-8 bg-white border border-[#e8dfd2] shadow-md space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#e8dfd2] pb-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs font-bold px-3 py-1 rounded-full uppercase bg-amber-100 text-amber-900 border border-amber-200">
              Official Verification Audit
            </span>
            {zeroRiskGuaranteed && (
              <span className="text-xs font-bold px-3 py-1 rounded-full uppercase bg-emerald-100 text-emerald-800 border border-emerald-300">
                0% Zero Risk Guarantee
              </span>
            )}
          </div>
          <h2 className="text-2xl font-extrabold text-stone-900">Employment Contract Audit Certificate</h2>
          <p className="text-xs text-stone-500 font-mono mt-1">Audit Report Reference: {reportId}</p>
        </div>
        <div className="p-4 rounded-xl bg-[#f7f4ed] border border-[#e8dfd2] text-center min-w-[140px]">
          <span className="text-[10px] font-bold text-stone-500 uppercase block">Fraud Risk</span>
          <span className="text-3xl font-extrabold font-mono text-emerald-600">{riskScore}%</span>
        </div>
      </div>

      {/* Overview Metadata */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
        <div className="p-3.5 rounded-xl bg-[#f7f4ed] border border-[#e8dfd2]">
          <span className="text-stone-500 block font-semibold">Candidate:</span>
          <span className="font-bold text-stone-800 text-sm">{candidateName || 'Verified Candidate'}</span>
        </div>
        <div className="p-3.5 rounded-xl bg-[#f7f4ed] border border-[#e8dfd2]">
          <span className="text-stone-500 block font-semibold">Company Entity:</span>
          <span className="font-bold text-stone-800 text-sm">{companyName || 'Corporate Entity'}</span>
        </div>
        <div className="p-3.5 rounded-xl bg-[#f7f4ed] border border-[#e8dfd2]">
          <span className="text-stone-500 block font-semibold">Role Title:</span>
          <span className="font-bold text-stone-800 text-sm">{roleTitle || 'Job Requisition'}</span>
        </div>
      </div>

      {/* Multi-Vector Research Checkpoints */}
      <div className="space-y-3">
        <h4 className="text-xs font-bold uppercase tracking-wider text-amber-800">
          Multi-Vector Research Verification Checkpoints
        </h4>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {researchCheckpoints.map((cp, idx) => (
            <div
              key={idx}
              className={`p-3.5 rounded-xl border ${
                cp.status === 'PASSED'
                  ? 'bg-emerald-50/40 border-emerald-200 text-emerald-950'
                  : 'bg-rose-50/40 border-rose-200 text-rose-950'
              }`}
            >
              <div className="flex items-center justify-between gap-2 mb-1">
                <span className="text-xs font-bold">{cp.title}</span>
                <span
                  className={`text-[10px] font-extrabold px-2 py-0.5 rounded ${
                    cp.status === 'PASSED' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
                  }`}
                >
                  {cp.status}
                </span>
              </div>
              <p className="text-[11px] text-stone-600 leading-snug">{cp.summary}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
