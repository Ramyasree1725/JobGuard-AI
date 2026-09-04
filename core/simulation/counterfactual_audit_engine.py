"""
JobGuard Core Simulation - Counterfactual Perturbation Audit Engine
Performs minimal-edit adversarial perturbations on job descriptions to identify
exact decision boundary sensitivities and model vulnerability to lexical evasions.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re


@dataclass
class PerturbationCandidate:
    original_phrase: str
    perturbed_phrase: str
    evasion_strategy: str  # 'SYNONYM_SUBSTITUTION', 'TYPO_INJECTION', 'SPACING_SPLIT', 'HOMOGLYPH'
    risk_delta: float
    is_evasive: bool


@dataclass
class CounterfactualAuditReport:
    original_text: str
    original_risk_score: float
    minimal_evasive_text: str
    minimal_evasive_risk_score: float
    perturbations_applied: List[PerturbationCandidate]
    robustness_margin: float  # Difference between clean score and best evasion
    is_vulnerable_to_lexical_evasion: bool


class CounterfactualAuditEngine:
    """Evaluates how robust the scam detection heuristics are against subtle adversarial text edits."""

    COMMON_EVASIONS: Dict[str, List[str]] = {
        "telegram": ["Tele-gram", "T.e.l.e.g.r.a.m", "Te1egram", "TG app"],
        "whatsapp": ["Whats-App", "W.h.a.t.s.a.p.p", "WA chat", "WApp"],
        "check": ["cheque", "e-check", "draft payment", "bank paper"],
        "wire transfer": ["direct bank wire", "SWIFT transfer", "RTGS", "electronic wire"],
        "equipment fee": ["procurement advance", "onboarding toolkit deposit", "workstation collateral"],
        "registration fee": ["administrative setup cost", "application processing charge", "candidate verification deposit"],
        "crypto": ["digital asset", "blockchain credit", "TRC-20 token", "USDT settlement"],
        "cashier check": ["official bank draft", "certified bank voucher", "corporate cashier order"]
    }

    def __init__(self, base_scorer=None):
        self.base_scorer = base_scorer or self._default_mock_scorer

    def _default_mock_scorer(self, text: str) -> float:
        """Simple baseline scorer for standalone counterfactual analysis."""
        score = 0.0
        lower = text.lower()
        
        red_flags = [
            (r"telegram|whatsapp|signal", 25.0),
            (r"check|cheque|cashier", 30.0),
            (r"wire\s+transfer|zelle|cashapp|crypto|usdt", 35.0),
            (r"equipment|registration|onboarding\s+fee", 40.0),
            (r"urgent|immediate\s+hire|no\s+interview", 20.0),
            (r"\$\d{2,3}/hr.*data\s+entry", 30.0)
        ]
        
        for pattern, weight in red_flags:
            if re.search(pattern, lower):
                score += weight

        return min(100.0, score)

    def generate_counterfactuals(self, text: str) -> CounterfactualAuditReport:
        """Applies systematic perturbations to discover minimal adversarial edits that evade detection."""
        original_score = self.base_scorer(text)
        current_text = text
        applied_perturbations: List[PerturbationCandidate] = []

        # Find targets in text
        for target, replacements in self.COMMON_EVASIONS.items():
            pattern = re.compile(re.escape(target), re.IGNORECASE)
            match = pattern.search(current_text)
            
            if match:
                best_sub: Optional[str] = None
                best_score = original_score

                for rep in replacements:
                    perturbed = pattern.sub(rep, current_text, count=1)
                    p_score = self.base_scorer(perturbed)
                    
                    if p_score < best_score:
                        best_score = p_score
                        best_sub = rep

                if best_sub:
                    current_text = pattern.sub(best_sub, current_text, count=1)
                    applied_perturbations.append(PerturbationCandidate(
                        original_phrase=target,
                        perturbed_phrase=best_sub,
                        evasion_strategy="SYNONYM_SUBSTITUTION",
                        risk_delta=original_score - best_score,
                        is_evasive=(best_score < 50.0 <= original_score)
                    ))

        final_score = self.base_scorer(current_text)
        robustness_margin = max(0.0, original_score - final_score)
        is_vulnerable = original_score >= 50.0 > final_score

        return CounterfactualAuditReport(
            original_text=text,
            original_risk_score=original_score,
            minimal_evasive_text=current_text,
            minimal_evasive_risk_score=final_score,
            perturbations_applied=applied_perturbations,
            robustness_margin=robustness_margin,
            is_vulnerable_to_lexical_evasion=is_vulnerable
        )
