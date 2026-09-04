"""
JobGuard Core Vision - PDF/Document Metadata Forensic Extractor
Extracts and analyzes PDF Info dictionaries, XMP metadata streams, creation toolchains,
modification history, and author provenance to flag forged employment offers.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import datetime
import re


@dataclass
class DocumentMetadataProfile:
    file_name: str
    file_size_bytes: int
    pdf_version: str
    creator_tool: Optional[str]
    producer_app: Optional[str]
    creation_date: Optional[datetime.datetime]
    modification_date: Optional[datetime.datetime]
    author_name: Optional[str]
    title: Optional[str]
    is_linearized_fast_web: bool
    has_incremental_updates: bool
    raw_metadata_dict: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetadataForensicAudit:
    metadata_profile: DocumentMetadataProfile
    is_generated_by_consumer_tool: bool
    is_modified_post_creation: bool
    suspicious_toolchain_detected: bool
    risk_score: float  # 0 to 100
    forensic_red_flags: List[str]
    provenance_verdict: str


class MetadataForensicExtractor:
    """Dissects PDF metadata streams to identify consumer editing apps and provenance tampering."""

    CONSUMER_EDITING_TOOLS: Set[str] = {
        "canva", "ilovepdf", "smallpdf", "pdfescape", "sejda", "photoshop",
        "gimp", "paint.net", "wondershare", "pdf24", "libreoffice", "foxit phantom"
    }

    ENTERPRISE_HR_SYSTEM_PRODUCERS: Set[str] = {
        "docusign", "adobesign", "workday", "greenhouse", "oracle taleo",
        "sap successfactors", "pandadoc", "hellosign", "adobe pdf library", "quartz pdfcontext"
    }

    def __init__(self):
        pass

    def audit_metadata(
        self,
        profile: DocumentMetadataProfile,
        claimed_company: Optional[str] = None
    ) -> MetadataForensicAudit:
        """Evaluates document authoring toolchain and creation timeline consistency."""
        red_flags: List[str] = []
        risk_score = 0.0

        creator = (profile.creator_tool or "").lower()
        producer = (profile.producer_app or "").lower()
        author = (profile.author_name or "").lower()

        # Check 1: Free consumer web editing tools
        is_consumer = False
        for tool in self.CONSUMER_EDITING_TOOLS:
            if tool in creator or tool in producer:
                is_consumer = True
                red_flags.append(f"Document produced using consumer web utility '{tool}'. Authentic corporate offers originate from enterprise ATS / DocuSign pipelines.")
                risk_score += 45.0
                break

        # Check 2: Graphic design software (Photoshop) used for legal text document
        if "photoshop" in creator or "photoshop" in producer:
            red_flags.append("CRITICAL: Legal offer letter generated via Adobe Photoshop graphic editor rather than PDF document compiler.")
            risk_score += 65.0

        # Check 3: Author mismatch with claimed company
        if claimed_company and author:
            if claimed_company.lower() not in author and author not in ("administrator", "hr", "talent", ""):
                # Check if author name is an individual personal username (e.g. 'User-PC', 'John-Laptop')
                if any(w in author for w in ["pc", "laptop", "desktop", "user", "admin", "owner", "asus", "dell", "hp"]):
                    red_flags.append(f"Author metadata indicates personal home computer identity ('{profile.author_name}') rather than enterprise organization.")
                    risk_score += 25.0

        # Check 4: Modification timestamp discrepancy
        is_modified = False
        if profile.creation_date and profile.modification_date:
            delta = profile.modification_date - profile.creation_date
            if delta.total_seconds() > 3600 * 24 * 30:  # Modified months after creation
                is_modified = True
                red_flags.append(f"Document modified {delta.days} days after initial creation date; indicates reused and altered template.")
                risk_score += 30.0

        # Verdict assignment
        if risk_score >= 60.0:
            verdict = "CRITICAL: High probability of template forgery or consumer editing manipulation."
        elif risk_score >= 25.0:
            verdict = "WARNING: Non-standard document creation metadata. Manual review advised."
        else:
            verdict = "VERIFIED: Metadata aligns with standard enterprise authoring toolchain."

        return MetadataForensicAudit(
            metadata_profile=profile,
            is_generated_by_consumer_tool=is_consumer,
            is_modified_post_creation=is_modified,
            suspicious_toolchain_detected=(risk_score > 30.0),
            risk_score=min(100.0, max(0.0, risk_score)),
            forensic_red_flags=red_flags if red_flags else ["Clean PDF metadata conforming to enterprise document standards."],
            provenance_verdict=verdict
        )
