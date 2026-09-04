const API_BASE = '/api';

export const apiClient = {
  async getSimulationStatus() {
    const res = await fetch(`${API_BASE}/simulation/status`);
    return res.json();
  },

  async startSimulation() {
    const res = await fetch(`${API_BASE}/simulation/start`, { method: 'POST' });
    return res.json();
  },

  async stopSimulation() {
    const res = await fetch(`${API_BASE}/simulation/stop`, { method: 'POST' });
    return res.json();
  },

  async stepSimulation() {
    const res = await fetch(`${API_BASE}/simulation/step`, { method: 'POST' });
    return res.json();
  },

  async commandArmReach(x: number, y: number, z: number) {
    const res = await fetch(`${API_BASE}/simulation/arm/reach`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ x, y, z }),
    });
    return res.json();
  },

  async runOptimization(algorithm: string, num_iterations: number) {
    const res = await fetch(`${API_BASE}/optimization/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ algorithm, num_iterations }),
    });
    return res.json();
  },

  async generateText(prompt: string, max_tokens = 25) {
    const res = await fetch(`${API_BASE}/nlp/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, max_tokens }),
    });
    return res.json();
  },

  async getKnowledgeGraph() {
    const res = await fetch(`${API_BASE}/knowledge/graph`);
    return res.json();
  },

  async pullBandit(user_features: number[] = [0.5, 0.2, 0.8, 0.1]) {
    const res = await fetch(`${API_BASE}/recommendation/bandit/pull`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_features }),
    });
    return res.json();
  },

  async appendConsensusState(event_name: string, telemetry_summary: any) {
    const res = await fetch(`${API_BASE}/consensus/append-state`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ event_name, telemetry_summary }),
    });
    return res.json();
  },
};
