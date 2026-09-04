import React, { useState } from 'react';

export const CandidateSafetyPortal: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'checklist' | 'emergency' | 'rights'>('checklist');

  return (
    <div className="rounded-2xl p-6 bg-white border border-[#e8dfd2] shadow-sm space-y-6">
      <div className="flex items-center justify-between border-b border-[#e8dfd2] pb-4">
        <div>
          <h3 className="text-lg font-bold text-stone-900">Candidate Safety & Legal Rights Portal</h3>
          <p className="text-xs text-stone-500 mt-0.5">Empowering job seekers with verified anti-fraud protocols</p>
        </div>
        <div className="flex gap-2">
          {(['checklist', 'emergency', 'rights'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold capitalize transition-all ${
                activeTab === tab
                  ? 'bg-amber-800 text-white'
                  : 'bg-stone-100 text-stone-600 hover:bg-stone-200'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {activeTab === 'checklist' && (
        <div className="space-y-3">
          <div className="p-3.5 rounded-xl bg-[#fbf9f4] border border-[#e8dfd2] flex items-start gap-3">
            <span className="font-mono text-xs font-bold text-amber-800 bg-amber-100 px-2 py-0.5 rounded">01</span>
            <div>
              <h4 className="text-xs font-bold text-stone-900">Zero Upfront Fees Standard</h4>
              <p className="text-xs text-stone-600 mt-0.5">Legitimate employers never demand registration, training, or laptop deposit fees.</p>
            </div>
          </div>
          <div className="p-3.5 rounded-xl bg-[#fbf9f4] border border-[#e8dfd2] flex items-start gap-3">
            <span className="font-mono text-xs font-bold text-amber-800 bg-amber-100 px-2 py-0.5 rounded">02</span>
            <div>
              <h4 className="text-xs font-bold text-stone-900">Official Recruiter Email Verification</h4>
              <p className="text-xs text-stone-600 mt-0.5">Confirm corporate domain match rather than free public webmail accounts.</p>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'emergency' && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-950 space-y-2">
          <h4 className="text-xs font-bold uppercase tracking-wider text-rose-800">Cyber Crime Helpline Contacts</h4>
          <p className="text-xs leading-relaxed">If you have sent money to scammers, call <strong>1930</strong> (India Cyber Helpline) or file on <strong>cybercrime.gov.in</strong> immediately.</p>
        </div>
      )}

      {activeTab === 'rights' && (
        <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-950 space-y-2">
          <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-800">Statutory Protections</h4>
          <p className="text-xs leading-relaxed">Protected under Section 66D IT Act and Statutory Labor Standards.</p>
        </div>
      )}
    </div>
  );
};
