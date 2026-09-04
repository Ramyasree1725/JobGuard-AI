"""
JobGuard Core NLP - Semantic Frame Catalog Master Volume C
Contains semantic frames and argument structure definitions for candidate identity extraction,
salary negotiation deception, and counterfeit corporate letterhead verification.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class SemanticFrameMasterC:
    frame_id: str
    frame_name: str
    core_thematic_roles: List[str]
    non_core_roles: List[str]
    lexical_triggers: List[str]
    adversarial_intent_probability: float
    description: str


class SemanticFrameCatalogMasterC:
    """Master expanded catalog volume C of semantic frames for deception parsing."""

    def __init__(self):
        self.frames: Dict[str, SemanticFrameMasterC] = {}
        self._seed_frames_c()

    def _seed_frames_c(self) -> None:
        """Register semantic frame structures."""

        frames_data = [
            (
                "FRAME-C-001",
                "Premature_PII_Solicitation",
                ["Collector", "Target_Individual", "Identity_Attribute", "Transmission_Protocol"],
                ["Stated_Pretext", "Encryption_Status"],
                ["social security number", "ssn", "passport scan", "driver license copy", "banking direct deposit login"],
                0.97,
                "An entity requests sensitive national identity or online banking access prior to formal evaluation."
            ),
            (
                "FRAME-C-002",
                "Hyper_Inflated_Compensation_Lure",
                ["Promisor", "Candidate", "Promised_Rate", "Work_Requirement"],
                ["Payment_Frequency", "Flexibility_Claim"],
                ["$50/hr data entry", "$300 daily", "typing jobs from home", "no experience needed high pay"],
                0.92,
                "A job listing promises compensation drastically exceeding standard market distributions for entry-level tasks."
            ),
            (
                "FRAME-C-003",
                "Anonymous_Messaging_Redirection",
                ["Recruiter", "Candidate", "Origin_Platform", "Destination_Platform", "Contact_Handle"],
                ["Urgency_Marker"],
                ["message on telegram", "download whatsapp", "chat on signal", "contact hiring manager directly"],
                0.85,
                "A recruiter diverts communication from a formal corporate board to a private messaging application."
            )
        ]

        for f_id, name, cores, non_cores, triggers, adv_p, desc in frames_data:
            self.frames[name] = SemanticFrameMasterC(
                frame_id=f_id,
                frame_name=name,
                core_thematic_roles=cores,
                non_core_roles=non_cores,
                lexical_triggers=triggers,
                adversarial_intent_probability=adv_p,
                description=desc
            )

    def get_frame(self, name: str) -> Optional[SemanticFrameMasterC]:
        return self.frames.get(name)
