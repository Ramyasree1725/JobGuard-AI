"""
JobGuard Core NLP - Semantic Frame Catalog Master Volume F
Contains semantic frame definitions for cryptocurrency commission task rating,
unsolicited job offers without evaluation, and artificial deadline pressure.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class SemanticFrameMasterF:
    frame_id: str
    frame_name: str
    core_thematic_roles: List[str]
    non_core_roles: List[str]
    lexical_triggers: List[str]
    adversarial_intent_probability: float
    description: str


class SemanticFrameCatalogMasterF:
    """Master expanded catalog volume F of semantic frames for deception parsing."""

    def __init__(self):
        self.frames: Dict[str, SemanticFrameMasterF] = {}
        self._seed_frames_f()

    def _seed_frames_f(self) -> None:
        """Register semantic frame structures."""

        frames_data = [
            (
                "FRAME-F-001",
                "Cryptocurrency_Recharge_Commission_Scheme",
                ["Platform_Operator", "Worker_Victim", "Commission_Rate", "Negative_Balance", "Recharge_Amount"],
                ["Cryptocurrency_Wallet", "VIP_Level"],
                ["recharge usdt", "negative balance reset", "daily commission unlock", "level 1 vip deposit", "crypto task rating"],
                0.99,
                "A victim is tricked into depositing cryptocurrency to unlock simulated e-commerce rating commissions."
            ),
            (
                "FRAME-F-002",
                "Instant_Selection_Without_Interview",
                ["Purported_Employer", "Job_Seeker", "Assigned_Role", "Promised_Compensation"],
                ["Resume_Source", "Start_Date"],
                ["selected without interview", "hired immediately based on resume", "no interview needed", "instant job offer"],
                0.94,
                "A candidate receives an instant job offer with zero formal video or in-person technical evaluation."
            ),
            (
                "FRAME-F-003",
                "Psychological_Exploding_Offer_Coercion",
                ["Coercer", "Victim_Candidate", "Expiration_Window", "Threatened_Consequence"],
                ["Urgency_Tone", "Contact_Channel"],
                ["offer expires in 2 hours", "sign immediately today", "limited slots first come first serve", "urgent response required"],
                0.88,
                "A perpetrator imposes an artificially short contract signing deadline to prevent independent verification."
            )
        ]

        for f_id, name, cores, non_cores, triggers, adv_p, desc in frames_data:
            self.frames[name] = SemanticFrameMasterF(
                frame_id=f_id,
                frame_name=name,
                core_thematic_roles=cores,
                non_core_roles=non_cores,
                lexical_triggers=triggers,
                adversarial_intent_probability=adv_p,
                description=desc
            )

    def get_frame(self, name: str) -> Optional[SemanticFrameMasterF]:
        return self.frames.get(name)
