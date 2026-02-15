# MIT License © 2025 Motohiro Suzuki
from __future__ import annotations

import os
import secrets
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .audit import AuditSink, audit_event
from .policy import Policy


def _rand_session_id() -> str:
    return secrets.token_hex(8)


@dataclass
class Session:
    """
    Minimal Session state for Stage185 SDK wrapper.

    NOTE:
    - This is a self-contained demo-grade engine (AESGCM + HKDF).
    - In your real QSP repo, you’ll later replace _derive_keys() with your true handshake/rekey core.
    """
    role: str  # "client" or "server"
    policy: Policy
    session_id: str = field(default_factory=_rand_session_id)
    epoch: int = 1
    mode: str = "QKD_MIXED"  # or "PQC_ONLY"
    audit: Optional[AuditSink] = None

    # symmetric keys
    tx_key: bytes = field(default_factory=lambda: b"")
    rx_key: bytes = field(default_factory=lambda: b"")

    # internal counters
    bytes_sent: int = 0
    bytes_recv: int = 0

    def close(self, reason: str) -> None:
        audit_event(
            self.audit,
            session_id=self.session_id,
            epoch=self.epoch,
            mode=self.mode,
            event_type="CLOSE",
            reason=reason,
            detail="fail-closed session termination",
        )
        # zeroize best-effort
        self.tx_key = b""
        self.rx_key = b""

    def set_audit_path(self, path: str | os.PathLike) -> None:
        self.audit = AuditSink(Path(path))

    def log(self, event_type: str, reason: str = "", detail: str = "") -> None:
        audit_event(
            self.audit,
            session_id=self.session_id,
            epoch=self.epoch,
            mode=self.mode,
            event_type=event_type,
            reason=reason,
            detail=detail,
        )
