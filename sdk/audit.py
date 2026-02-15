# MIT License © 2025 Motohiro Suzuki
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

DEFAULT_AUDIT_PATH = Path("out/audit.jsonl")


def _now_ms() -> int:
    return int(time.time() * 1000)


def append_event(event: Dict[str, Any], path: Path = DEFAULT_AUDIT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    event = dict(event)
    event.setdefault("ts_ms", _now_ms())
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
