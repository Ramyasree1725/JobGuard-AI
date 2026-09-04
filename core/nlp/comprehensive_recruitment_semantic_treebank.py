"""
JobGuard Core NLP - Comprehensive Recruitment Semantic Frame Treebank
Provides annotated semantic frames, syntactic parse trees, predicate argument structures,
and thematic role bindings for linguistic fraud detection and intent decomposition.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class SemanticFrameDefinition:
    frame_name: str
    core_elements: List[str]  # e.g., 'PERPETRATOR', 'VICTIM', 'MONETARY_AMOUNT', 'MEDIUM'
    lexical_units: List[str]
    is_adversarial_intent: bool
    frame_description: str
    sample_sentence: str


class ComprehensiveRecruitmentSemanticTreebank:
    """Repository of semantic frames capturing recruitment fraud interactions."""

    def __init__(self):
        self.frames: Dict[str, SemanticFrameDefinition] = {}
        self._initialize_frame_treebank()

    def _initialize_frame_treebank(self) -> None:
        """Register semantic frame structures."""

        frames_data = [
            (
                "ADVANCE_FEE_DEMAND",
                ["PERPETRATOR", "VICTIM", "FEE_AMOUNT", "PRETEXT", "PAYMENT_RAIL"],
                ["charge", "fee", "deposit", "pay upfront", "registration cost", "onboarding fee"],
                True,
                "A perpetrator demands that a prospective job applicant pay an advance sum under the guise of an onboarding, equipment, or background check fee.",
                "Candidate is instructed to pay a $250 registration fee via Zelle to activate their employee profile."
            ),
            (
                "CHECK_OVERPAYMENT_DISBURSEMENT",
                ["DRAWER", "PAYEE", "CHECK_AMOUNT", "SURPLUS_AMOUNT", "VENDOR"],
                ["mail check", "deposit check", "send balance", "vendor payment", "home office funds"],
                True,
                "A perpetrator delivers a fraudulent check to the victim, instructing them to deposit it and transfer the surplus to an alleged vendor.",
                "Employer mails a $4,500 check and instructs applicant to wire $3,800 to an IT hardware supplier."
            ),
            (
                "ANONYMOUS_COMMUNICATION_DIVERT",
                ["RECRUITER", "CANDIDATE", "ORIGINAL_CHANNEL", "DIVERTED_PLATFORM", "HANDLE"],
                ["message on telegram", "add on whatsapp", "switch to signal", "chat interview"],
                True,
                "A recruiter redirects communication from a standard job board to an unverified, encrypted, or disposable messaging platform.",
                "Recruiter requests applicant to download Telegram and message @hiring_desk for immediate evaluation."
            ),
            (
                "COMPENSATION_PROMISORY_OFFER",
                ["EMPLOYER", "EMPLOYEE", "OFFERED_RATE", "TIME_PERIOD", "JOB_DUTIES"],
                ["hourly rate", "daily pay", "sign-on bonus", "weekly commission", "compensation package"],
                False,
                "An organization defines the remuneration and wage structure offered to a worker in exchange for defined labor services.",
                "Company offers $28.50 per hour with medical, dental, and 401(k) benefits."
            ),
            (
                "IDENTITY_CREDENTIAL_SOLICITATION",
                ["COLLECTOR", "SUBJECT", "CREDENTIAL_TYPE", "TRANSMISSION_METHOD"],
                ["request ssn", "ask for passport", "banking login", "w4 details", "identity verification"],
                True,
                "An entity requests government identification, direct deposit details, or tax numbers from an applicant.",
                "Application form demands submission of full Social Security Number before any interview."
            )
        ]

        for name, cores, units, is_adv, desc, samp in frames_data:
            frame = SemanticFrameDefinition(
                frame_name=name,
                core_elements=cores,
                lexical_units=units,
                is_adversarial_intent=is_adv,
                frame_description=desc,
                sample_sentence=samp
            )
            self.frames[name] = frame

    def get_frame(self, frame_name: str) -> Optional[SemanticFrameDefinition]:
        return self.frames.get(frame_name)
