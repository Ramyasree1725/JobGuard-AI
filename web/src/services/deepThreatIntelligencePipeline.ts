/**
 * JobGuard AI - Deep Threat Intelligence Pipeline Client
 * Manages streaming ingestion, client-side caching, threat graph edge construction,
 * and real-time subscription feeds for recruitment fraud telemetry.
 */

export interface TelemetryStreamEvent {
  eventId: string;
  timestamp: number;
  sourceDomain: string;
  threatType: string;
  riskScore: number;
  indicators: string[];
}

export class DeepThreatIntelligencePipeline {
  private events: TelemetryStreamEvent[] = [];
  private listeners: ((event: TelemetryStreamEvent) => void)[] = [];

  constructor() {
    this.seedInitialEvents();
  }

  private seedInitialEvents(): void {
    this.events = [
      {
        eventId: 'EVT-1001',
        timestamp: Date.now() - 3600000 * 4,
        sourceDomain: 'google-careers-desk.net',
        threatType: 'TYPOSQUAT_ATS_CLONE',
        riskScore: 95,
        indicators: ['Fake Greenhouse Form', 'Lookalike Domain', 'Anonymous Registrar'],
      },
      {
        eventId: 'EVT-1002',
        timestamp: Date.now() - 3600000 * 2,
        sourceDomain: 'opt-media-vip.top',
        threatType: 'CRYPTO_TASK_ESCROW',
        riskScore: 98,
        indicators: ['USDT Recharge Demand', 'Telegram Bot Routing', 'Tiered VIP Scheme'],
      },
      {
        eventId: 'EVT-1003',
        timestamp: Date.now() - 3600000,
        sourceDomain: 'microsoft-talent-portal.org',
        threatType: 'CHECK_OVERPAYMENT',
        riskScore: 92,
        indicators: ['Counterfeit Cashier Check', 'Approved Vendor Kickback'],
      },
    ];
  }

  public subscribe(callback: (event: TelemetryStreamEvent) => void): () => void {
    this.listeners.push(callback);
    return () => {
      this.listeners = this.listeners.filter(cb => cb !== callback);
    };
  }

  public emitEvent(event: Omit<TelemetryStreamEvent, 'eventId' | 'timestamp'>): TelemetryStreamEvent {
    const fullEvent: TelemetryStreamEvent = {
      ...event,
      eventId: `EVT-${Date.now()}`,
      timestamp: Date.now(),
    };
    this.events.unshift(fullEvent);
    this.listeners.forEach(cb => cb(fullEvent));
    return fullEvent;
  }

  public getRecentEvents(limit = 10): TelemetryStreamEvent[] {
    return this.events.slice(0, limit);
  }

  public getAverageThreatScore(): number {
    if (this.events.length === 0) return 0;
    const sum = this.events.reduce((acc, ev) => acc + ev.riskScore, 0);
    return Math.round(sum / this.events.length);
  }
}
