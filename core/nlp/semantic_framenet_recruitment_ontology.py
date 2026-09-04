"""
JobGuard Core NLP - Semantic FrameNet Recruitment Ontology & Valence Engine
Defines rich FrameNet-style semantic valence patterns, frame-to-frame relations
(Inheritance, Subframe, Causation), and lexical trigger mappings for recruitment deception.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class FrameElement:
    element_name: str
    semantic_type: str  # 'SENTIENT', 'MONETARY', 'ARTIFACT', 'ACTION'
    is_core: bool
    description: str


@dataclass
class FrameNetOntologyEntry:
    frame_id: str
    frame_name: str
    parent_frames: List[str]
    sub_frames: List[str]
    frame_elements: List[FrameElement]
    lexical_triggers: List[str]
    threat_severity_weight: float


class SemanticFrameNetRecruitmentOntology:
    """FrameNet ontological representation of hiring deception structures."""

    def __init__(self):
        self.frames: Dict[str, FrameNetOntologyEntry] = {}
        self._initialize_framenet_ontology()

    def _initialize_framenet_ontology(self) -> None:
        """Register FrameNet structural hierarchies."""

        self.frames["Scam_Commercial_Interaction"] = FrameNetOntologyEntry(
            frame_id="FRAME-001",
            frame_name="Scam_Commercial_Interaction",
            parent_frames=["Commercial_Transaction"],
            sub_frames=["Advance_Fee_Extortion", "Counterfeit_Disbursement"],
            frame_elements=[
                FrameElement("Perpetrator", "SENTIENT", True, "The fraudulent entity posing as employer or recruiter."),
                FrameElement("Victim", "SENTIENT", True, "The job applicant targeted by the predatory scheme."),
                FrameElement("Money", "MONETARY", True, "The financial sum demanded or disbursed."),
                FrameElement("Pretext", "ACTION", False, "The stated reason (equipment, registration, background).")
            ],
            lexical_triggers=["pay", "charge", "deposit", "wire", "fee", "cost", "check"],
            threat_severity_weight=0.85
        )

        self.frames["Advance_Fee_Extortion"] = FrameNetOntologyEntry(
            frame_id="FRAME-002",
            frame_name="Advance_Fee_Extortion",
            parent_frames=["Scam_Commercial_Interaction"],
            sub_frames=[],
            frame_elements=[
                FrameElement("Perpetrator", "SENTIENT", True, "The scam recruiter."),
                FrameElement("Victim", "SENTIENT", True, "The applicant."),
                FrameElement("Demanded_Fee", "MONETARY", True, "The advance payment demanded before work commences.")
            ],
            lexical_triggers=["registration fee", "processing deposit", "onboarding cost", "background check fee"],
            threat_severity_weight=0.95
        )

        self.frames["Legitimate_Employment_Offer"] = FrameNetOntologyEntry(
            frame_id="FRAME-003",
            frame_name="Legitimate_Employment_Offer",
            parent_frames=["Contract_Formation"],
            sub_frames=[],
            frame_elements=[
                FrameElement("Employer", "SENTIENT", True, "The authentic hiring corporation."),
                FrameElement("Employee", "SENTIENT", True, "The candidate accepting the position."),
                FrameElement("Compensation", "MONETARY", True, "Agreed wage or salary rate."),
                FrameElement("Position_Title", "ARTIFACT", True, "The formal occupational role.")
            ],
            lexical_triggers=["annual salary", "hourly wage", "health benefits", "401k", "paid time off"],
            threat_severity_weight=0.05
        )

    def get_frame(self, frame_name: str) -> Optional[FrameNetOntologyEntry]:
        return self.frames.get(frame_name)
