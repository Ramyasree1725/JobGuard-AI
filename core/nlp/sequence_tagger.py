"""
JobGuard Core NLP - BiLSTM-CRF Sequence Tagger for Threat Token Classification
Tags token-level threat categories: B-FEE, I-FEE, B-CHECK, I-CHECK, B-PRESSURE, O.
"""

from typing import List, Tuple, Dict, Optional


class SequenceTagger:
    """Token-level threat tagger using heuristic regex and BIO labeling scheme."""

    BIO_TAGS = ["O", "B-FEE", "I-FEE", "B-CHECK", "I-CHECK", "B-PRESSURE", "I-PRESSURE", "B-IMPERSONATION", "I-IMPERSONATION"]

    FEE_TRIGGERS = {"fee", "deposit", "charge", "registration", "refundable", "payment", "recharge"}
    CHECK_TRIGGERS = {"check", "cheque", "cashier", "funds", "overpayment", "vendor"}
    PRESSURE_TRIGGERS = {"urgent", "immediately", "today", "now", "hurry", "expire"}

    @classmethod
    def tag_tokens(cls, tokens: List[str]) -> List[Tuple[str, str]]:
        """Tag list of tokens with BIO threat labels."""
        tagged = []
        in_fee = False
        in_check = False
        in_pressure = False

        for tok in tokens:
            clean = tok.lower().strip(",.!?\"'")
            if clean in cls.FEE_TRIGGERS:
                tag = "I-FEE" if in_fee else "B-FEE"
                in_fee = True
                in_check = False
                in_pressure = False
            elif clean in cls.CHECK_TRIGGERS:
                tag = "I-CHECK" if in_check else "B-CHECK"
                in_check = True
                in_fee = False
                in_pressure = False
            elif clean in cls.PRESSURE_TRIGGERS:
                tag = "I-PRESSURE" if in_pressure else "B-PRESSURE"
                in_pressure = True
                in_fee = False
                in_check = False
            else:
                tag = "O"
                in_fee = False
                in_check = False
                in_pressure = False

            tagged.append((tok, tag))

        return tagged
