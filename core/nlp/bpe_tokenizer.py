"""
Aetheris NLP & Cognitive Engine: Byte-Pair Encoding (BPE) Subword Tokenizer
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
import re
from typing import List, Dict, Tuple, Set, Optional


class BPETokenizer:
    """
    Subword Byte-Pair Encoding (BPE) Tokenizer built from first principles.
    Learns frequent character n-gram merges and enables vocabulary compression.
    """
    def __init__(self, vocab_size: int = 1000) -> None:
        self.vocab_size = vocab_size
        self.merges: List[Tuple[str, str]] = []
        self.vocab: Dict[str, int] = {}
        self.inv_vocab: Dict[int, str] = {}
        
        # Special tokens
        self.pad_token = "<PAD>"
        self.unk_token = "<UNK>"
        self.bos_token = "<BOS>"
        self.eos_token = "<EOS>"
        self.special_tokens = [self.pad_token, self.unk_token, self.bos_token, self.eos_token]
        self._init_special_tokens()

    def _init_special_tokens(self) -> None:
        self.vocab.clear()
        self.inv_vocab.clear()
        for idx, token in enumerate(self.special_tokens):
            self.vocab[token] = idx
            self.inv_vocab[idx] = token

    def _get_stats(self, word_freqs: Dict[Tuple[str, ...], int]) -> Dict[Tuple[str, str], int]:
        pairs: Dict[Tuple[str, str], int] = {}
        for word, freq in word_freqs.items():
            for i in range(len(word) - 1):
                pair = (word[i], word[i + 1])
                pairs[pair] = pairs.get(pair, 0) + freq
        return pairs

    def _merge_pair(self, pair: Tuple[str, str], word_freqs: Dict[Tuple[str, ...], int]) -> Dict[Tuple[str, ...], int]:
        new_freqs: Dict[Tuple[str, ...], int] = {}
        bigram = pair
        for word, freq in word_freqs.items():
            new_word: List[str] = []
            i = 0
            while i < len(word):
                if i < len(word) - 1 and (word[i], word[i + 1]) == bigram:
                    new_word.append(word[i] + word[i + 1])
                    i += 2
                else:
                    new_word.append(word[i])
                    i += 1
            new_freqs[tuple(new_word)] = freq
        return new_freqs

    def train(self, corpus: List[str]) -> None:
        """Learns BPE merge table from text corpus."""
        self._init_special_tokens()
        
        # Initialize basic character vocabulary
        raw_words: Dict[str, int] = {}
        for text in corpus:
            tokens = re.findall(r"\w+|[^\w\s]", text.lower())
            for t in tokens:
                raw_words[t] = raw_words.get(t, 0) + 1

        # Represent words as tuple of characters + end-of-word suffix '</w>'
        word_freqs: Dict[Tuple[str, ...], int] = {
            tuple(list(w) + ['</w>']): freq for w, freq in raw_words.items()
        }

        # Collect initial alphabet
        alphabet: Set[str] = set()
        for word in word_freqs.keys():
            for ch in word:
                alphabet.add(ch)

        for ch in sorted(list(alphabet)):
            idx = len(self.vocab)
            self.vocab[ch] = idx
            self.inv_vocab[idx] = ch

        # Iterate merges
        num_merges = max(0, self.vocab_size - len(self.vocab))
        self.merges.clear()

        for _ in range(num_merges):
            pairs = self._get_stats(word_freqs)
            if not pairs:
                break
            best_pair = max(pairs, key=pairs.get)
            self.merges.append(best_pair)
            word_freqs = self._merge_pair(best_pair, word_freqs)

            merged_token = best_pair[0] + best_pair[1]
            idx = len(self.vocab)
            self.vocab[merged_token] = idx
            self.inv_vocab[idx] = merged_token

    def tokenize_word(self, word: str) -> List[str]:
        """Applies learned BPE merges to single word."""
        symbols = list(word) + ['</w>']
        for pair in self.merges:
            bigram = (pair[0], pair[1])
            new_symbols: List[str] = []
            i = 0
            while i < len(symbols):
                if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == bigram:
                    new_symbols.append(symbols[i] + symbols[i + 1])
                    i += 2
                else:
                    new_symbols.append(symbols[i])
                    i += 1
            symbols = new_symbols
        return symbols

    def encode(self, text: str) -> List[int]:
        """Encodes string to list of token IDs."""
        tokens = re.findall(r"\w+|[^\w\s]", text.lower())
        token_ids: List[int] = [self.vocab[self.bos_token]]

        for t in tokens:
            subwords = self.tokenize_word(t)
            for sw in subwords:
                token_ids.append(self.vocab.get(sw, self.vocab[self.unk_token]))

        token_ids.append(self.vocab[self.eos_token])
        return token_ids

    def decode(self, token_ids: Sequence[int]) -> str:
        """Decodes list of token IDs back into string."""
        subwords: List[str] = []
        for tid in token_ids:
            if tid in self.inv_vocab:
                token = self.inv_vocab[tid]
                if token not in self.special_tokens:
                    subwords.append(token)

        raw_str = "".join(subwords).replace("</w>", " ")
        return raw_str.strip()
