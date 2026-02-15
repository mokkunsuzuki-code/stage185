# MIT License © 2025 Motohiro Suzuki
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default="out/audit.jsonl")
    args = ap.parse_args()

    p = Path(args.path)
    if not p.exists():
        raise SystemExit(f"not found: {p}")

    events = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            events.append(json.loads(line))

    cnt = Counter(e.get("event_type", "UNKNOWN") for e in events)

    # epoch progression per session
    epochs = defaultdict(list)
    modes = defaultdict(list)
    for e in events:
        sid = e.get("session_id", "?")
        epochs[sid].append(int(e.get("epoch", 0)))
        modes[sid].append(e.get("mode", "?"))

    print("=== Audit Summary ===")
    for k, v in cnt.most_common():
        print(f"{k}: {v}")

    print("\n=== Per Session ===")
    for sid in sorted(epochs.keys()):
        ep = epochs[sid]
        md = modes[sid]
        ep_min, ep_max = (min(ep), max(ep)) if ep else (0, 0)
        print(f"- session_id={sid}")
        print(f"  epoch range: {ep_min} -> {ep_max}")
        if md:
            # show mode transitions compactly
            trans = []
            last = None
            for m in md:
                if m != last:
                    trans.append(m)
                    last = m
            print(f"  mode transitions: {' -> '.join(trans)}")
        print()

if __name__ == "__main__":
    main()
