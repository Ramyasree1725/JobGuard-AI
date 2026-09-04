"""
JobGuard Core NLP - Semantic Frame Catalog Database Part A
Contains FrameNet semantic frames, core frame elements, and lexical unit mappings.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class SemanticFrameData:
    frame_name: str
    frame_id: str
    definition: str
    core_elements: List[str]
    lexical_units: List[str]
    is_threat_salient: bool = False


SEMANTIC_FRAMES_A: List[SemanticFrameData] = [
    SemanticFrameData(
        frame_name="Commerce_pay_catalog_a",
        frame_id="FRM-CAT-A-0001",
        definition="A Buyer transmits Money to a Seller in exchange for Goods or Services.",
        core_elements=["Buyer", "Seller", "Money", "Goods"],
        lexical_units=["pay.v", "payment.n", "disburse.v", "remit.v", "fee.n", "charge.n"],
        is_threat_salient=True
    ),
    SemanticFrameData(
        frame_name="Prevarication_catalog_a",
        frame_id="FRM-CAT-A-0002",
        definition="A Speaker communicates information to an Addressee that is intentionally misleading.",
        core_elements=["Speaker", "Addressee", "Topic"],
        lexical_units=["lie.v", "deceive.v", "mislead.v", "impersonate.v", "scam.v"],
        is_threat_salient=True
    ),
    SemanticFrameData(
        frame_name="Hiring_catalog_a",
        frame_id="FRM-CAT-A-0003",
        definition="An Employer engages an Employee to perform tasks in exchange for Compensation.",
        core_elements=["Employer", "Employee", "Position", "Compensation"],
        lexical_units=["hire.v", "employ.v", "appoint.v", "recruit.v", "onboard.v"],
        is_threat_salient=False
    ),
    SemanticFrameData(
        frame_name="Extortion_catalog_a",
        frame_id="FRM-CAT-A-0004",
        definition="A Perpetrator compels a Victim to surrender Money through coercion or deception.",
        core_elements=["Perpetrator", "Victim", "Money"],
        lexical_units=["extort.v", "demand.v", "forfeit.v", "blacklist_threat.n"],
        is_threat_salient=True
    ),
    SemanticFrameData(
        frame_name="Being_obligated_catalog_a",
        frame_id="FRM-CAT-A-0005",
        definition="A Duty requires a Responsible_party to perform an Action under conditions.",
        core_elements=["Responsible_party", "Duty", "Condition"],
        lexical_units=["must.v", "require.v", "mandate.v", "obligation.n", "clause.n"],
        is_threat_salient=False
    )
]


class SemanticFrameManagerA:
    """Manager class for querying semantic frames in Part A."""

    def __init__(self):
        self.frames = {f.frame_name.lower(): f for f in SEMANTIC_FRAMES_A}

    def get_frame(self, name: str) -> Optional[SemanticFrameData]:
        return self.frames.get(name.strip().lower())
