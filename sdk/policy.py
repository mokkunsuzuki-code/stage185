# MIT License © 2025 Motohiro Suzuki
from dataclasses import dataclass


@dataclass(frozen=True)
class Policy:
    """
    Stage185(C強化) Policy:
    - fail_closed: any decode/auth mismatch => hard close (no silent continue)
    - require_qkd: if True, forbid PQC_ONLY mode (demo uses False)
    - allow_downgrade: if False, reject a peer trying to force PQC_ONLY if we started QKD_MIXED
    - rekey_bytes/rekey_seconds: basic triggers (demo uses manual)
    """
    fail_closed: bool = True
    require_qkd: bool = False
    allow_downgrade: bool = False
    rekey_bytes: int = 1_000_000
    rekey_seconds: int = 3600
