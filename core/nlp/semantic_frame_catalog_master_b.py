"""
JobGuard Core NLP - Semantic Frame Catalog Master Volume B
Contains detailed semantic frame structures, lexical unit triggers, and thematic role
bindings for modeling recruitment deception, fake checks, and fee demands.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class SemanticFrameMasterB:
    frame_id: str
    frame_name: str
    core_thematic_roles: List[str]
    non_core_roles: List[str]
    lexical_triggers: List[str]
    adversarial_intent_probability: float
    description: str


class SemanticFrameCatalogMasterB:
    """Master expanded catalog volume B of semantic frames for deception parsing."""

    def __init__(self):
        self.frames: Dict[str, SemanticFrameMasterB] = {}
        self._seed_frames_b()

    def _seed_frames_b(self) -> None:
        """Register semantic frame structures."""

        frames_data = [
            (
                "FRAME-B-001",
                "Predatory_Check_Overpayment",
                ["Drawer", "Payee", "Disbursed_Amount", "Surplus_Transfer_Amount", "Designated_Vendor"],
                ["Payment_Medium", "Time_Horizon", "Purported_Purpose"],
                ["mail check", "deposit cashier check", "send remaining balance", "vendor kickback", "home office check"],
                0.98,
                "A perpetrator sends a fraudulent check to a candidate with explicit instructions to wire surplus funds to an unverified vendor."
            ),
            (
                "FRAME-B-002",
                "Deceptive_Task_Rating_Commission",
                ["Operator", "Participant", "Task_Type", "Commission_Rate", "Deposit_Requirement"],
                ["Platform_App", "Tier_Level", "Cryptocurrency_Rail"],
                ["recharge balance", "rate products", "boost hotel reviews", "level 1 vip", "daily task profit"],
                0.96,
                "A victim is tricked into depositing cryptocurrency to unlock simulated e-commerce rating commissions."
            ),
            (
                "FRAME-B-003",
                "Unlawful_Pre_Employment_Fee_Extraction",
                ["Employer_Impersonator", "Applicant", "Fee_Type", "Monetary_Charge"],
                ["Payment_Method", "Reimbursement_Promise"],
                ["registration fee", "training deposit", "onboarding cost", "background check fee", "reimbursed in first paycheck"],
                0.95,
                "A scam recruiter demands that an applicant pay advance fees for registration, training, or equipment setup."
            )
        ]

        for f_id, name, cores, non_cores, triggers, adv_p, desc in frames_data:
            self.frames[name] = SemanticFrameMasterB(
                frame_id=f_id,
                frame_name=name,
                core_thematic_roles=cores,
                non_core_roles=non_cores,
                lexical_triggers=triggers,
                adversarial_intent_probability=adv_p,
                description=desc
            )

    def get_frame(self, name: str) -> Optional[SemanticFrameMasterB]:
        return self.frames.get(name)
