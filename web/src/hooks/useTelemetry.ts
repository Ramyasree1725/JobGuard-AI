import { useState, useEffect } from 'react';
import { TelemetryFrame } from '../types';
import { wsService } from '../services/websocket';
import { apiClient } from '../services/api';

export function useTelemetry() {
  const [telemetry, setTelemetry] = useState<TelemetryFrame | null>(null);
  const [isRunning, setIsRunning] = useState<boolean>(true);

  useEffect(() => {
    // Fetch initial snapshot
    apiClient.getSimulationStatus().then((res) => {
      if (res && res.telemetry) {
        setTelemetry(res.telemetry);
        setIsRunning(res.is_running);
      }
    });

    // Subscribe to live WebSocket telemetry stream
    const unsubscribe = wsService.subscribe((frame) => {
      setTelemetry(frame);
    });

    return () => {
      unsubscribe();
    };
  }, []);

  const toggleSimulation = async () => {
    if (isRunning) {
      await apiClient.stopSimulation();
      setIsRunning(false);
    } else {
      await apiClient.startSimulation();
      setIsRunning(true);
    }
  };

  const stepSingle = async () => {
    const res = await apiClient.stepSimulation();
    if (res && res.telemetry) {
      setTelemetry(res.telemetry);
    }
  };

  return { telemetry, isRunning, toggleSimulation, stepSingle };
}
