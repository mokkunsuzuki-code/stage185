# MIT License © 2025 Motohiro Suzuki
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

LOG_PATH = Path("out/audit.jsonl")


@dataclass
class Ev:
    ts_ms: int
    event: str
    role: str
    frame_type: str
    payload_len: Optional[int] = None
    out_len: Optional[int] = None
    err_type: Optional[str] = None
    err: Optional[str] = None


def _load_events(path: Path) -> List[Ev]:
    if not path.exists():
        return []
    out: List[Ev] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        d: Dict[str, Any] = json.loads(line)
        out.append(
            Ev(
                ts_ms=int(d.get("ts_ms", 0)),
                event=str(d.get("event", "")),
                role=str(d.get("role", "-")),
                frame_type=str(d.get("frame_type", "-")),
                payload_len=d.get("payload_len"),
                out_len=d.get("out_len"),
                err_type=d.get("err_type"),
                err=d.get("err"),
            )
        )
    out.sort(key=lambda e: e.ts_ms)
    return out


def _fmt_ms(ts0: int, ts: int) -> str:
    return f"+{(ts - ts0):>4}ms"


def _short(s: Optional[str], n: int = 72) -> str:
    if not s:
        return ""
    s = s.replace("\n", " ").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def _glyph(e: Ev) -> str:
    if e.event == "FRAME_IN":
        return "→"
    if e.event == "FRAME_OUT":
        return "✓"
    if e.event == "FRAME_ERR":
        return "✗"
    return "·"


def _label(e: Ev) -> str:
    # compact label that “reads” quickly
    if e.event == "FRAME_IN":
        pl = f"payload={e.payload_len}" if e.payload_len is not None else "payload=?"
        return f"{e.frame_type}  {pl}"
    if e.event == "FRAME_OUT":
        ol = f"out={e.out_len}" if e.out_len is not None else "out=?"
        return f"{e.frame_type}  {ol}"
    if e.event == "FRAME_ERR":
        return f"{e.frame_type}  {e.err_type}: {_short(e.err, 60)}"
    return f"{e.frame_type}"


def _group_by_role(evs: List[Ev]) -> Dict[str, List[Ev]]:
    g: Dict[str, List[Ev]] = {}
    for e in evs:
        # ignore SESSION_NEW etc; focus on the requested 3
        if e.event not in ("FRAME_IN", "FRAME_OUT", "FRAME_ERR"):
            continue
        g.setdefault(e.role, []).append(e)
    return g


def _render_single_stream(role: str, evs: List[Ev]) -> None:
    if not evs:
        print(f"[NO EVENTS] role={role}")
        return

    ts0 = evs[0].ts_ms
    print(f"\n=== ASCII Timeline (role={role}) ===")
    print("Legend:  → FRAME_IN   ✓ FRAME_OUT   ✗ FRAME_ERR")
    print("-" * 78)

    for i, e in enumerate(evs, 1):
        dt = _fmt_ms(ts0, e.ts_ms)
        sym = _glyph(e)
        lab = _label(e)
        print(f"{i:02d}  {dt}  {sym}  {lab}")

    print("-" * 78)

    # quick human verdict lines (useful for README / reviewers)
    has_a1 = any(
        (e.event == "FRAME_ERR" and e.frame_type == "APP_DATA" and e.err and "handshake not complete" in e.err)
        for e in evs
    )
    has_hs_ok = any((e.event == "FRAME_OUT" and e.frame_type == "HS") for e in evs)
    has_app_ok = any((e.event == "FRAME_OUT" and e.frame_type == "APP_DATA") for e in evs)

    print("Summary:")
    print(f" - Claim A1 (APP_DATA before HS rejected): {'PASS' if has_a1 else 'MISSING'}")
    print(f" - HS success: {'YES' if has_hs_ok else 'NO'}")
    print(f" - APP_DATA after HS accepted: {'YES' if has_app_ok else 'NO'}")


def main() -> None:
    evs = _load_events(LOG_PATH)
    if not evs:
        print("[NO LOG]", LOG_PATH)
        print("Run: python tools/make_evidence_pack.sh  (or python -m examples.ten_lines_demo)")
        return

    by_role = _group_by_role(evs)
    if not by_role:
        print("[NO FRAME EVENTS]", LOG_PATH)
        return

    # Render each role stream (most Stage185 runs will have only "server")
    for role in sorted(by_role.keys()):
        _render_single_stream(role, by_role[role])


if __name__ == "__main__":
    main()
