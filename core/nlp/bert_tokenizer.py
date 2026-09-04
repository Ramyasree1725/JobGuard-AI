"""
JobGuard Core NLP - WordPiece Tokenizer & BERT Preprocessing
Implements WordPiece subword tokenization, vocabulary trie search,
special token handling ([CLS], [SEP], [MASK], [UNK]), and positional masking.
"""

from typing import List, Dict, Tuple, Set, Optional


class WordPieceTokenizer:
    """Standard WordPiece subword tokenizer implementation."""

    def __init__(self, vocab: Optional[Dict[str, int]] = None, unk_token: str = "[UNK]", max_input_chars_per_word: int = 100):
        self.vocab = vocab or self._default_vocab()
        self.inv_vocab = {v: k for k, v in self.vocab.items()}
        self.unk_token = unk_token
        self.max_chars = max_input_chars_per_word

    @staticmethod
    def _default_vocab() -> Dict[str, int]:
        tokens = [
            "[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]",
            "job", "offer", "letter", "salary", "fee", "deposit", "check", "wire", "transfer",
            "recruiter", "company", "interview", "telegram", "whatsapp", "payment", "bank",
            "urgent", "immediate", "guaranteed", "google", "amazon", "microsoft", "apple",
            "##ing", "##ed", "##ly", "##tion", "##ment", "##s", "##es", "##er", "##est"
        ]
        return {tok: idx for idx, tok in enumerate(tokens)}

    def tokenize_word(self, word: str) -> List[str]:
        """Tokenize a single word into subword units with '##' prefix."""
        if len(word) > self.max_chars:
            return [self.unk_token]

        is_bad = False
        start = 0
        sub_tokens: List[str] = []

        while start < len(word):
            end = len(word)
            cur_substr = None

            while start < end:
                substr = word[start:end]
                if start > 0:
                    substr = "##" + substr
                if substr in self.vocab:
                    cur_substr = substr
                    break
                end -= 1

            if cur_substr is None:
                is_bad = True
                break

            sub_tokens.append(cur_substr)
            start = end

        if is_bad:
            return [self.unk_token]
        return sub_tokens

    def encode(self, text: str, max_length: int = 128) -> Tuple[List[int], List[int], List[int]]:
        """Encodes text into (input_ids, attention_mask, token_type_ids)."""
        words = text.lower().split()
        subwords = ["[CLS]"]
        for w in words:
            subwords.extend(self.tokenize_word(w))
        subwords = subwords[:max_length - 1] + ["[SEP]"]

        input_ids = [self.vocab.get(tok, self.vocab.get(self.unk_token, 1)) for tok in subwords]
        attention_mask = [1] * len(input_ids)
        token_type_ids = [0] * len(input_ids)

        # Padding
        pad_len = max_length - len(input_ids)
        if pad_len > 0:
            input_ids.extend([self.vocab.get("[PAD]", 0)] * pad_len)
            attention_mask.extend([0] * pad_len)
            token_type_ids.extend([0] * pad_len)

        return input_ids, attention_mask, token_type_ids
