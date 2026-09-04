"""
JobGuard Core Network - Autonomous System (AS) & BGP Routing Telemetry
Analyzes Autonomous System Numbers (ASN), routing path anomalies, bulletproof hosting
identification, and suspicious network egress for recruitment fraud infrastructure.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import ipaddress


class ASNHostingCategory(Enum):
    ENTERPRISE_TIER_1 = "ENTERPRISE_TIER_1"
    COMMERCIAL_CLOUD = "COMMERCIAL_CLOUD"
    RESIDENTIAL_ISP = "RESIDENTIAL_ISP"
    BULLETPROOF_OFFSHORE = "BULLETPROOF_OFFSHORE"
    ANONYMIZING_VPN_TOR = "ANONYMIZING_VPN_TOR"
    UNKNOWN = "UNKNOWN"


@dataclass
class AutonomousSystemRecord:
    asn: int
    as_name: str
    country_code: str
    hosting_category: ASNHostingCategory
    reputation_score: float  # 0.0 (clean) to 1.0 (malicious haven)
    is_bulletproof: bool
    abuse_contact_email: str
    bgp_prefix_count: int
    registered_organization: str


@dataclass
class ASNAuditReport:
    query_ip: str
    matched_asn: Optional[AutonomousSystemRecord]
    risk_score: float
    risk_factors: List[str]
    is_known_fraud_host: bool
    remediation_recommendation: str


class AutonomousSystemAnalyzer:
    """Telemetry analyzer for AS numbers, BGP prefixes, and hosting infrastructure reputation."""

    def __init__(self):
        self.asn_database: Dict[int, AutonomousSystemRecord] = {}
        self.ip_prefix_table: List[Tuple[ipaddress.IPv4Network, int]] = []
        self._initialize_asn_database()

    def _initialize_asn_database(self) -> None:
        """Populate ASN threat intelligence profiles."""

        # Legitimate Tier 1 and Cloud Providers
        self._register_asn(AutonomousSystemRecord(
            asn=15169,
            as_name="GOOGLE",
            country_code="US",
            hosting_category=ASNHostingCategory.ENTERPRISE_TIER_1,
            reputation_score=0.05,
            is_bulletproof=False,
            abuse_contact_email="network-abuse@google.com",
            bgp_prefix_count=1200,
            registered_organization="Google LLC"
        ), ["8.8.8.0/24", "172.217.0.0/16", "142.250.0.0/15"])

        self._register_asn(AutonomousSystemRecord(
            asn=8075,
            as_name="MICROSOFT-CORP",
            country_code="US",
            hosting_category=ASNHostingCategory.ENTERPRISE_TIER_1,
            reputation_score=0.05,
            is_bulletproof=False,
            abuse_contact_email="abuse@microsoft.com",
            bgp_prefix_count=2100,
            registered_organization="Microsoft Corporation"
        ), ["20.0.0.0/11", "40.74.0.0/15", "52.96.0.0/12"])

        self._register_asn(AutonomousSystemRecord(
            asn=16509,
            as_name="AMAZON-02",
            country_code="US",
            hosting_category=ASNHostingCategory.COMMERCIAL_CLOUD,
            reputation_score=0.15,
            is_bulletproof=False,
            abuse_contact_email="trustandsafety@support.aws.com",
            bgp_prefix_count=3500,
            registered_organization="Amazon.com, Inc."
        ), ["3.0.0.0/9", "54.0.0.0/8"])

        # High-Risk / Bulletproof Hosting ASNs
        self._register_asn(AutonomousSystemRecord(
            asn=48031,
            as_name="CHINANET-IDC",
            country_code="CN",
            hosting_category=ASNHostingCategory.BULLETPROOF_OFFSHORE,
            reputation_score=0.88,
            is_bulletproof=True,
            abuse_contact_email="anti-spam@chinanet.cn",
            bgp_prefix_count=45,
            registered_organization="Hangzhou Offshore Media Ltd"
        ), ["103.224.182.0/24", "185.156.72.0/24"])

        self._register_asn(AutonomousSystemRecord(
            asn=51852,
            as_name="PRIVATE-LAYER-SWISS",
            country_code="CH",
            hosting_category=ASNHostingCategory.BULLETPROOF_OFFSHORE,
            reputation_score=0.92,
            is_bulletproof=True,
            abuse_contact_email="abuse@privatelayer.biz",
            bgp_prefix_count=18,
            registered_organization="Private Layer Cyber Ltd"
        ), ["185.220.101.0/24", "194.26.29.0/24"])

        self._register_asn(AutonomousSystemRecord(
            asn=208323,
            as_name="CZ-ANON-VPN",
            country_code="CZ",
            hosting_category=ASNHostingCategory.ANONYMIZING_VPN_TOR,
            reputation_score=0.85,
            is_bulletproof=False,
            abuse_contact_email="abuse@cz-exit.net",
            bgp_prefix_count=12,
            registered_organization="Czech Anonymous Transit Relay"
        ), ["185.100.86.0/24"])

    def _register_asn(self, record: AutonomousSystemRecord, cidrs: List[str]) -> None:
        self.asn_database[record.asn] = record
        for cidr in cidrs:
            try:
                net = ipaddress.IPv4Network(cidr, strict=False)
                self.ip_prefix_table.append((net, record.asn))
            except ValueError:
                pass

    def audit_ip_infrastructure(self, ip_str: str) -> ASNAuditReport:
        """Inspects an IP address against BGP prefix routing tables and ASN reputation metrics."""
        try:
            target_ip = ipaddress.IPv4Address(ip_str.strip())
        except ValueError:
            return ASNAuditReport(
                query_ip=ip_str,
                matched_asn=None,
                risk_score=50.0,
                risk_factors=["Invalid or non-routable IPv4 address formatting"],
                is_known_fraud_host=False,
                remediation_recommendation="Verify network origin with valid public IP address."
            )

        matched_asn_id: Optional[int] = None
        for network, asn in self.ip_prefix_table:
            if target_ip in network:
                matched_asn_id = asn
                break

        if not matched_asn_id or matched_asn_id not in self.asn_database:
            return ASNAuditReport(
                query_ip=ip_str,
                matched_asn=None,
                risk_score=20.0,
                risk_factors=["Uncataloged ISP network (standard residential/commercial)"],
                is_known_fraud_host=False,
                remediation_recommendation="Standard domain origin. Monitor for application-level anomalies."
            )

        asn_record = self.asn_database[matched_asn_id]
        risk_factors: List[str] = []
        base_risk = asn_record.reputation_score * 100.0

        if asn_record.is_bulletproof:
            risk_factors.append(f"Host resides in known bulletproof ASN {asn_record.asn} ({asn_record.as_name}).")
        if asn_record.hosting_category == ASNHostingCategory.ANONYMIZING_VPN_TOR:
            risk_factors.append("Host operates as an anonymizing proxy, VPN node, or TOR exit gateway.")
        if asn_record.country_code in ["RU", "CN", "NG", "IR", "KP"]:
            risk_factors.append(f"Autonomous system jurisdiction ({asn_record.country_code}) has elevated cross-border fraud incidence.")

        return ASNAuditReport(
            query_ip=ip_str,
            matched_asn=asn_record,
            risk_score=min(100.0, max(0.0, base_risk)),
            risk_factors=risk_factors if risk_factors else ["Clean enterprise/cloud transit infrastructure."],
            is_known_fraud_host=asn_record.is_bulletproof or asn_record.reputation_score > 0.80,
            remediation_recommendation="Block recruitment communication from bulletproof or anonymized infrastructure." if asn_record.is_bulletproof else "Infrastructure verified."
        )
