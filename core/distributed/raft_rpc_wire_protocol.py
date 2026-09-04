"""
JobGuard Core Distributed - Raft Binary Wire Protocol & RPC Frame Codec
Implements binary serialization, CRC32 packet checksum validation,
TLV (Type-Length-Value) framing, and network packet encode/decode primitives for Raft RPCs.
"""

import struct
import zlib
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass


class RaftWireCodec:
    """Binary wire codec for serializing and deserializing Raft consensus RPC frames."""

    MAGIC_HEADER = 0x52414654  # 'RAFT' in ASCII hex
    PROTOCOL_VERSION = 1

    MSG_REQUEST_VOTE = 0x01
    MSG_REQUEST_VOTE_REPLY = 0x02
    MSG_APPEND_ENTRIES = 0x03
    MSG_APPEND_ENTRIES_REPLY = 0x04

    @classmethod
    def encode_frame(cls, msg_type: int, payload: bytes) -> bytes:
        """Frame format: [MAGIC(4B)][VER(1B)][TYPE(1B)][LEN(4B)][PAYLOAD(N B)][CRC32(4B)]."""
        payload_len = len(payload)
        header = struct.pack("!IBBI", cls.MAGIC_HEADER, cls.PROTOCOL_VERSION, msg_type, payload_len)
        crc = zlib.crc32(header + payload) & 0xFFFFFFFF
        return header + payload + struct.pack("!I", crc)

    @classmethod
    def decode_frame(cls, raw_bytes: bytes) -> Tuple[int, bytes]:
        """Validates magic header, length, and CRC32 before returning payload."""
        if len(raw_bytes) < 14:
            raise ValueError("Buffer too small for minimum Raft frame header")

        magic, version, msg_type, payload_len = struct.unpack("!IBBI", raw_bytes[:10])
        if magic != cls.MAGIC_HEADER:
            raise ValueError(f"Invalid wire protocol magic: 0x{magic:08X}")

        if len(raw_bytes) < 10 + payload_len + 4:
            raise ValueError("Incomplete frame received")

        payload = raw_bytes[10:10 + payload_len]
        received_crc = struct.unpack("!I", raw_bytes[10 + payload_len:14 + payload_len])[0]

        expected_crc = zlib.crc32(raw_bytes[:10 + payload_len]) & 0xFFFFFFFF
        if received_crc != expected_crc:
            raise ValueError(f"CRC32 mismatch: expected 0x{expected_crc:08X}, got 0x{received_crc:08X}")

        return msg_type, payload
