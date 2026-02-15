# MIT License © 2025 Motohiro Suzuki
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

PATH = Path("out/audit.jsonl")


def load_events() -> List[Dict[str, Any]]:
    if not PATH.exists():
        return []
    out: List[Dict[str, Any]] = []
    for line in PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        out.append(json.loads(line))
    return out


def main() -> None:
    evs = load_events()
    if not evs:
        print("[NO LOG]", PATH)
        return

    n_in = sum(1 for e in evs if e.get("event") == "FRAME_IN")
    n_out = sum(1 for e in evs if e.get("event") == "FRAME_OUT")
    n_err = sum(1 for e in evs if e.get("event") == "FRAME_ERR")

    # Claim A1 evidence: APP_DATA rejected before handshake
    a1 = [
        e for e in evs
        if e.get("event") == "FRAME_ERR"
        and e.get("frame_type") == "APP_DATA"
        and "handshake not complete" in str(e.get("err", ""))
    ]

    print("=== Stage185 Audit Summary ===")
    print("log_path:", PATH)
    print("events:", len(evs))
    print("frame_in:", n_in)
    print("frame_out:", n_out)
    print("frame_err:", n_err)
    print()

    print("=== Evidence: Claim A1 (fail-closed before handshake) ===")
    if not a1:
        print("[MISSING] No Claim A1 rejection found")
    else:
        # print first evidence line compactly
        e = a1[0]
        print("[OK] APP_DATA rejected before handshake")
        print(" ts_ms:", e.get("ts_ms"))
        print(" err :", e.get("err_type"), e.get("err"))
    print()

    print("=== README snippet (copy/paste) ===")
    if a1:
        e = a1[0]
        ts = e.get("ts_ms")
        print("- Evidence (Stage185): `APP_DATA` is rejected before handshake (Claim A1).")
        print(f"  - audit.ts_ms={ts}, event=FRAME_ERR, frame_type=APP_DATA, err={e.get('err_type')}: {e.get('err')}")
    else:
        print("- Evidence (Stage185): (no Claim A1 line found)")

    print()


if __name__ == "__main__":
    main()
