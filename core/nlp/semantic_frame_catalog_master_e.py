"""
JobGuard Core NLP - Semantic Frame Catalog Master Volume E
Contains semantic frame structures for equipment delivery check disbursement,
stolen credit card package reshipping, and fake corporate notary certification.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class SemanticFrameMasterE:
    frame_id: str
    frame_name: str
    core_thematic_roles: List[str]
    non_core_roles: List[str]
    lexical_triggers: List[str]
    adversarial_intent_probability: float
    description: str


class SemanticFrameCatalogMasterE:
    """Master expanded catalog volume E of semantic frames for deception parsing."""

    def __init__(self):
        self.frames: Dict[str, SemanticFrameMasterE] = {}
        self._seed_frames_e()

    def _seed_frames_e() -> None:
        """Register semantic frame structures."""

        frames_data = [
            (
                "FRAME-E-001",
                "Equipment_Check_Kickback_Disbursement",
                ["Disburser", "Recipient_Employee", "Check_Value", "Kickback_Amount", "Shell_Vendor"],
                ["Transmission_Method", "Reimbursement_Timeline"],
                ["home office check", "equipment allowance", "vendor wire", "surplus funds return", "approved supplier"],
                0.99,
                "A perpetrator sends a counterfeit check to an employee, requiring them to transfer surplus funds to a shell vendor."
            ),
            (
                "FRAME-E-002",
                "Mule_Package_Re_Shipping_Arrangement",
                ["Syndicate_Handler", "Reshipper_Worker", "Parcel_Item", "Delivery_Destination"],
                ["Compensation_Rate", "Origin_Vendor"],
                ["re-ship package", "package forwarding assistant", "merchandise inspector", "forward parcels", "quality review from home"],
                0.97,
                "A victim is contracted to receive stolen goods and re-ship them to international addresses."
            ),
            (
                "FRAME-E-003",
                "Fraudulent_Visa_Clearance_Solicitation",
                ["Immigration_Impersonator", "Foreign_Applicant", "Visa_Type", "Advance_Fee"],
                ["Embassy_Claim", "Urgency_Deadline"],
                ["visa processing fee", "work permit clearance", "embassy medical charge", "consular deposit"],
                0.98,
                "A scammer demands advance visa processing fees from international job applicants."
            )
        ]

        for f_id, name, cores, non_cores, triggers, adv_p, desc in frames_data:
            self.frames[name] = SemanticFrameMasterE(
                frame_id=f_id,
                frame_name=name,
                core_thematic_roles=cores,
                non_core_roles=non_cores,
                lexical_triggers=triggers,
                adversarial_intent_probability=adv_p,
                description=desc
            )

    def get_frame(self, name: str) -> Optional[SemanticFrameMasterE]:
        return self.frames.get(name)
