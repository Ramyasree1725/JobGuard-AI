"""
JobGuard Core Security - Statutory IoC Threat Matrix Expanded
Provides structured database of Indicators of Compromise (IoCs) cross-linked
to federal criminal statutes, civil causes of action, and automated firewall block rules.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class StatutoryIoCEntry:
    ioc_id: str
    ioc_type: str  # 'IP_ADDRESS', 'DOMAIN', 'EMAIL', 'WALLET_ADDRESS', 'FILE_HASH_SHA256'
    ioc_value: str
    associated_scam_campaign: str
    statute_violation_code: str
    remediation_firewall_rule: str
    confidence_percentage: float
    reported_loss_aggregate_usd: float


class StatutoryIoCThreatMatrixExpanded:
    """Master expanded repository of Indicators of Compromise cross-linked to legal statutes."""

    def __init__(self):
        self.iocs: Dict[str, StatutoryIoCEntry] = {}
        self._seed_iocs()

    def _seed_iocs(self) -> None:
        """Register extensive IoC records."""

        records = [
            ("IOC-EXP-001", "DOMAIN", "careers-google-verify.com", "Google Impersonation Ring", "18 U.S.C. § 1343", "DNS_BLOCK_SINKHOLE", 99.5, 450000.0),
            ("IOC-EXP-002", "DOMAIN", "microsoft-recruiting-desk.net", "Microsoft Impersonation Ring", "18 U.S.C. § 1343", "DNS_BLOCK_SINKHOLE", 98.9, 620000.0),
            ("IOC-EXP-003", "IP_ADDRESS", "185.156.72.44", "SilverPhish Command Infrastructure", "18 U.S.C. § 1030", "BGP_BLACKHOLE_DROP", 97.8, 1200000.0),
            ("IOC-EXP-004", "WALLET_ADDRESS", "0x71C8366420A0926793fe839C7752eD78297745E2", "CryptoTask Drainer Wallet", "18 U.S.C. § 1956", "CRYPTO_COMPLIANCE_FREEZE", 99.9, 8500000.0),
            ("IOC-EXP-005", "WALLET_ADDRESS", "TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE", "USDT Task Recharge Escrow", "18 U.S.C. § 1956", "CRYPTO_COMPLIANCE_FREEZE", 99.8, 3400000.0),
            ("IOC-EXP-006", "FILE_HASH_SHA256", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "Counterfeit Check PDF Template", "18 U.S.C. § 1344", "EMAIL_GATEWAY_QUARANTINE", 99.0, 2100000.0),
            ("IOC-EXP-007", "EMAIL", "recruitment@google-careers-portal.org", "Spoofed Recruiter Mailbox", "18 U.S.C. § 1343", "SMTP_ENVELOPE_REJECT", 98.5, 180000.0)
        ]

        for ioc_id, itype, val, camp, stat, rem, conf, loss in records:
            self.iocs[val.lower()] = StatutoryIoCEntry(
                ioc_id=ioc_id,
                ioc_type=itype,
                ioc_value=val,
                associated_scam_campaign=camp,
                statute_violation_code=stat,
                remediation_firewall_rule=rem,
                confidence_percentage=conf,
                reported_loss_aggregate_usd=loss
            )

    def check_ioc(self, value: str) -> Optional[StatutoryIoCEntry]:
        return self.iocs.get(value.lower().strip())
