#!/usr/bin/env bash
set -euo pipefail

# MIT License © 2025 Motohiro Suzuki
# Attack-01: downgrade attempt
# - local starts QKD_MIXED
# - attacker forces PQC_ONLY flag in wire
# Expected: ATTACK_DETECTED + fail-closed

python - << 'PY'
from sdk import session_start, send, recv
from sdk.framing import parse_frame, build_header, MSG_APP_DATA

alice = session_start("client")
bob = session_start("server")

wire = send(alice, b"hello")
header, pf = parse_frame(wire)

# force PQC_ONLY flag bit0=1
forced_flags = pf.flags | 1
new_header = build_header(msg_type=MSG_APP_DATA, flags=forced_flags, epoch=pf.epoch, nonce=pf.nonce, ct_len=len(pf.ciphertext))
tampered = new_header + pf.ciphertext

try:
    recv(bob, tampered)
    print("[NG] downgrade was accepted (unexpected)")
except Exception as e:
    print("[OK] downgrade rejected:", str(e))
PY
