# Stage185 — Minimal SDK + Evidence (Claim A1)

Stage185 provides a minimal, public-entry SDK layer on top of Stage178
and demonstrates a reproducible security property:

> Claim A1 — Fail-Closed:
> `APP_DATA` is rejected before handshake completion.

This stage does **not modify Stage178 logic**.
It wraps the public entrypoint:

qsp.core.ProtocolCore.accept_frame()


and generates machine-verifiable audit evidence.

---

## 🔁 Repro (Stage185)

```bash
cd ~/Desktop/test/stage185
source .venv/bin/activate

# install Stage178 (core)
python -m pip install -e ../stage178 --upgrade

# install Stage185 SDK
python -m pip install -e . --upgrade

# run demo + generate evidence pack
python tools/make_evidence_pack.sh
After execution, the following files are generated:

out/
 ├── audit.jsonl          # machine-readable audit log
 ├── audit_print.txt      # human-readable log
 ├── audit_summary.txt    # summarized evidence
 ├── demo_output.txt      # demo stdout
 └── evidence_pack.txt    # explanation bundle
🧪 Evidence (Claim A1 — Fail-Closed)
Security property demonstrated:

APP_DATA before handshake → rejected

handshake via HS

APP_DATA after handshake → accepted

Example evidence (from audit log):

event=FRAME_ERR
frame_type=APP_DATA
error=ProtocolViolation: APP_DATA rejected: handshake not complete (Claim A1)
Then:

event=FRAME_OUT
frame_type=HS
Then:

event=FRAME_OUT
frame_type=APP_DATA
This proves:

✔ Fail-closed before handshake
✔ Handshake completion toggles state
✔ APP_DATA allowed only after handshake

🎯 Architectural Position
Stage185 is:

A minimal SDK wrapper

Public API surface definition

Evidence generation layer

Research reproducibility scaffold

It intentionally keeps Stage178 untouched.

📦 Design Goal
“Do not steal the reviewer’s time.”

Anyone can:

Clone

Run 1 command

See security evidence

No QKD device required.
No network required.
No external dependencies required.

📜 License
MIT License © 2025 Motohiro Suzuki