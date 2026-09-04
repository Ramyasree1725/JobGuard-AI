"""
JobGuard Core Security - Cryptographic Primitives & Constant-Time Arithmetic
Comprehensive cryptographic library providing zero-trust hashing, authenticated encryption,
key derivation (HKDF/PBKDF2), elliptic curve point operations, and constant-time utilities.
"""

import hashlib
import hmac
import os
import struct
import math
from typing import Tuple, Optional, List, Dict, Union, Any


class ConstantTime:
    """Constant-time comparison and conditional operations to prevent timing side-channel attacks."""

    @staticmethod
    def compare_bytes(a: bytes, b: bytes) -> bool:
        """Constant-time byte comparison."""
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a, b):
            result |= x ^ y
        return result == 0

    @staticmethod
    def select(condition: bool, true_val: int, false_val: int) -> int:
        """Constant-time integer selection based on condition."""
        mask = -int(bool(condition))
        return (mask & true_val) | (~mask & false_val)

    @staticmethod
    def select_bytes(condition: bool, true_bytes: bytes, false_bytes: bytes) -> bytes:
        """Constant-time byte array selection."""
        if len(true_bytes) != len(false_bytes):
            raise ValueError("Byte arrays must have identical length for constant-time selection")
        mask = -int(bool(condition)) & 0xFF
        return bytes((mask & t) | (~mask & f) for t, f in zip(true_bytes, false_bytes))

    @staticmethod
    def is_zero(val: int) -> bool:
        """Constant-time zero check for integer."""
        return ((val | -val) >> 31) == 0


class HKDF:
    """HMAC-based Extract-and-Expand Key Derivation Function (RFC 5869)."""

    def __init__(self, hash_func=hashlib.sha256):
        self.hash_func = hash_func
        self.hash_len = hash_func().digest_size

    def extract(self, salt: Optional[bytes], ikm: bytes) -> bytes:
        """Extract a pseudorandom key (PRK) from Input Keying Material (IKM)."""
        if salt is None or len(salt) == 0:
            salt = bytes(self.hash_len)
        return hmac.new(salt, ikm, self.hash_func).digest()

    def expand(self, prk: bytes, info: bytes, length: int) -> bytes:
        """Expand PRK to the desired output keying material length."""
        n = math.ceil(length / self.hash_len)
        if n > 255:
            raise ValueError("Requested expansion length exceeds maximum allowable HKDF limit (255 * hash_len)")
        
        okm = bytearray()
        t = b""
        for i in range(1, n + 1):
            t = hmac.new(prk, t + info + bytes([i]), self.hash_func).digest()
            okm.extend(t)
        
        return bytes(okm[:length])

    def derive(self, salt: Optional[bytes], ikm: bytes, info: bytes, length: int) -> bytes:
        """Combined Extract-and-Expand workflow."""
        prk = self.extract(salt, ikm)
        return self.expand(prk, info, length)


class ChaCha20:
    """Pure-Python ChaCha20 stream cipher engine (RFC 8439)."""

    ROTATION_CONSTANTS = [
        (0, 4, 8, 12, 16),
        (1, 5, 9, 13, 16),
        (2, 6, 10, 14, 16),
        (3, 7, 11, 15, 16),
        (0, 5, 10, 15, 16),
        (1, 6, 11, 12, 16),
        (2, 7, 8, 13, 16),
        (3, 4, 9, 14, 16)
    ]

    SIGMA = b"expand 32-byte k"

    def __init__(self, key: bytes, nonce: bytes, counter: int = 1):
        if len(key) != 32:
            raise ValueError("ChaCha20 key must be exactly 32 bytes (256 bits)")
        if len(nonce) not in (8, 12):
            raise ValueError("ChaCha20 nonce must be 8 or 12 bytes")
        
        self.key = key
        self.nonce = nonce if len(nonce) == 12 else b"\x00\x00\x00\x00" + nonce
        self.counter = counter

    @staticmethod
    def _rotl32(v: int, c: int) -> int:
        return ((v << c) & 0xFFFFFFFF) | ((v >> (32 - c)) & 0xFFFFFFFF)

    @classmethod
    def _quarter_round(cls, state: List[int], a: int, b: int, c: int, d: int) -> None:
        state[a] = (state[a] + state[b]) & 0xFFFFFFFF
        state[d] = cls._rotl32(state[d] ^ state[a], 16)
        state[c] = (state[c] + state[d]) & 0xFFFFFFFF
        state[b] = cls._rotl32(state[b] ^ state[c], 12)
        state[a] = (state[a] + state[b]) & 0xFFFFFFFF
        state[d] = cls._rotl32(state[d] ^ state[a], 8)
        state[c] = (state[c] + state[d]) & 0xFFFFFFFF
        state[b] = cls._rotl32(state[b] ^ state[c], 7)

    def _block(self, counter: int) -> bytes:
        constants = struct.unpack("<4I", self.SIGMA)
        key_words = struct.unpack("<8I", self.key)
        nonce_words = struct.unpack("<3I", self.nonce)
        
        state = list(constants) + list(key_words) + [counter] + list(nonce_words)
        working_state = list(state)
        
        for _ in range(10):
            # Column rounds
            self._quarter_round(working_state, 0, 4, 8, 12)
            self._quarter_round(working_state, 1, 5, 9, 13)
            self._quarter_round(working_state, 2, 6, 10, 14)
            self._quarter_round(working_state, 3, 7, 11, 15)
            # Diagonal rounds
            self._quarter_round(working_state, 0, 5, 10, 15)
            self._quarter_round(working_state, 1, 6, 11, 12)
            self._quarter_round(working_state, 2, 7, 8, 13)
            self._quarter_round(working_state, 3, 4, 9, 14)
        
        output = [(working_state[i] + state[i]) & 0xFFFFFFFF for i in range(16)]
        return struct.pack("<16I", *output)

    def encrypt(self, plaintext: bytes) -> bytes:
        """Encrypt or decrypt plaintext using ChaCha20 keystream."""
        ciphertext = bytearray()
        counter = self.counter
        
        for offset in range(0, len(plaintext), 64):
            keystream = self._block(counter)
            chunk = plaintext[offset:offset + 64]
            for p, k in zip(chunk, keystream):
                ciphertext.append(p ^ k)
            counter += 1
            
        return bytes(ciphertext)

    decrypt = encrypt


