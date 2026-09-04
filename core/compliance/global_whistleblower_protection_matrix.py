"""
JobGuard Core Compliance - Global Whistleblower & Fraud Informant Protection Matrix
Provides statutory protections, anonymity safeguards, anti-retaliation legal remedies,
and bounty award frameworks (SEC Whistleblower, False Claims Act) for fraud informants.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class InformantProtectionTier(Enum):
    TIER_1_STANDARD_ANONYMITY = "TIER_1_STANDARD_ANONYMITY"
    TIER_2_STATUTORY_REMEDY = "TIER_2_STATUTORY_REMEDY"
    TIER_3_MONETARY_BOUNTY_ELIGIBLE = "TIER_3_MONETARY_BOUNTY_ELIGIBLE"
    TIER_4_FULL_IMMUNITY_AND_SHIELD = "TIER_4_FULL_IMMUNITY_AND_SHIELD"


@dataclass
class WhistleblowerFrameworkRecord:
    framework_id: str
    jurisdiction: str
    governing_statute: str
    administering_agency: str
    bounty_percentage_range: Tuple[float, float]
    anti_retaliation_remedies: List[str]
    confidentiality_guarantee: str
    applicable_fraud_types: List[str]


class GlobalWhistleblowerProtectionMatrix:
    """Master database of whistleblower protections and bounty reward frameworks."""

    def __init__(self):
        self.frameworks: Dict[str, WhistleblowerFrameworkRecord] = {}
        self._initialize_frameworks()

    def _initialize_frameworks(self) -> None:
        """Register whistleblower protection programs across international jurisdictions."""

        programs = [
            (
                "WB-US-SEC",
                "US_FEDERAL",
                "Dodd-Frank Wall Street Reform Act § 922 (15 U.S.C. § 78u-6)",
                "U.S. Securities and Exchange Commission (SEC) Office of the Whistleblower",
                (10.0, 30.0),
                [
                    "Reinstatement with senior status",
                    "Double back-pay with compounded interest",
                    "Coverage of all legal and attorney fees"
                ],
                "Strict statutory confidentiality; whistleblowers may report anonymously via legal counsel.",
                [
                    "Public company recruitment impersonation fraud",
                    "Cryptocurrency investment scams masquerading as employment",
                    "False statements in securities filings regarding workforce"
                ]
            ),
            (
                "WB-US-CFTC",
                "US_FEDERAL",
                "Commodity Exchange Act § 23 (7 U.S.C. § 26)",
                "Commodity Futures Trading Commission (CFTC) Whistleblower Office",
                (10.0, 30.0),
                [
                    "Reinstatement and compensatory damages",
                    "Anti-retaliation federal civil right of action"
                ],
                "Anonymous reporting permitted through accredited legal representation.",
                [
                    "Crypto task rating escrow schemes",
                    "Commodity futures and forex work-from-home scams"
                ]
            ),
            (
                "WB-US-FCA",
                "US_FEDERAL",
                "Federal False Claims Act (31 U.S.C. § 3730 - Qui Tam Provisions)",
                "United States Department of Justice (DOJ)",
                (15.0, 30.0),
                [
                    "Two times back pay plus special damages",
                    "Mandatory reinstatement",
                    "Civil penalty recovery of up to $27,000 per false claim"
                ],
                "Filed under seal with the Federal District Court for government review.",
                [
                    "Fraudulent recruitment under government defense contracts",
                    "Fake job staffing under federally funded research grants"
                ]
            ),
            (
                "WB-EU-DIR",
                "EUROPEAN_UNION",
                "EU Directive 2019/1937 on the Protection of Persons Who Report Breaches of Union Law",
                "National Competent Authorities of EU Member States",
                (0.0, 0.0),
                [
                    "Exemption from liability for breach of non-disclosure agreements",
                    "Reversal of burden of proof in retaliation lawsuits",
                    "Comprehensive legal aid and psychological support"
                ],
                "Mandatory secure and confidential reporting channels across public and private sectors.",
                [
                    "Deceptive cross-border worker recruitment and PII harvesting",
                    "Violations of EU labor mobility directives and wage fraud"
                ]
            ),
            (
                "WB-UK-PIDA",
                "UNITED_KINGDOM",
                "Public Interest Disclosure Act 1998 (PIDA) & Employment Rights Act 1996",
                "UK Employment Tribunals / Department for Business and Trade",
                (0.0, 0.0),
                [
                    "Uncapped compensatory damages for wrongful dismissal or detriment",
                    "Interim relief orders to preserve employment pending trial"
                ],
                "Protected disclosures can be made directly to prescribed persons or regulators.",
                [
                    "Unlawful employment agency fee charging and sham contracting",
                    "Systematic recruitment fraud in violation of UK Fraud Act 2006"
                ]
            )
        ]

        for f_id, jur, stat, agency, bounty, remedies, conf, f_types in programs:
            record = WhistleblowerFrameworkRecord(
                framework_id=f_id,
                jurisdiction=jur,
                governing_statute=stat,
                administering_agency=agency,
                bounty_percentage_range=bounty,
                anti_retaliation_remedies=remedies,
                confidentiality_guarantee=conf,
                applicable_fraud_types=f_types
            )
            self.frameworks[f_id] = record

    def get_framework(self, framework_id: str) -> Optional[WhistleblowerFrameworkRecord]:
        return self.frameworks.get(framework_id)
