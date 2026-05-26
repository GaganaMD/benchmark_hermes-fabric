#!/usr/bin/env bash
set -euo pipefail

TASK="${1:?task_id required}"
VARIANT="${2:?variant required}"
TRIAL="${3:-1}"
TS=$(date -u +%Y%m%dT%H%M%SZ)
RUNS_ROOT="${RUNS_ROOT:-runs}"
OUT="$RUNS_ROOT/$TASK/$VARIANT/trial${TRIAL}_${TS}"
mkdir -p "$OUT"

FIX="fixtures/$TASK"
RAW=$(cat "$FIX/prompt.txt")
PATTERN=$(cat "$FIX/pattern.txt" 2>/dev/null || echo "")

case "$VARIANT" in
  raw|hermes)       FINAL="$RAW" ;;
  brief)            FINAL=$(cat "$FIX/brief.md") ;;
  fabric|hermes-fabric)
                    FINAL=$(echo "$RAW" | fabric -p "$PATTERN") ;;
  fabric-improve)   FINAL=$(echo "$RAW" | fabric -p improve_prompt | fabric -p codex_brief) ;;
  fabric-stitch)    FINAL=$(echo "$RAW" | fabric -p create_prd | fabric -p improve_prompt | fabric -p codex_brief) ;;
  *) echo "unknown variant: $VARIANT"; exit 1 ;;
esac

echo "$FINAL" > "$OUT/final_prompt.txt"

START=$(date +%s%N)
case "$VARIANT" in
  hermes|hermes-fabric)
    ( cd "$FIX" && hermes -z "$FINAL" chat ) 2>&1 | tee "$OUT/codex.log" >/dev/null
    ;;
  *)
    ( cd "$FIX" && codex exec --full-auto "$FINAL" ) 2>&1 | tee "$OUT/codex.log" >/dev/null
    ;;
esac
END=$(date +%s%N)
LATENCY_MS=$(( (END - START) / 1000000 ))

( cd "$FIX" && git diff > "../../$OUT/changes.diff" )

TESTS_RC="na"
if [[ -d "$FIX/tests" ]]; then
  if ( cd "$FIX" && pytest -x --tb=short ) > "$OUT/pytest.log" 2>&1; then
    TESTS_RC=0
  else
    TESTS_RC=$?
  fi
fi

cat > "$OUT/run.json" <<JSON
{
  "task_id": "$TASK",
  "variant": "$VARIANT",
  "trial": $TRIAL,
  "ts": "$TS",
  "total_ms": $LATENCY_MS,
  "tests_exit_code": "$TESTS_RC"
}
JSON

echo "done: $OUT  (${LATENCY_MS}ms, tests=$TESTS_RC)"