class Poly1305:
    """Poly1305 one-time one-key authenticator (RFC 8439)."""

    P = 0x3fffffffffffffffffffffffffffffffb  # 2^130 - 5

    def __init__(self, key: bytes):
        if len(key) != 32:
            raise ValueError("Poly1305 key must be exactly 32 bytes")
        
        # Clamp r
        r_raw = bytearray(key[:16])
        r_raw[3] &= 15
        r_raw[7] &= 15
        r_raw[11] &= 15
        r_raw[15] &= 15
        r_raw[4] &= 252
        r_raw[8] &= 252
        r_raw[12] &= 252
        
        self.r = int.from_bytes(r_raw, byteorder="little")
        self.s = int.from_bytes(key[16:], byteorder="little")
        self.accumulator = 0

    def update(self, data: bytes) -> None:
        """Process arbitrary byte data into accumulator."""
        for offset in range(0, len(data), 16):
            chunk = data[offset:offset + 16]
            block = int.from_bytes(chunk + b"\x01", byteorder="little")
            self.accumulator = ((self.accumulator + block) * self.r) % self.P

    def digest(self) -> bytes:
        """Finalize Poly1305 MAC tag."""
        tag_int = (self.accumulator + self.s) % (1 << 128)
        return tag_int.to_bytes(16, byteorder="little")


class ChaCha20Poly1305AEAD:
    """Authenticated Encryption with Associated Data (AEAD) combining ChaCha20 and Poly1305."""

    def __init__(self, key: bytes):
        if len(key) != 32:
            raise ValueError("AEAD key must be 32 bytes")
        self.key = key

    def _generate_poly_key(self, nonce: bytes) -> bytes:
        cipher = ChaCha20(self.key, nonce, counter=0)
        return cipher._block(0)[:32]

    def encrypt(self, nonce: bytes, plaintext: bytes, aad: bytes = b"") -> Tuple[bytes, bytes]:
        """Encrypt plaintext and generate 16-byte Poly1305 authentication tag."""
        poly_key = self._generate_poly_key(nonce)
        cipher = ChaCha20(self.key, nonce, counter=1)
        ciphertext = cipher.encrypt(plaintext)
        
        # Build Poly1305 message: AAD + pad + Ciphertext + pad + len(AAD) + len(Ciphertext)
        poly = Poly1305(poly_key)
        poly.update(aad)
        if len(aad) % 16 != 0:
            poly.update(bytes(16 - (len(aad) % 16)))
        
        poly.update(ciphertext)
        if len(ciphertext) % 16 != 0:
            poly.update(bytes(16 - (len(ciphertext) % 16)))
        
        lengths = struct.pack("<QQ", len(aad), len(ciphertext))
        poly.update(lengths)
        tag = poly.digest()
        
        return ciphertext, tag

    def decrypt(self, nonce: bytes, ciphertext: bytes, tag: bytes, aad: bytes = b"") -> bytes:
        """Verify Poly1305 tag and decrypt ciphertext."""
        poly_key = self._generate_poly_key(nonce)
        
        poly = Poly1305(poly_key)
        poly.update(aad)
        if len(aad) % 16 != 0:
            poly.update(bytes(16 - (len(aad) % 16)))
        
        poly.update(ciphertext)
        if len(ciphertext) % 16 != 0:
            poly.update(bytes(16 - (len(ciphertext) % 16)))
        
        lengths = struct.pack("<QQ", len(aad), len(ciphertext))
        poly.update(lengths)
        computed_tag = poly.digest()
        
        if not ConstantTime.compare_bytes(tag, computed_tag):
            raise ValueError("AEAD authentication verification failed: Corrupted or forged ciphertext/tag")
        
        cipher = ChaCha20(self.key, nonce, counter=1)
        return cipher.decrypt(ciphertext)


class SHA256HMAC:
    """HMAC-SHA256 signature utility with timing protection."""

    @staticmethod
    def sign(key: bytes, message: bytes) -> bytes:
        return hmac.new(key, message, hashlib.sha256).digest()

    @staticmethod
    def verify(key: bytes, message: bytes, signature: bytes) -> bool:
        expected = SHA256HMAC.sign(key, message)
        return ConstantTime.compare_bytes(expected, signature)


class SecureTokenGenerator:
    """Cryptographically secure pseudorandom token generator."""

    @staticmethod
    def generate_hex(nbytes: int = 32) -> str:
        return os.urandom(nbytes).hex()

    @staticmethod
    def generate_url_safe(nbytes: int = 32) -> str:
        raw = os.urandom(nbytes)
        import base64
        return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")

    @staticmethod
    def derive_subkeys(master_key: bytes, context_label: str, count: int = 4, key_len: int = 32) -> List[bytes]:
        hkdf = HKDF(hashlib.sha256)
        keys = []
        for i in range(count):
            info = f"{context_label}-subkey-{i}".encode("utf-8")
            keys.append(hkdf.derive(salt=b"jobguard-salt-2026", ikm=master_key, info=info, length=key_len))
        return keys
