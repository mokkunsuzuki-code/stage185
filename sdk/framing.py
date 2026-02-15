# MIT License © 2025 Motohiro Suzuki
from __future__ import annotations

import struct
from dataclasses import dataclass
from typing import Tuple

MAGIC = b"QSP1"

# Frame format (minimal):
# MAGIC(4) | version(1)=1 | msg_type(1) | flags(1) | epoch(u32) | nonce(12) | ct_len(u32) | ciphertext(ct_len)
#
# msg_type:
#   1 = APP_DATA
#   2 = REKEY_TICK (optional; demo uses explicit rekey() API not wire)
#
# flags bit0: mode_is_pqc_only (1 => PQC_ONLY, 0 => QKD_MIXED)
#
# ciphertext is AEAD output (ct+tag) from AESGCM; aad covers header fields (except ct itself).

VERSION = 1
MSG_APP_DATA = 1

HEADER_FMT = "!4sBBBBI12sI"  # magic, ver, type, flags, reserved, epoch, nonce, ct_len
HEADER_LEN = struct.calcsize(HEADER_FMT)


@dataclass(frozen=True)
class ParsedFrame:
    msg_type: int
    flags: int
    epoch: int
    nonce: bytes
    ciphertext: bytes


def build_header(*, msg_type: int, flags: int, epoch: int, nonce: bytes, ct_len: int) -> bytes:
    if len(nonce) != 12:
        raise ValueError("nonce must be 12 bytes for AESGCM")
    reserved = 0
    return struct.pack(HEADER_FMT, MAGIC, VERSION, msg_type, flags, reserved, epoch, nonce, ct_len)


def parse_frame(wire: bytes) -> Tuple[bytes, ParsedFrame]:
    if len(wire) < HEADER_LEN:
        raise ValueError("wire too short")
    magic, ver, msg_type, flags, _reserved, epoch, nonce, ct_len = struct.unpack(
        HEADER_FMT, wire[:HEADER_LEN]
    )
    if magic != MAGIC:
        raise ValueError("bad magic")
    if ver != VERSION:
        raise ValueError("bad version")
    if len(wire) != HEADER_LEN + ct_len:
        raise ValueError("length mismatch")
    ciphertext = wire[HEADER_LEN:]
    header = wire[:HEADER_LEN]
    return header, ParsedFrame(msg_type=msg_type, flags=flags, epoch=epoch, nonce=nonce, ciphertext=ciphertext)
