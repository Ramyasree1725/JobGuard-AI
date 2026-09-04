/**
 * JobGuard Web Architecture - Telemetry Client & Metric Dispatcher
 * Dispatches anonymous client performance and verification metrics to backend hub.
 */

export interface ClientTelemetryEvent {
  eventType: string;
  durationMs: number;
  timestamp: number;
  metadata?: Record<string, unknown>;
}

export class TelemetryClient {
  private static buffer: ClientTelemetryEvent[] = [];

  public static trackEvent(eventType: string, durationMs: number, metadata?: Record<string, unknown>): void {
    const evt: ClientTelemetryEvent = {
      eventType,
      durationMs,
      timestamp: Date.now(),
      metadata,
    };
    this.buffer.push(evt);
    if (this.buffer.length > 50) {
      this.flush();
    }
  }

  public static flush(): void {
    // In-memory flush
    this.buffer = [];
  }
}
