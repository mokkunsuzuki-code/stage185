# MIT License © 2025 Motohiro Suzuki
from __future__ import annotations

import json
from pathlib import Path

PATH = Path("out/audit.jsonl")


def main() -> None:
    if not PATH.exists():
        print("[NO LOG]", PATH)
        return

    for line in PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        ts = e.get("ts_ms", "?")
        ev = e.get("event", "?")
        role = e.get("role", "-")
        ft = e.get("frame_type", "-")
        msg = ""
        if ev == "FRAME_ERR":
            msg = f"{e.get('err_type')} {e.get('err')}"
        elif ev == "FRAME_IN":
            msg = f"payload_len={e.get('payload_len')}"
        elif ev == "FRAME_OUT":
            msg = f"out_len={e.get('out_len')}"
        else:
            # SESSION_NEW etc.
            extras = {k: v for k, v in e.items() if k not in ("ts_ms", "event")}
            msg = json.dumps(extras, ensure_ascii=False)

        print(f"{ts}  {ev:10}  role={role:6}  ft={ft:10}  {msg}")


if __name__ == "__main__":
    main()
