"""
JobGuard Backend Service - Forensic Case Investigation & Law Enforcement Export Suite
Manages candidate fraud incident cases, chronological evidence timelines,
and formats official statutory complaints for Cyber Crime Portals (1930 / IC3 / ActionFraud).
"""

import time
import json
import hashlib
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class EvidenceArtifact:
    artifact_id: str
    artifact_type: str  # "email_screenshot", "bank_statement", "chat_log", "fake_offer_pdf"
    file_hash_sha256: str
    description: str
    uploaded_at: float = field(default_factory=time.time)


@dataclass
class ForensicCaseRecord:
    case_id: str
    victim_name: str
    victim_contact: str
    suspect_entity: str
    suspect_contact_channels: List[str]
    total_financial_loss_usd: float
    incident_timeline: List[Dict[str, Any]]
    evidence_artifacts: List[EvidenceArtifact]
    statutory_codes_violated: List[str]
    case_status: str = "OPEN_INVESTIGATION"


class ForensicCaseManager:
    """Enterprise case management and police complaint packager."""

    def __init__(self):
        self.cases: Dict[str, ForensicCaseRecord] = {}

    def create_case(
        self,
        victim_name: str,
        victim_contact: str,
        suspect_entity: str,
        suspect_contacts: List[str],
        financial_loss: float,
        timeline_events: List[Dict[str, Any]]
    ) -> ForensicCaseRecord:
        """Initialize formal forensic investigation case."""
        case_id = f"CASE-JG-{int(time.time()*1000)}-{hashlib.md5(victim_name.encode('utf-8')).hexdigest()[:6].upper()}"
        case = ForensicCaseRecord(
            case_id=case_id,
            victim_name=victim_name,
            victim_contact=victim_contact,
            suspect_entity=suspect_entity,
            suspect_contact_channels=suspect_contacts,
            total_financial_loss_usd=financial_loss,
            incident_timeline=timeline_events,
            evidence_artifacts=[],
            statutory_codes_violated=["IND-IT-66D", "USA-18USC-1343", "GBR-FRAUD-2006"]
        )
        self.cases[case_id] = case
        return case

    def export_formal_police_complaint(self, case_id: str) -> Dict[str, Any]:
        """Generate structured legal complaint document ready for law enforcement submission."""
        if case_id not in self.cases:
            raise KeyError(f"Case {case_id} not found")

        case = self.cases[case_id]
        return {
            "complaint_reference_id": case.case_id,
            "title": f"FORMAL CYBER FRAUD COMPLAINT REGARDING {case.suspect_entity.upper()}",
            "complainant_details": {
                "name": case.victim_name,
                "contact": case.victim_contact,
            },
            "accused_entity": {
                "claimed_identity": case.suspect_entity,
                "observed_channels": case.suspect_contact_channels,
            },
            "financial_damages": {
                "total_loss_usd": case.total_financial_loss_usd,
            },
            "statutory_provisions": case.statutory_codes_violated,
            "evidence_count": len(case.evidence_artifacts),
            "generated_timestamp": time.time(),
            "digital_signature_hash": hashlib.sha256(json.dumps(case.incident_timeline, sort_keys=True).encode("utf-8")).hexdigest()
        }
