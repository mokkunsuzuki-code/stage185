#!/usr/bin/env bash
# MIT License © 2025 Motohiro Suzuki
set -euo pipefail

cd "$(dirname "$0")/.."

mkdir -p out

# fresh logs / outputs
rm -f \
  out/audit.jsonl \
  out/audit_print.txt \
  out/audit_timeline.txt \
  out/audit_summary.txt \
  out/demo_output.txt \
  out/evidence_pack.txt

# Run the minimal demo (captures stdout; keep going even if demo exits non-zero)
python -m examples.ten_lines_demo | tee out/demo_output.txt >/dev/null || true

# Produce human-readable and summarized evidence artifacts
python tools/print_audit.py   | tee out/audit_print.txt >/dev/null
python tools/plot_audit.py    | tee out/audit_timeline.txt >/dev/null
python tools/audit_summary.py | tee out/audit_summary.txt >/dev/null

# Write a small manifest/explanation bundle
cat > out/evidence_pack.txt << 'TXT'
Stage185 Evidence Pack
======================

This pack demonstrates a minimal fail-closed property (Claim A1) using the Stage178 public entrypoint:
  - qsp.core.ProtocolCore.accept_frame()

Artifacts:
  - out/demo_output.txt       : demo stdout
  - out/audit.jsonl           : machine-readable audit log (JSONL)
  - out/audit_print.txt       : human-readable audit log
  - out/audit_timeline.txt    : ASCII timeline visualization
  - out/audit_summary.txt     : summary + README snippet
  - out/evidence_pack.txt     : this explanation

How to reproduce:
  source .venv/bin/activate
  python -m pip install -e ../stage178 --upgrade
  python -m pip install -e . --upgrade
  python tools/make_evidence_pack.sh
TXT

echo "[OK] wrote out/evidence_pack.txt"
echo "[OK] wrote out/audit.jsonl out/audit_print.txt out/audit_timeline.txt out/audit_summary.txt out/demo_output.txt"
