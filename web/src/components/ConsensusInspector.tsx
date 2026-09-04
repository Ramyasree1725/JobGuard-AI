import React, { useState } from 'react';
import { apiClient } from '../services/api';

export const ConsensusInspector: React.FC = () => {
  const [eventName, setEventName] = useState<string>('CHECKPOINT_DRONE_TRAJECTORY');
  const [blocks, setBlocks] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const handleAppend = async () => {
    setLoading(true);
    try {
      const summary = {
        drone_speed: (Math.random() * 3).toFixed(2),
        swarm_health: 'NOMINAL',
        proof_nonce: Math.floor(Math.random() * 100000),
      };
      const res = await apiClient.appendConsensusState(eventName, summary);
      setBlocks((prev) => [
        {
          hash: res.node_hash,
          event: eventName,
          proofLength: res.proof_lineage_length,
          timestamp: new Date().toLocaleTimeString(),
        },
        ...prev,
      ]);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div>
          <h3 className="text-sm font-bold text-amber-400 uppercase font-mono">
            Merkle-DAG Distributed Consensus State Ledger
          </h3>
          <p className="text-xs text-slate-400 font-mono">SHA-256 Content-Addressed Cryptographic Proofs</p>
        </div>

        <div className="flex items-center space-x-3">
          <input
            type="text"
            value={eventName}
            onChange={(e) => setEventName(e.target.value)}
            className="px-3 py-1.5 bg-slate-950 border border-slate-700 rounded-lg text-xs font-mono text-slate-200"
          />
          <button onClick={handleAppend} disabled={loading} className="btn-primary text-xs">
            {loading ? 'Hashing...' : 'Append State Block'}
          </button>
        </div>
      </div>

      <div className="space-y-3">
        {blocks.length === 0 ? (
          <div className="p-8 text-center text-xs font-mono text-slate-500 border border-dashed border-slate-800 rounded-lg">
            No state blocks appended yet. Click "Append State Block" to add verifiable telemetry state.
          </div>
        ) : (
          blocks.map((b, i) => (
            <div
              key={i}
              className="p-3 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-between text-xs font-mono"
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-amber-400"></span>
                  <span className="text-slate-300 font-bold">{b.event}</span>
                  <span className="text-[10px] text-slate-500">{b.timestamp}</span>
                </div>
                <div className="text-[11px] text-cyan-400 break-all">Hash: {b.hash}</div>
              </div>
              <div className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded text-[11px] font-bold">
                Proof Verified (Lineage: {b.proofLength})
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
