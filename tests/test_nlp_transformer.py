"""
Unit Tests: Aetheris NLP & Transformer Multi-Head Attention
"""
import pytest
from core.nlp.bpe_tokenizer import BPETokenizer
from core.nlp.attention import MultiHeadAttention, PositionalEncoding
from core.nlp.transformer_blocks import ResearchTransformerLM
from core.nlp.beam_search import TextGenerator


def test_bpe_tokenizer_encode_decode():
    tok = BPETokenizer(vocab_size=50)
    tok.train(["autonomous robotics system", "optimization algorithms"])
    ids = tok.encode("autonomous system")
    assert len(ids) >= 2
    decoded = tok.decode(ids)
    assert "autonomous" in decoded


def test_multi_head_attention_shape():
    mha = MultiHeadAttention(d_model=16, num_heads=2)
    # Dummy sequence (seq_len=4, d_model=16)
    dummy_seq = [[0.1] * 16 for _ in range(4)]
    out = mha.forward(dummy_seq, dummy_seq, dummy_seq, is_causal=True)
    assert len(out) == 4
    assert len(out[0]) == 16


def test_transformer_autoregressive_generation():
    lm = ResearchTransformerLM(vocab_size=20, d_model=16, num_layers=1, num_heads=2)
    gen = TextGenerator(lm)
    out_ids = gen.generate([1, 2], max_new_tokens=5)
    assert len(out_ids) == 7
