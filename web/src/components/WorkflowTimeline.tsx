import React from 'react';

export interface TimelineEvent {
  title: string;
  timestamp: string;
  status: 'completed' | 'current' | 'upcoming';
  description: string;
}

interface WorkflowTimelineProps {
  events?: TimelineEvent[];
}

export const WorkflowTimeline: React.FC<WorkflowTimelineProps> = ({ events = [] }) => {
  const defaultEvents: TimelineEvent[] = [
    {
      title: 'Offer Letter Upload & OCR Extraction',
      timestamp: 'Step 1',
      status: 'completed',
      description: 'Document parsed via client-side PDF.js and text normalization engine.',
    },
    {
      title: 'Zero Upfront Money & Check Fraud Audit',
      timestamp: 'Step 2',
      status: 'completed',
      description: 'Zero financial demands and check schemes verified across 64 threat signatures.',
    },
    {
      title: 'Recruiter Domain & Identity Verification',
      timestamp: 'Step 3',
      status: 'completed',
      description: 'Corporate DNS and recruiter email matched against authorized enterprise registrar.',
    },
    {
      title: '0% Zero Risk Guarantee Certificate Issued',
      timestamp: 'Step 4',
      status: 'current',
      description: 'Statutory compliance confirmed; final candidate safety report rendered.',
    },
  ];

  const activeEvents = events.length > 0 ? events : defaultEvents;

  return (
    <div className="rounded-2xl p-6 bg-white border border-[#e8dfd2] shadow-sm space-y-4">
      <h3 className="text-sm font-bold text-stone-900 uppercase tracking-wider border-b border-[#e8dfd2] pb-3">
        Audit Pipeline Execution Flow
      </h3>
      <div className="relative border-l-2 border-amber-200 ml-4 space-y-6 pl-6 py-2">
        {activeEvents.map((evt, idx) => (
          <div key={idx} className="relative group">
            <div
              className={`absolute -left-[31px] top-0.5 w-4 h-4 rounded-full border-2 bg-white ${
                evt.status === 'completed'
                  ? 'border-emerald-600 bg-emerald-600'
                  : evt.status === 'current'
                  ? 'border-amber-700 bg-amber-700'
                  : 'border-stone-300'
              }`}
            />
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-stone-900">{evt.title}</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-stone-100 text-stone-600">
                  {evt.timestamp}
                </span>
              </div>
              <p className="text-xs text-stone-500 mt-0.5 leading-relaxed">{evt.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
