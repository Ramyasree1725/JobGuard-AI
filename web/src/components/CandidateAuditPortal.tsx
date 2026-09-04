import React, { useState } from 'react';

export const CandidateAuditPortal: React.FC = () => {
  const [inputText, setInputText] = useState('');

  return (
    <div className="rounded-2xl p-8 bg-white border border-[#e8dfd2] shadow-sm space-y-6">
      <div className="border-b border-[#e8dfd2] pb-4">
        <h2 className="text-xl font-extrabold text-stone-900">Job Posting & Offer Verification Portal</h2>
        <p className="text-xs text-stone-500 mt-1">Direct multi-vector audit engine for recruitment security</p>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-xs font-bold text-stone-700 uppercase mb-2">Job Offer Text or Description</label>
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            rows={5}
            placeholder="Paste job description, recruiter WhatsApp message, or appointment letter text..."
            className="w-full p-4 rounded-xl border border-[#e8dfd2] bg-[#fbf9f4] text-xs font-mono focus:outline-none focus:ring-2 focus:ring-amber-700"
          />
        </div>

        <button
          className="w-full py-3.5 rounded-xl bg-amber-800 text-white font-bold text-sm shadow hover:bg-amber-900 transition-all"
        >
          Execute Comprehensive Fraud Audit
        </button>
      </div>
    </div>
  );
};
