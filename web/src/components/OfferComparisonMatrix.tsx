import React from 'react';

interface OfferComparisonProps {
  offers?: Array<{
    id: string;
    company: string;
    role: string;
    salary: string;
    riskScore: number;
    verdict: string;
  }>;
}

export const OfferComparisonMatrix: React.FC<OfferComparisonProps> = ({ offers = [] }) => {
  const sampleOffers = offers.length > 0 ? offers : [
    { id: '1', company: 'Verified Tech Corp', role: 'Software Engineer', salary: '$120,000/yr', riskScore: 0, verdict: 'SAFE' },
    { id: '2', company: 'Digital Nexus VIP', role: 'Data Entry Assistant', salary: '$5,000/week', riskScore: 85, verdict: 'CRITICAL SCAM' },
  ];

  return (
    <div className="rounded-2xl p-6 bg-white border border-[#e8dfd2] shadow-sm space-y-4">
      <h3 className="text-sm font-bold text-stone-900 uppercase tracking-wider border-b border-[#e8dfd2] pb-3">
        Side-by-Side Offer Legitimacy Comparison
      </h3>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-stone-200 text-stone-500 font-bold uppercase">
              <th className="py-2.5 px-3">Company</th>
              <th className="py-2.5 px-3">Role</th>
              <th className="py-2.5 px-3">Compensation</th>
              <th className="py-2.5 px-3">Fraud Risk</th>
              <th className="py-2.5 px-3">Verdict</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-stone-100">
            {sampleOffers.map((o) => (
              <tr key={o.id} className="hover:bg-stone-50 transition-colors">
                <td className="py-3 px-3 font-bold text-stone-800">{o.company}</td>
                <td className="py-3 px-3 text-stone-600">{o.role}</td>
                <td className="py-3 px-3 font-mono font-semibold text-stone-700">{o.salary}</td>
                <td className="py-3 px-3 font-mono font-bold">
                  <span className={o.riskScore === 0 ? 'text-emerald-600' : 'text-rose-600'}>
                    {o.riskScore}%
                  </span>
                </td>
                <td className="py-3 px-3">
                  <span
                    className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                      o.riskScore === 0
                        ? 'bg-emerald-100 text-emerald-800'
                        : 'bg-rose-100 text-rose-800'
                    }`}
                  >
                    {o.verdict}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
