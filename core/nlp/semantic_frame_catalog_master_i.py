"""
JobGuard Core NLP - Semantic Frame Catalog Master Volume I
Contains semantic frame definitions for simulated escrow holding agreements,
task reset penalty surcharges, and altered contract creation dates.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class SemanticFrameMasterI:
    frame_id: str
    frame_name: str
    core_thematic_roles: List[str]
    non_core_roles: List[str]
    lexical_triggers: List[str]
    adversarial_intent_probability: float
    description: str


class SemanticFrameCatalogMasterI:
    """Master expanded catalog volume I of semantic frames for deception parsing."""

    def __init__(self):
        self.frames: Dict[str, SemanticFrameMasterI] = {}
        self._seed_frames_i()

    def _seed_frames_i(self) -> None:
        """Register semantic frame structures."""

        frames_data = [
            (
                "FRAME-I-001",
                "Simulated_Escrow_Holding_Pretext",
                ["Escrow_Operator", "Victim_Beneficiary", "Locked_Amount", "Unlock_Deposit_Demand"],
                ["Purported_Escrow_Portal", "Release_Condition"],
                ["funds held in escrow", "advance deposit to release salary", "escrow security requirement", "unlock pending balance"],
                0.98,
                "A perpetrator claims that candidate funds or allowances are locked in an escrow account requiring a deposit to release."
            ),
            (
                "FRAME-I-002",
                "Task_Reset_Penalty_Surcharge",
                ["Platform_Controller", "Defrauded_Worker", "Locked_Earnings", "Surcharge_Amount"],
                ["VIP_Tier", "Cryptocurrency_Address"],
                ["account frozen task incomplete", "deposit to unfreeze balance", "task reset penalty", "recharge to complete VIP cycle"],
                0.99,
                "A predatory algorithm locks user balances and demands exponential cryptocurrency deposits to withdraw earnings."
            ),
            (
                "FRAME-I-003",
                "Altered_Contract_Creation_Date",
                ["Document_Originator", "Signatory_Candidate", "Printed_Date", "Digital_Creation_Timestamp"],
                ["Discrepancy_Window", "Stated_Urgency"],
                ["signed on effective date", "valid for 24 hours only", "immediate electronic signature required"],
                0.86,
                "A forged document displays fabricated dates that conflict with internal PDF creation metadata timestamps."
            )
        ]

        for f_id, name, cores, non_cores, triggers, adv_p, desc in frames_data:
            self.frames[name] = SemanticFrameMasterI(
                frame_id=f_id,
                frame_name=name,
                core_thematic_roles=cores,
                non_core_roles=non_cores,
                lexical_triggers=triggers,
                adversarial_intent_probability=adv_p,
                description=desc
            )

    def get_frame(self, name: str) -> Optional[SemanticFrameMasterI]:
        return self.frames.get(name)
