# MIT License © 2025 Motohiro Suzuki
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from qsp.core import ProtocolCore

from sdk.audit import append_event


@dataclass
class QspSession:
    role: str  # "client" | "server"
    core: ProtocolCore


def session_new(role: str, *, handshake_complete: bool = False) -> QspSession:
    if role not in ("client", "server"):
        raise ValueError("role must be 'client' or 'server'")
    s = QspSession(role=role, core=ProtocolCore(handshake_complete=handshake_complete))
    append_event({"event": "SESSION_NEW", "role": role, "handshake_complete": bool(handshake_complete)})
    return s


def send_frame(sess: QspSession, frame_type: str, payload: bytes = b"") -> bytes:
    if not isinstance(payload, (bytes, bytearray)):
        raise TypeError("payload must be bytes-like")

    ft = str(frame_type)
    pl = bytes(payload)

    append_event({"event": "FRAME_IN", "role": sess.role, "frame_type": ft, "payload_len": len(pl)})

    try:
        out = sess.core.accept_frame(frame_type=ft, payload=pl)
        append_event({"event": "FRAME_OUT", "role": sess.role, "frame_type": ft, "out_len": len(out)})
        return out
    except Exception as e:
        append_event(
            {
                "event": "FRAME_ERR",
                "role": sess.role,
                "frame_type": ft,
                "err_type": type(e).__name__,
                "err": str(e),
            }
        )
        raise
