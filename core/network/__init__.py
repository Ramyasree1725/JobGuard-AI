"""
JobGuard Core Network & Infrastructure Framework
Provides asynchronous connection pooling, DNS-over-HTTPS (DoH) resolution,
and JA3/JA4 TLS handshake fingerprinting for network scam forensics.
"""

from .http_pool import HTTPConnectionPool, SimpleHTTPResponse
from .dns_resolver import DNSResolver, DNSRecord, DomainReputationReport
from .tls_fingerprint import TLSFingerprinter, TLSClientHello, CipherSuite

__all__ = [
    "HTTPConnectionPool",
    "SimpleHTTPResponse",
    "DNSResolver",
    "DNSRecord",
    "DomainReputationReport",
    "TLSFingerprinter",
    "TLSClientHello",
    "CipherSuite",
]
