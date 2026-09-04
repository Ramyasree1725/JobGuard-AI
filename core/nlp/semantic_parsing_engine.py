"""
JobGuard Core NLP - Semantic Role Labeling (SRL) & FrameNet Predicate Extractors
Maps sentence clauses into PropBank predicate-argument structures:
[ARG0 Agent / Recruiter] -> [TARGET Predicate: Demands] -> [ARG1 Patient: Registration Fee] -> [ARG2 Recipient: Personal UPI].
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class SemanticRoleArgument:
    role_label: str  # "ARG0", "ARG1", "ARG2", "ARGM-TMP", "ARGM-LOC", "ARGM-MNR"
    span_text: str
    token_indices: List[int]


@dataclass
class PropBankFrame:
    predicate_lemma: str
    predicate_sense: str  # e.g., "pay.01", "wire.01", "deposit.01"
    predicate_token_idx: int
    arguments: List[SemanticRoleArgument]


class SemanticParsingEngine:
    """Extracts propositional semantic frames from contract sentences."""

    TARGET_PREDICATES = {
        "pay": "pay.01",
        "deposit": "deposit.01",
        "wire": "wire.01",
        "transfer": "transfer.01",
        "send": "send.01",
        "recharge": "recharge.01",
        "buy": "buy.01",
        "purchase": "purchase.01"
    }

    @classmethod
    def parse_sentence(cls, sentence: str) -> List[PropBankFrame]:
        tokens = sentence.split()
        frames: List[PropBankFrame] = []

        for idx, tok in enumerate(tokens):
            clean_tok = tok.lower().strip(",.!?\"'")
            if clean_tok in cls.TARGET_PREDICATES:
                sense = cls.TARGET_PREDICATES[clean_tok]
                
                # Heuristic argument assignment
                arg0_tokens = tokens[:idx]
                arg1_tokens = tokens[idx + 1:]

                args = []
                if arg0_tokens:
                    args.append(SemanticRoleArgument(
                        role_label="ARG0",  # Agent / Subject
                        span_text=" ".join(arg0_tokens),
                        token_indices=list(range(0, idx))
                    ))

                if arg1_tokens:
                    args.append(SemanticRoleArgument(
                        role_label="ARG1",  # Theme / Amount / Object
                        span_text=" ".join(arg1_tokens),
                        token_indices=list(range(idx + 1, len(tokens)))
                    ))

                frames.append(PropBankFrame(
                    predicate_lemma=clean_tok,
                    predicate_sense=sense,
                    predicate_token_idx=idx,
                    arguments=args
                ))

        return frames
