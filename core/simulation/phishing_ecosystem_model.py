"""
JobGuard Core Simulation - Phishing Ecosystem & Kill Chain Simulator
Models the full recruitment fraud lifecycle from initial bait delivery,
chat onboarding, fake portal credential capture, to downstream banking drain.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import random


class KillChainStage(Enum):
    STAGE_1_RECON_AND_LURE = "STAGE_1_RECON_AND_LURE"
    STAGE_2_ENGAGEMENT_AND_CHAT = "STAGE_2_ENGAGEMENT_AND_CHAT"
    STAGE_3_FAKE_INTERVIEW_PASS = "STAGE_3_FAKE_INTERVIEW_PASS"
    STAGE_4_OFFER_LETTER_DELIVERY = "STAGE_4_OFFER_LETTER_DELIVERY"
    STAGE_5_EQUIPMENT_CHECK_ISSUANCE = "STAGE_5_EQUIPMENT_CHECK_ISSUANCE"
    STAGE_6_SURPLUS_TRANSFER_EXECUTION = "STAGE_6_SURPLUS_TRANSFER_EXECUTION"
    STAGE_7_CHECK_BOUNCE_AND_LOSS = "STAGE_7_CHECK_BOUNCE_AND_LOSS"


@dataclass
class KillChainTransition:
    from_stage: KillChainStage
    to_stage: KillChainStage
    probability: float
    jobguard_interception_point: bool
    detection_vectors: List[str]
    candidate_escape_action: str


@dataclass
class SimulationTrace:
    trace_id: str
    starting_candidate_tier: str
    reached_stage: KillChainStage
    was_intercepted: bool
    intercepting_subsystem: Optional[str]
    victim_financial_loss: float
    dwell_time_days: float
    stage_transitions_logged: List[str]


class PhishingEcosystemModel:
    """Simulates the step-by-step conversion funnel across the recruitment fraud kill chain."""

    def __init__(self, seed: Optional[int] = 42):
        if seed is not None:
            random.seed(seed)
        self.transitions: Dict[KillChainStage, KillChainTransition] = {}
        self._build_transition_graph()

    def _build_transition_graph(self) -> None:
        """Configures the probabilistic state machine for recruitment fraud progression."""

        self.transitions[KillChainStage.STAGE_1_RECON_AND_LURE] = KillChainTransition(
            from_stage=KillChainStage.STAGE_1_RECON_AND_LURE,
            to_stage=KillChainStage.STAGE_2_ENGAGEMENT_AND_CHAT,
            probability=0.35,
            jobguard_interception_point=True,
            detection_vectors=["Job Posting Scanner", "Domain Lookalike Verifier"],
            candidate_escape_action="Flag email / Ignore unsolicited LinkedIn message"
        )

        self.transitions[KillChainStage.STAGE_2_ENGAGEMENT_AND_CHAT] = KillChainTransition(
            from_stage=KillChainStage.STAGE_2_ENGAGEMENT_AND_CHAT,
            to_stage=KillChainStage.STAGE_3_FAKE_INTERVIEW_PASS,
            probability=0.70,
            jobguard_interception_point=True,
            detection_vectors=["Telegram Channel Heuristics", "Scripted Questionnaire NLP Scanner"],
            candidate_escape_action="Demand live video conference or official HR phone call"
        )

        self.transitions[KillChainStage.STAGE_3_FAKE_INTERVIEW_PASS] = KillChainTransition(
            from_stage=KillChainStage.STAGE_3_FAKE_INTERVIEW_PASS,
            to_stage=KillChainStage.STAGE_4_OFFER_LETTER_DELIVERY,
            probability=0.90,
            jobguard_interception_point=False,
            detection_vectors=[],
            candidate_escape_action="Inquire why no technical or behavioral evaluation took place"
        )

        self.transitions[KillChainStage.STAGE_4_OFFER_LETTER_DELIVERY] = KillChainTransition(
            from_stage=KillChainStage.STAGE_4_OFFER_LETTER_DELIVERY,
            to_stage=KillChainStage.STAGE_5_EQUIPMENT_CHECK_ISSUANCE,
            probability=0.60,
            jobguard_interception_point=True,
            detection_vectors=["Offer Letter Auditor", "Cryptographic Seal & Exif Scanner"],
            candidate_escape_action="Scan PDF contract on JobGuard Offer Letter Auditor"
        )

        self.transitions[KillChainStage.STAGE_5_EQUIPMENT_CHECK_ISSUANCE] = KillChainTransition(
            from_stage=KillChainStage.STAGE_5_EQUIPMENT_CHECK_ISSUANCE,
            to_stage=KillChainStage.STAGE_6_SURPLUS_TRANSFER_EXECUTION,
            probability=0.45,
            jobguard_interception_point=True,
            detection_vectors=["Financial Check Kickback Detector", "Banking Alert Protocol"],
            candidate_escape_action="Refuse to deposit check or forward money to third-party vendor"
        )

        self.transitions[KillChainStage.STAGE_6_SURPLUS_TRANSFER_EXECUTION] = KillChainTransition(
            from_stage=KillChainStage.STAGE_6_SURPLUS_TRANSFER_EXECUTION,
            to_stage=KillChainStage.STAGE_7_CHECK_BOUNCE_AND_LOSS,
            probability=0.98,
            jobguard_interception_point=False,
            detection_vectors=[],
            candidate_escape_action="File immediate IC3 and bank fraud chargeback"
        )

    def run_kill_chain_simulation(
        self,
        num_trials: int = 1000,
        enable_jobguard_interception: bool = True,
        interception_efficacy: float = 0.95
    ) -> Dict[str, Any]:
        """Simulates thousands of victim trajectories through the recruitment fraud kill chain."""
        traces: List[SimulationTrace] = []
        stage_counts: Dict[str, int] = {s.value: 0 for s in KillChainStage}
        total_loss = 0.0
        interceptions_by_system: Dict[str, int] = {}

        for i in range(num_trials):
            current_stage = KillChainStage.STAGE_1_RECON_AND_LURE
            stage_counts[current_stage.value] += 1
            log = [current_stage.value]
            dwell_days = random.uniform(0.5, 2.0)
            intercepted = False
            interceptor = None
            loss = 0.0

            while current_stage in self.transitions:
                transition = self.transitions[current_stage]

                # Check if JobGuard intercepts at this junction
                if enable_jobguard_interception and transition.jobguard_interception_point:
                    if random.random() < interception_efficacy:
                        intercepted = True
                        interceptor = random.choice(transition.detection_vectors)
                        interceptions_by_system[interceptor] = interceptions_by_system.get(interceptor, 0) + 1
                        break

                # Check if victim transitions to next trap
                if random.random() < transition.probability:
                    current_stage = transition.to_stage
                    stage_counts[current_stage.value] += 1
                    log.append(current_stage.value)
                    dwell_days += random.uniform(1.0, 4.0)

                    if current_stage == KillChainStage.STAGE_7_CHECK_BOUNCE_AND_LOSS:
                        loss = random.uniform(1800.0, 4500.0)
                        total_loss += loss
                        break
                else:
                    # Candidate dropped out on their own
                    break

            traces.append(SimulationTrace(
                trace_id=f"TRACE_{i:05d}",
                starting_candidate_tier="GENERAL_COHORT",
                reached_stage=current_stage,
                was_intercepted=intercepted,
                intercepting_subsystem=interceptor,
                victim_financial_loss=loss,
                dwell_time_days=dwell_days,
                stage_transitions_logged=log
            ))

        return {
            "total_trials": num_trials,
            "stage_distribution": stage_counts,
            "total_financial_loss_usd": total_loss,
            "interceptions_by_subsystem": interceptions_by_system,
            "total_intercepted": sum(1 for t in traces if t.was_intercepted),
            "final_stage_victim_rate_pct": (stage_counts[KillChainStage.STAGE_7_CHECK_BOUNCE_AND_LOSS.value] / num_trials) * 100.0
        }
