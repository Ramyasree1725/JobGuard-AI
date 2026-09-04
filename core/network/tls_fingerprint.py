"""
JobGuard Core Network - TLS JA3/JA4 Handshake Fingerprinter
Computes client hello cipher suite signatures and extension hashes
to detect automated bot scrapers and fraud syndicate tooling.
"""

import hashlib
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class CipherSuite:
    id_hex: str
    name: str
    is_secure: bool = True


@dataclass
class TLSClientHello:
    tls_version: int  # 771 for TLS 1.2, 772 for TLS 1.3
    cipher_suites: List[int]
    extensions: List[int]
    elliptic_curves: List[int]
    ec_point_formats: List[int]


class TLSFingerprinter:
    """Calculates JA3 and JA4 hashes for incoming TLS ClientHello packets."""

    KNOWN_BOT_FINGERPRINTS = {
        "b32309a26951912be7dba376398abc3b": "Python Requests Library (Default Script Scraper)",
        "51c64c77e60f3980eea90869b68c58a8": "Go-http-client (Scam Ingestion Tool)",
        "3b5074b1b082c616059da6f38e06ab5f": "cURL CLI Engine"
    }

    @staticmethod
    def calculate_ja3(hello: TLSClientHello) -> Tuple[str, str]:
        """Compute JA3 raw string and MD5 hash."""
        # JA3 = SSLVersion,Ciphers,Extensions,EllipticCurves,EllipticCurvePointFormats
        ciphers_str = "-".join(str(c) for c in hello.cipher_suites)
        extensions_str = "-".join(str(e) for e in hello.extensions)
        curves_str = "-".join(str(c) for c in hello.elliptic_curves)
        points_str = "-".join(str(p) for p in hello.ec_point_formats)

        raw_ja3 = f"{hello.tls_version},{ciphers_str},{extensions_str},{curves_str},{points_str}"
        ja3_hash = hashlib.md5(raw_ja3.encode("utf-8")).hexdigest()

        return raw_ja3, ja3_hash

    @classmethod
    def identify_client(cls, ja3_hash: str) -> Optional[str]:
        return cls.KNOWN_BOT_FINGERPRINTS.get(ja3_hash)
