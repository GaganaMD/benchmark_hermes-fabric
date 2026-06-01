# Artifact Relationship Map

raw_prompt (prereqs/fixtures/task01_explain_jwt/prompt.txt)
  -> transformation (pattern: explain_code)
  -> final_prompt.txt per variant
  -> codex.log per variant
  -> changes.diff + run.json per variant

run orchestration logs (logs/*.log)
  -> execution status and latency

runtime exports roots
  -> runtime_exports/prereqs_runs_snapshot
  -> runtime_exports/prereqs/runs/task01_explain_jwt
  -> runtime_exports/.hermes/sessions (recent)
  -> runtime_exports/bridge/out/logs + temp/runtime/cache (recent if present)

benchmark_row.json
  -> normalized row for tabulation

artifact_inventory.md
  -> file-level ledger with size + hash prefixes