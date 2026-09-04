"""
JobGuard Core Security - Cryptographic Benchmark & Performance Suite
Tests high-throughput key generation, symmetric throughput, and signature latency.
"""

import time
import os
import hashlib
from typing import Dict, List, Tuple
from .crypto_primitives import HKDF, ChaCha20Poly1305AEAD, SHA256HMAC, ConstantTime


class CryptoBenchmarkSuite:
    """Measures encryption and hashing throughput for security audit compliance."""

    @staticmethod
    def benchmark_aead_throughput(payload_size_kb: int = 64, iterations: int = 20) -> Dict[str, float]:
        key = os.urandom(32)
        nonce = os.urandom(12)
        payload = os.urandom(payload_size_kb * 1024)
        aead = ChaCha20Poly1305AEAD(key)

        start = time.monotonic()
        total_bytes = 0

        for _ in range(iterations):
            ct, tag = aead.encrypt(nonce, payload)
            total_bytes += len(payload)
            pt = aead.decrypt(nonce, ct, tag)

        elapsed = max(1e-6, time.monotonic() - start)
        throughput_mbps = (total_bytes / (1024 * 1024)) / elapsed

        return {
            "payload_kb": float(payload_size_kb),
            "iterations": float(iterations),
            "elapsed_sec": round(elapsed, 4),
            "throughput_mbps": round(throughput_mbps, 2)
        }

    @staticmethod
    def benchmark_hkdf_derivation(iterations: int = 100) -> Dict[str, float]:
        hkdf = HKDF(hashlib.sha256)
        ikm = os.urandom(32)
        salt = os.urandom(32)
        info = b"jobguard-benchmark-test"

        start = time.monotonic()
        for i in range(iterations):
            _ = hkdf.derive(salt, ikm, info, 32)
        elapsed = max(1e-6, time.monotonic() - start)

        return {
            "derivations_count": float(iterations),
            "elapsed_sec": round(elapsed, 4),
            "derivations_per_sec": round(iterations / elapsed, 1)
        }
