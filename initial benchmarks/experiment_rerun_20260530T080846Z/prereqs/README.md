# Hermes + Fabric + Codex — Prereqs and Runbook

## 1. Setup

```bash
./install.sh
hermes auth add openai-codex          # one-time
mkdir -p ~/.config/fabric/patterns/codex_brief
cp patterns/codex_brief/system.md ~/.config/fabric/patterns/codex_brief/system.md
```

Confirm:
```bash
hermes --version && fabric --listpatterns | grep codex_brief && codex --version
```

## 2. Fixture layout

Each `fixtures/taskNN_*/` is a self-contained mini-project:

- `prompt.txt` — the raw user prompt for this task (1–2 lines)
- `pattern.txt` — the Fabric pattern name used by the `fabric` variant
- `brief.md` — hand-crafted task brief: scope, forbidden paths, done-criteria, verification (the ceiling for the `brief` variant)
- source files matching what the prompt expects (paths line up exactly)
- a git repo with a `baseline` tag (created by `reset.sh --init`)

Initialize all fixtures once:
```bash
./scripts/reset.sh --init
```

This `git init`s each fixture and tags `baseline`. After every run, `reset.sh <task_id>` rewinds it.

## 3. Running a single experiment

```bash
./scripts/run_task.sh task05_dry_run_flag fabric
```

Variants:
- `raw` — pure Codex, no Fabric, no Hermes (control / floor)
- `brief` — hand-crafted task brief (`fixtures/<task>/brief.md`) shipped directly to Codex (ceiling: what perfect prompt engineering looks like)
- `hermes` — Hermes session, no Fabric
- `fabric` — Fabric pattern from `pattern.txt`, then Codex
- `fabric-improve` — `improve_prompt` → `codex_brief` → Codex
- `fabric-stitch` — `create_prd` → `improve_prompt` → `codex_brief` → Codex
- `hermes-fabric` — your target stack

The key comparison: **how close does `fabric-improve` get to `brief`?** That delta tells you whether Fabric is recovering the value of hand-crafted prompts or leaving it on the table.

Each run writes to `runs/<task>/<variant>/<ts>/`:
- `final_prompt.txt` — actual text shipped to Codex
- `codex.log` — full stdout/stderr
- `changes.diff` — `git diff` of the fixture after the run
- `pytest.log` — test output if tests exist
- `run.json` — latency, exit code

## 4. Running the full matrix

```bash
for task in fixtures/task*/; do
  task_id=$(basename "$task")
  for variant in raw brief hermes fabric fabric-improve hermes-fabric; do
    ./scripts/reset.sh "$task_id"
    ./scripts/run_task.sh "$task_id" "$variant"
  done
done
python scripts/aggregate.py     # → summary.csv
```

Recommend 3 trials per (task, variant) for variance bars.

## 5. Scoring outputs

For read-only tasks (1, 2): manual rubric. For everything else, two automatic signals:

1. **Tests pass** — `pytest -x` in the fixture after the run (the runner does this).
2. **Judge score** — pipe `codex.log` through Fabric's `rate_ai_result`:
   ```bash
   cat runs/task05_dry_run_flag/fabric/*/codex.log | \
       fabric -p rate_ai_result -m gpt-5 > judge.txt
   ```

Add the judge score as a column when aggregating.

## 6. What to document per run

The fields from the benchmark plan section 5. The runner emits most automatically; `correctness_score` and `judge_score` are filled in after.

## 7. Common pitfalls

- **Codex refuses outside a git repo** — that's why every fixture is `git init`ed.
- **Sandbox profile** — `--full-auto` (used by the runner) keeps writes inside the workspace without per-step prompts.
- **Cache bias** — Hermes caches prompt prefixes. Run `raw` first as warmup and discard, or disable cache for measurement.
- **Path resolution** — fixtures use a `conftest.py` for `sys.path`. Run pytest from the fixture root.
