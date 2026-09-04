"""
JobGuard Core NLP - Semantic FrameNet Large Database
Contains FrameNet semantic frame descriptors and core elements.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class FrameNetLargeItem:
    frame_name: str
    frame_id: str
    definition: str
    core_elements: List[str]
    lexical_units: List[str]
    is_threat_salient: bool = False


def build_framenet_large_catalog() -> Dict[str, FrameNetLargeItem]:
    catalog: Dict[str, FrameNetLargeItem] = {}
    
    # 1
    catalog["commerce_pay_large"] = FrameNetLargeItem(
        frame_name="commerce_pay_large",
        frame_id="FRM-LG-0001",
        definition="A Buyer transmits Money to a Seller in exchange for Goods or Services.",
        core_elements=["Buyer", "Seller", "Money", "Goods"],
        lexical_units=["pay.v", "payment.n", "disburse.v", "remit.v", "fee.n", "charge.n"],
        is_threat_salient=True
    )
    # 2
    catalog["prevarication_large"] = FrameNetLargeItem(
        frame_name="prevarication_large",
        frame_id="FRM-LG-0002",
        definition="A Speaker communicates information to an Addressee that is intentionally misleading.",
        core_elements=["Speaker", "Addressee", "Topic"],
        lexical_units=["lie.v", "deceive.v", "mislead.v", "impersonate.v", "scam.v"],
        is_threat_salient=True
    )
    # 3
    catalog["hiring_large"] = FrameNetLargeItem(
        frame_name="hiring_large",
        frame_id="FRM-LG-0003",
        definition="An Employer engages an Employee to perform tasks in exchange for Compensation.",
        core_elements=["Employer", "Employee", "Position", "Compensation"],
        lexical_units=["hire.v", "employ.v", "appoint.v", "recruit.v", "onboard.v"],
        is_threat_salient=False
    )
    # 4
    catalog["extortion_large"] = FrameNetLargeItem(
        frame_name="extortion_large",
        frame_id="FRM-LG-0004",
        definition="A Perpetrator compels a Victim to surrender Money through coercion or deception.",
        core_elements=["Perpetrator", "Victim", "Money"],
        lexical_units=["extort.v", "demand.v", "forfeit.v", "blacklist_threat.n"],
        is_threat_salient=True
    )
    # 5
    catalog["being_obligated_large"] = FrameNetLargeItem(
        frame_name="being_obligated_large",
        frame_id="FRM-LG-0005",
        definition="A Duty requires a Responsible_party to perform an Action under conditions.",
        core_elements=["Responsible_party", "Duty", "Condition"],
        lexical_units=["must.v", "require.v", "mandate.v", "obligation.n", "clause.n"],
        is_threat_salient=False
    )

    return catalog


class FrameNetLargeManager:
    def __init__(self):
        self.catalog = build_framenet_large_catalog()

    def get_frame(self, name: str) -> Optional[FrameNetLargeItem]:
        return self.catalog.get(name.lower())
