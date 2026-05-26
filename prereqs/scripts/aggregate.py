#!/usr/bin/env python3
"""Aggregate run results into summary.csv."""
import csv
import json
import os
from pathlib import Path

RUNS = Path(os.environ.get("RUNS_ROOT", "runs"))
OUT = Path(os.environ.get("SUMMARY_OUT", "summary.csv"))

rows = []
for rj in RUNS.rglob("run.json"):
    data = json.loads(rj.read_text())
    diff_path = rj.parent / "changes.diff"
    if diff_path.exists():
        diff = diff_path.read_text()
        data["lines_added"] = sum(
            1 for line in diff.splitlines()
            if line.startswith("+") and not line.startswith("+++")
        )
        data["lines_removed"] = sum(
            1 for line in diff.splitlines()
            if line.startswith("-") and not line.startswith("---")
        )
        data["files_touched"] = sum(
            1 for line in diff.splitlines() if line.startswith("diff --git")
        )
    prompt_path = rj.parent / "final_prompt.txt"
    if prompt_path.exists():
        data["prompt_chars"] = len(prompt_path.read_text())
    rows.append(data)

if not rows:
    print("no runs found")
    raise SystemExit(0)

fields = sorted({k for r in rows for k in r})
with OUT.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
print(f"wrote {len(rows)} rows → {OUT}")
