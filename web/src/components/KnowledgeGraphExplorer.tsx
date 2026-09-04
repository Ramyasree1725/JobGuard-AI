import React, { useState, useEffect } from 'react';
import { apiClient } from '../services/api';

export const KnowledgeGraphExplorer: React.FC = () => {
  const [graphData, setGraphData] = useState<any>(null);
  const [prompt, setPrompt] = useState<string>('autonomous robotic research prototype');
  const [generatedText, setGeneratedText] = useState<string>('');
  const [loadingText, setLoadingText] = useState<boolean>(false);

  useEffect(() => {
    apiClient.getKnowledgeGraph().then(setGraphData);
  }, []);

  const handleGenerate = async () => {
    setLoadingText(true);
    try {
      const res = await apiClient.generateText(prompt, 30);
      setGeneratedText(res.generated_text);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingText(false);
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* Knowledge Graph Explorer */}
      <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <h3 className="text-sm font-bold text-cyan-400 uppercase font-mono">Knowledge Graph Triples</h3>
          <span className="text-xs font-mono text-slate-400">
            {graphData?.num_triples ?? 0} Triples / {graphData?.num_entities ?? 0} Entities
          </span>
        </div>

        <div className="space-y-2 max-h-80 overflow-y-auto">
          {graphData?.sample_triples?.map((t: any, idx: number) => (
            <div
              key={idx}
              className="p-2.5 rounded-lg bg-slate-950 border border-slate-800/80 flex items-center justify-between text-xs font-mono"
            >
              <span className="text-cyan-300 font-semibold">{t.head}</span>
              <span className="text-amber-400 text-[11px] px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/20">
                --[{t.relation}]--&gt;
              </span>
              <span className="text-emerald-300 font-semibold">{t.tail}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Transformer Text Generation Sandbox */}
      <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl space-y-4 flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
            <h3 className="text-sm font-bold text-purple-400 uppercase font-mono">
              Scratch Transformer Autoregressive LM
            </h3>
            <span className="text-xs font-mono text-purple-300">BPE + Attention</span>
          </div>

          <div className="space-y-3">
            <label className="text-xs font-mono text-slate-400 uppercase block">Input Prompt</label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="w-full h-24 p-3 bg-slate-950 border border-slate-800 rounded-lg text-xs font-mono text-slate-200 focus:outline-none focus:border-purple-500"
            />
          </div>
        </div>

        <div className="space-y-3">
          <button
            onClick={handleGenerate}
            disabled={loadingText}
            className="w-full py-2 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 font-semibold text-xs rounded-lg transition-all text-white shadow-lg shadow-purple-500/20"
          >
            {loadingText ? 'Generating via Attention...' : 'Generate Text'}
          </button>

          {generatedText && (
            <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg text-xs font-mono text-emerald-300">
              <span className="text-slate-500 block mb-1 font-bold">Generated Output:</span>
              "{generatedText}"
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
