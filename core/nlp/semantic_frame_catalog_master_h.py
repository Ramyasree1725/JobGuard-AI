"""
JobGuard Core NLP - Semantic Frame Catalog Master Volume H
Contains semantic frame definitions for cryptocurrency exchange onboarding,
personal bank account mule laundering, and synthetic voice interview deception.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class SemanticFrameMasterH:
    frame_id: str
    frame_name: str
    core_thematic_roles: List[str]
    non_core_roles: List[str]
    lexical_triggers: List[str]
    adversarial_intent_probability: float
    description: str


class SemanticFrameCatalogMasterH:
    """Master expanded catalog volume H of semantic frames for deception parsing."""

    def __init__(self):
        self.frames: Dict[str, SemanticFrameMasterH] = {}
        self._seed_frames_h()

    def _seed_frames_h() -> None:
        """Register semantic frame structures."""

        frames_data = [
            (
                "FRAME-H-001",
                "Personal_Bank_Account_Laundering_Conversion",
                ["Syndicate_Controller", "Mule_Employee", "Inbound_Funds", "Outbound_Transfer_Channel"],
                ["Mule_Commission_Cut", "Pretext_Reason"],
                ["receive client payments into personal account", "forward funds to suppliers", "financial agent role", "payment processing assistant"],
                0.99,
                "A perpetrator contracts an individual to receive third-party funds into their personal bank account and forward them to external accounts."
            ),
            (
                "FRAME-H-002",
                "Crypto_Exchange_Account_Creation_Mandate",
                ["Employer_Impersonator", "Prospective_Employee", "Exchange_Platform", "Wallet_Address"],
                ["Verification_Level", "Purported_Wage_Rail"],
                ["create account on binance for payroll", "register coinbase for salary", "open kraken account for company disbursements"],
                0.98,
                "A victim is instructed to open an account on a cryptocurrency exchange to receive or transfer corporate funds."
            ),
            (
                "FRAME-H-003",
                "Voice_Only_Deceptive_Screening",
                ["Interviewer", "Candidate", "Telephony_Rail", "Evaluation_Scope"],
                ["Audio_Quality_Marker", "Refusal_Reason"],
                ["phone call only interview", "camera not working", "voice screening only", "text and audio evaluation"],
                0.78,
                "An interviewer deliberately avoids live video interaction to conceal their identity, location, or synthetic voice artifacts."
            )
        ]

        for f_id, name, cores, non_cores, triggers, adv_p, desc in frames_data:
            self.frames[name] = SemanticFrameMasterH(
                frame_id=f_id,
                frame_name=name,
                core_thematic_roles=cores,
                non_core_roles=non_cores,
                lexical_triggers=triggers,
                adversarial_intent_probability=adv_p,
                description=desc
            )

    def get_frame(self, name: str) -> Optional[SemanticFrameMasterH]:
        return self.frames.get(name)
