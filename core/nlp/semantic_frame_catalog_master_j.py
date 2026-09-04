"""
JobGuard Core NLP - Semantic Frame Catalog Master Volume J
Contains semantic frame definitions for simulated embassy interview appointments,
repatriation security deposits, and international wire tax withholding redirection.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class SemanticFrameMasterJ:
    frame_id: str
    frame_name: str
    core_thematic_roles: List[str]
    non_core_roles: List[str]
    lexical_triggers: List[str]
    adversarial_intent_probability: float
    description: str


class SemanticFrameCatalogMasterJ:
    """Master expanded catalog volume J of semantic frames for deception parsing."""

    def __init__(self):
        self.frames: Dict[str, SemanticFrameMasterJ] = {}
        self._seed_frames_j()

    def _seed_frames_j() -> None:
        """Register semantic frame structures."""

        frames_data = [
            (
                "FRAME-J-001",
                "Simulated_Embassy_Appointment_Fee",
                ["Consular_Impersonator", "Applicant_Worker", "Embassy_Location", "Booking_Fee_Amount"],
                ["Appointment_Window", "Visa_Category"],
                ["embassy booking fee", "consular interview appointment charge", "visa slot fee", "diplomatic mission deposit"],
                0.98,
                "A perpetrator charges an advance fee to an applicant under the false claim of securing a visa interview slot."
            ),
            (
                "FRAME-J-002",
                "Repatriation_Security_Deposit_Demand",
                ["Recruitment_Agency", "Foreign_Worker", "Repatriation_Guarantee_Amount", "Return_Airfare_Pretext"],
                ["Destination_State", "Refund_Conditions"],
                ["repatriation security deposit", "airfare guarantee fund", "mandatory return deposit", "worker return bond"],
                0.97,
                "An agency demands that an overseas worker pay upfront security deposits for future repatriation or return airfare."
            ),
            (
                "FRAME-J-003",
                "International_Tax_Withholding_Diversion",
                ["Tax_Collector_Impersonator", "Taxpayer_Candidate", "Withholding_Amount", "Overseas_Bank_Account"],
                ["Tax_Treaty_Pretext", "Payment_Deadline"],
                ["wire tax to overseas account", "international tax clearance fee", "foreign employment tax withholding", "consular tax deposit"],
                0.99,
                "A victim is instructed to wire funds to an offshore bank account under the guise of paying international employment taxes."
            )
        ]

        for f_id, name, cores, non_cores, triggers, adv_p, desc in frames_data:
            self.frames[name] = SemanticFrameMasterJ(
                frame_id=f_id,
                frame_name=name,
                core_thematic_roles=cores,
                non_core_roles=non_cores,
                lexical_triggers=triggers,
                adversarial_intent_probability=adv_p,
                description=desc
            )

    def get_frame(self, name: str) -> Optional[SemanticFrameMasterJ]:
        return self.frames.get(name)
