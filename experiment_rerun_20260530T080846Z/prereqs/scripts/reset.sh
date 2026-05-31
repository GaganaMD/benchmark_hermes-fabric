#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "--init" ]]; then
  for d in fixtures/task*/; do
    ( cd "$d"
      git init -q
      git add -A
      git -c user.email=bench@local -c user.name=bench commit -q -m "baseline" || true
      git tag -f baseline >/dev/null
    )
    echo "init: $d"
  done
  exit 0
fi

TASK="${1:-}"
[[ -z "$TASK" ]] && { echo "usage: reset.sh <task_id> | --init"; exit 1; }
( cd "fixtures/$TASK"
  git reset --hard baseline -q
  git clean -fdq
)
echo "reset: $TASK"
