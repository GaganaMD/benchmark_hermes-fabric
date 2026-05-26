#!/usr/bin/env bash
set -uo pipefail

ROOT="/c/Users/gagan/Desktop/benchmark_hermes+fabric"
PRE="$ROOT/prereqs"
LOGDIR="$ROOT/benchmarks/logs"
RUN_TIMEOUT_SEC="${RUN_TIMEOUT_SEC:-600}"
mkdir -p "$LOGDIR"

cd "$PRE"
./scripts/reset.sh --init >> "$LOGDIR/reset_init.log" 2>&1

# Required modes from prompt.txt
# RAW -> raw
# FABRIC -> fabric
# FABRIC_CUSTOM -> fabric-improve (task10 uses stitch per requirement)
# OPTIONAL_ABLATION -> raw_ablation (codex raw + no retry loop/no additional verification)

TASKS=(
  task00_greeting
  task01_explain_jwt
  task02_signup_flow
  task03_failing_test
  task04_input_validation
  task05_dry_run_flag
  task06_signature_change
  task07_print_to_logger
  task08_config_migration
  task09_flaky_workers
  task10_fm_cli
)

for task in "${TASKS[@]}"; do
  ./scripts/reset.sh "$task" >> "$LOGDIR/matrix.log" 2>&1 || true
  timeout "$RUN_TIMEOUT_SEC" ./scripts/run_task.sh "$task" raw 1 >> "$LOGDIR/matrix.log" 2>&1 || echo "run_timeout_or_fail task=$task variant=raw rc=$?" >> "$LOGDIR/matrix.log"

  ./scripts/reset.sh "$task" >> "$LOGDIR/matrix.log" 2>&1 || true
  timeout "$RUN_TIMEOUT_SEC" ./scripts/run_task.sh "$task" fabric 1 >> "$LOGDIR/matrix.log" 2>&1 || echo "run_timeout_or_fail task=$task variant=fabric rc=$?" >> "$LOGDIR/matrix.log"

  ./scripts/reset.sh "$task" >> "$LOGDIR/matrix.log" 2>&1 || true
  if [[ "$task" == "task10_fm_cli" ]]; then
    timeout "$RUN_TIMEOUT_SEC" ./scripts/run_task.sh "$task" fabric-stitch 1 >> "$LOGDIR/matrix.log" 2>&1 || echo "run_timeout_or_fail task=$task variant=fabric-stitch rc=$?" >> "$LOGDIR/matrix.log"
  elif [[ "$task" == "task09_flaky_workers" ]]; then
    timeout "$RUN_TIMEOUT_SEC" ./scripts/run_task.sh "$task" fabric-improve 1 >> "$LOGDIR/matrix.log" 2>&1 || echo "run_timeout_or_fail task=$task variant=fabric-improve rc=$?" >> "$LOGDIR/matrix.log"
  else
    timeout "$RUN_TIMEOUT_SEC" ./scripts/run_task.sh "$task" fabric-improve 1 >> "$LOGDIR/matrix.log" 2>&1 || echo "run_timeout_or_fail task=$task variant=fabric-improve rc=$?" >> "$LOGDIR/matrix.log"
  fi

  # optional ablation: intentionally no retries/planning wrapper
  ./scripts/reset.sh "$task" >> "$LOGDIR/matrix.log" 2>&1 || true
  TS=$(date -u +%Y%m%dT%H%M%SZ)
  OUT="runs/$task/optional-ablation/trial1_${TS}"
  mkdir -p "$OUT"
  RAW=$(cat "fixtures/$task/prompt.txt")
  echo "$RAW" > "$OUT/final_prompt.txt"
  START=$(date +%s%N)
  timeout "$RUN_TIMEOUT_SEC" bash -lc "cd 'fixtures/$task' && codex exec --full-auto \"$RAW\"" > "$OUT/codex.log" 2>&1
  rc=$?
  if [ $rc -ne 0 ]; then
    echo "run_timeout_or_fail task=$task variant=optional-ablation rc=$rc" >> "$LOGDIR/matrix.log"
  fi
  END=$(date +%s%N)
  LATENCY_MS=$(( (END - START) / 1000000 ))
  ( cd "fixtures/$task" && git diff > "../../$OUT/changes.diff" ) || true
  cat > "$OUT/run.json" <<JSON
{"task_id":"$task","variant":"optional-ablation","trial":1,"ts":"$TS","total_ms":$LATENCY_MS,"tests_exit_code":"na"}
JSON

done

python scripts/aggregate.py > "$LOGDIR/aggregate.log" 2>&1 || true
cp summary.csv "$ROOT/benchmarks/aggregate/summary.csv" 2>/dev/null || true
