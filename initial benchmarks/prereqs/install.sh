#!/usr/bin/env bash
set -euo pipefail

echo "[1/4] Hermes Agent"
if ! command -v hermes >/dev/null; then
  curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
fi

echo "[2/4] Fabric"
if ! command -v fabric >/dev/null; then
  go install github.com/danielmiessler/fabric@latest
fi

echo "[3/4] Codex CLI"
if ! command -v codex >/dev/null; then
  npm install -g @openai/codex
fi

echo "[4/4] Python deps"
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --quiet pytest pyjwt click

echo
echo "Done. Next: hermes auth add openai-codex"
echo "Then:  cp patterns/codex_brief/system.md ~/.config/fabric/patterns/codex_brief/"
