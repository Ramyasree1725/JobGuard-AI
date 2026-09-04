"""
JobGuard Core NLP - Semantic Frame Catalog Master Volume D
Contains semantic frame definitions for foreign visa fee extraction,
package mule reshipping recruitment, and malicious coding repository execution.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class SemanticFrameMasterD:
    frame_id: str
    frame_name: str
    core_thematic_roles: List[str]
    non_core_roles: List[str]
    lexical_triggers: List[str]
    adversarial_intent_probability: float
    description: str


class SemanticFrameCatalogMasterD:
    """Master expanded catalog volume D of semantic frames for deception parsing."""

    def __init__(self):
        self.frames: Dict[str, SemanticFrameMasterD] = {}
        self._seed_frames_d()

    def _seed_frames_d(self) -> None:
        """Register semantic frame structures."""

        frames_data = [
            (
                "FRAME-D-001",
                "Foreign_Visa_Advance_Fee_Trap",
                ["Agent_Impersonator", "Foreign_Worker", "Visa_Type", "Processing_Fee_Amount"],
                ["Destination_Country", "Embassy_Pretext"],
                ["visa processing fee", "work permit deposit", "consular clearance charge", "embassy medical fee"],
                0.99,
                "A perpetrator demands advance funds from an international applicant under the pretext of securing an overseas work visa."
            ),
            (
                "FRAME-D-002",
                "Package_Mule_Reshipping_Recruitment",
                ["Handler", "Unwitting_Mule", "Package_Type", "Reship_Destination"],
                ["Promised_Per_Package_Pay", "Merchandise_Value"],
                ["package inspector", "package forwarding assistant", "reship parcels", "merchandise quality inspector"],
                0.97,
                "A scam syndicate recruits a victim to receive and reship stolen goods purchased with compromised payment cards."
            ),
            (
                "FRAME-D-003",
                "Malicious_Code_Repository_Lure",
                ["Threat_Actor", "Developer_Candidate", "Repository_URL", "Execution_Command"],
                ["Target_Platform", "Payload_Type"],
                ["clone assessment repo", "run npm install to test", "take-home coding challenge zip", "cargo build test suite"],
                0.95,
                "A software engineering candidate is instructed to clone and execute a repository containing backdoored build scripts."
            )
        ]

        for f_id, name, cores, non_cores, triggers, adv_p, desc in frames_data:
            self.frames[name] = SemanticFrameMasterD(
                frame_id=f_id,
                frame_name=name,
                core_thematic_roles=cores,
                non_core_roles=non_cores,
                lexical_triggers=triggers,
                adversarial_intent_probability=adv_p,
                description=desc
            )

    def get_frame(self, name: str) -> Optional[SemanticFrameMasterD]:
        return self.frames.get(name)
