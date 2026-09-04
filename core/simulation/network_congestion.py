"""
JobGuard Core Simulation - TCP Congestion Control (Reno, Cubic, BBR)
Simulates packet drop, additive increase multiplicative decrease (AIMD),
and bottleneck bandwidth round-trip propagation time (BBR).
"""

import math
from typing import List, Tuple, Dict


class TCPRenoSimulator:
    """TCP Reno Congestion Control state machine."""

    def __init__(self, ssthresh: float = 64.0):
        self.cwnd = 1.0  # Congestion window in segments
        self.ssthresh = ssthresh
        self.rtt_ms = 50.0

    def on_ack_received(self) -> float:
        """Window growth upon ACK receipt."""
        if self.cwnd < self.ssthresh:
            # Slow start: exponential growth
            self.cwnd += 1.0
        else:
            # Congestion avoidance: additive linear increase
            self.cwnd += 1.0 / self.cwnd
        return self.cwnd

    def on_packet_loss_3dup(self) -> float:
        """Fast recovery / 3 duplicate ACKs."""
        self.ssthresh = max(2.0, self.cwnd / 2.0)
        self.cwnd = self.ssthresh
        return self.cwnd

    def on_timeout(self) -> float:
        """RTO timeout penalty."""
        self.ssthresh = max(2.0, self.cwnd / 2.0)
        self.cwnd = 1.0
        return self.cwnd
