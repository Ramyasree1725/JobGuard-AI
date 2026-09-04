"""
JobGuard Core NLP - Semantic Frame Catalog Master Volume G
Contains semantic frame definitions for fake executive appointment letters,
simulated performance bonds, and international customs clearance fees.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class SemanticFrameMasterG:
    frame_id: str
    frame_name: str
    core_thematic_roles: List[str]
    non_core_roles: List[str]
    lexical_triggers: List[str]
    adversarial_intent_probability: float
    description: str


class SemanticFrameCatalogMasterG:
    """Master expanded catalog volume G of semantic frames for deception parsing."""

    def __init__(self):
        self.frames: Dict[str, SemanticFrameMasterG] = {}
        self._seed_frames_g()

    def _seed_frames_g(self) -> None:
        """Register semantic frame structures."""

        frames_data = [
            (
                "FRAME-G-001",
                "Simulated_Performance_Bond_Demand",
                ["Bond_Issuer", "Obligee_Candidate", "Bond_Amount", "Purported_Guarantee"],
                ["Payment_Gateway", "Release_Condition"],
                ["performance bond", "security deposit guarantee", "refundable indemnity bond", "employment surety"],
                0.98,
                "A perpetrator demands that a candidate post a financial surety bond prior to starting a remote engagement."
            ),
            (
                "FRAME-G-002",
                "Customs_Clearance_Fee_Shifting",
                ["Carrier_Impersonator", "Recipient_Employee", "Package_Declaration", "Clearance_Fee"],
                ["Customs_Border", "Duty_Pretext"],
                ["customs duty fee", "package clearance charge", "border tax deposit", "courier customs release"],
                0.97,
                "A victim is told that corporate equipment is held at customs and must pay personal funds to release the shipment."
            ),
            (
                "FRAME-G-003",
                "Fake_Executive_Authority_Invocation",
                ["Named_Executive", "Purported_Title", "Authority_Claim", "Subordinate_Directive"],
                ["Corporate_Entity", "Urgency_Modifier"],
                ["by order of the ceo", "executive board decision", "signed by chief talent officer", "approved by managing director"],
                0.89,
                "A scam communication invokes high-ranking corporate executives to fabricate organizational authority and suppress questioning."
            )
        ]

        for f_id, name, cores, non_cores, triggers, adv_p, desc in frames_data:
            self.frames[name] = SemanticFrameMasterG(
                frame_id=f_id,
                frame_name=name,
                core_thematic_roles=cores,
                non_core_roles=non_cores,
                lexical_triggers=triggers,
                adversarial_intent_probability=adv_p,
                description=desc
            )

    def get_frame(self, name: str) -> Optional[SemanticFrameMasterG]:
        return self.frames.get(name)
