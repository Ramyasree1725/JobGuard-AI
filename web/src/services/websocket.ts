import { TelemetryFrame } from '../types';

type TelemetryListener = (frame: TelemetryFrame) => void;

class WebSocketService {
  private socket: WebSocket | null = null;
  private listeners: Set<TelemetryListener> = new Set();
  private reconnectTimer: any = null;

  connect() {
    if (this.socket && (this.socket.readyState === WebSocket.OPEN || this.socket.readyState === WebSocket.CONNECTING)) {
      return;
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    const wsUrl = `${protocol}//${host}/ws/telemetry`;

    try {
      this.socket = new WebSocket(wsUrl);

      this.socket.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data);
          if (msg.event === 'TELEMETRY_FRAME') {
            this.listeners.forEach((listener) => listener(msg.data));
          }
        } catch (e) {
          // ignore parsing error
        }
      };

      this.socket.onclose = () => {
        this.socket = null;
        this.reconnectTimer = setTimeout(() => this.connect(), 2000);
      };

      this.socket.onerror = () => {
        if (this.socket) {
          this.socket.close();
        }
      };
    } catch (e) {
      this.reconnectTimer = setTimeout(() => this.connect(), 2000);
    }
  }

  subscribe(listener: TelemetryListener) {
    this.listeners.add(listener);
    this.connect();
    return () => {
      this.listeners.delete(listener);
    };
  }

  disconnect() {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}

export const wsService = new WebSocketService();
