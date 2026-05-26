#!/usr/bin/env bash
set -euo pipefail

ROOT="/c/Users/gagan/Desktop/benchmark_hermes+fabric"
PRE="$ROOT/prereqs"
RUN_ID="${RUN_ID:-overnight_$(date -u +%Y%m%dT%H%M%SZ)}"
RUNS_ROOT_REL="runs_isolated/$RUN_ID"
RUNS_ROOT_ABS="$PRE/$RUNS_ROOT_REL"
LOGDIR="$ROOT/benchmarks/logs/$RUN_ID"
RUN_TIMEOUT_SEC="${RUN_TIMEOUT_SEC:-600}"

mkdir -p "$LOGDIR" "$RUNS_ROOT_ABS" "$ROOT/benchmarks/aggregate/$RUN_ID"
cd "$PRE"

# Validate task00_greeting fixture exists and capture one-time sanity artifacts (not part of strict 50 cells)
for f in fixtures/task00_greeting/prompt.txt fixtures/task00_greeting/pattern.txt fixtures/task00_greeting/brief.md; do
  [[ -f "$f" ]] || { echo "missing_fixture_file: $f" | tee -a "$LOGDIR/matrix_strict50.log"; exit 1; }
done
echo "task00_greeting fixture present" | tee -a "$LOGDIR/matrix_strict50.log"
cp fixtures/task00_greeting/prompt.txt "$LOGDIR/task00_prompt.txt"
cp fixtures/task00_greeting/pattern.txt "$LOGDIR/task00_pattern.txt"
cp fixtures/task00_greeting/brief.md "$LOGDIR/task00_brief.md"

# 10 benchmark tasks × 5 variants = strict 50 cells
TASKS=(
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
VARIANTS=(raw hermes fabric fabric-stitch hermes-fabric)

./scripts/reset.sh --init >> "$LOGDIR/reset_init.log" 2>&1

for task in "${TASKS[@]}"; do
  for variant in "${VARIANTS[@]}"; do
    ./scripts/reset.sh "$task" >> "$LOGDIR/matrix_strict50.log" 2>&1 || true
    RUNS_ROOT="$RUNS_ROOT_REL" timeout "$RUN_TIMEOUT_SEC" ./scripts/run_task.sh "$task" "$variant" 1 >> "$LOGDIR/matrix_strict50.log" 2>&1 || {
      rc=$?
      echo "run_timeout_or_fail task=$task variant=$variant rc=$rc" >> "$LOGDIR/matrix_strict50.log"
    }
  done
done

RUNS_ROOT="$RUNS_ROOT_REL" SUMMARY_OUT="$LOGDIR/summary_strict50.csv" python ./scripts/aggregate.py >> "$LOGDIR/aggregate.log" 2>&1 || true
cp "$LOGDIR/summary_strict50.csv" "$ROOT/benchmarks/aggregate/$RUN_ID/summary_strict50.csv" 2>/dev/null || true

echo "run_id=$RUN_ID" | tee -a "$LOGDIR/matrix_strict50.log"
echo "runs_root=$RUNS_ROOT_REL" | tee -a "$LOGDIR/matrix_strict50.log"
echo "summary=$LOGDIR/summary_strict50.csv" | tee -a "$LOGDIR/matrix_strict50.log"
