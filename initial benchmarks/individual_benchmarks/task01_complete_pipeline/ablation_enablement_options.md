# OPTIONAL_ABLATION enablement options

## Can the blocker be removed?
Yes, likely removable, but root cause must be isolated first (sandbox init vs shell path resolution).

## Is it safe to remove?
Partially.
- Safe: fix shell path/tooling and keep sandboxing.
- Higher risk: disabling/weakening sandbox controls globally.

## Enablement options (ranked)

### Option A (preferred): keep sandbox, fix shell/tool path compatibility
What to change:
1. Ensure Codex exec uses a valid shell path available in sandbox context.
2. Avoid hard-coded `C:\Program Files\7\pwsh.exe` dependency if not guaranteed.
3. Validate simple read command execution in same fixture before ablation run.

Pros:
- Preserves security posture.
- Addresses likely trigger directly.

Cons:
- Requires Codex runtime/shell configuration inspection.

Risk:
- Low-to-moderate.

Runtime/resource impact:
- Negligible.

### Option B: keep shell path, adjust Codex sandbox/approval mode for this run only
What to change:
- Run ablation with a less restrictive execution profile (if supported), scoped to the benchmark run only.

Pros:
- May bypass spawn-refresh issue quickly.

Cons:
- Reduced containment.
- May violate reproducibility/security policy depending governance.

Risk:
- Moderate to high (security/isolation).

Runtime/resource impact:
- Low.

### Option C: replace shell-dependent inspection with non-shell MCP/file APIs
What to change:
- Force Codex workflow that reads files without shell spawn during ablation.

Pros:
- Avoids failing path entirely.

Cons:
- Changes behavior of OPTIONAL_ABLATION from pure direct codex shell path; comparability risk.

Risk:
- Low security risk, medium methodology risk.

Runtime/resource impact:
- Low.

## Would enabling OPTIONAL_ABLATION increase instability?
- If enabled via Option A: limited additional instability.
- If enabled via Option B (reduced sandbox): can increase operational/security instability.

## Would enabling materially increase runtime/resource use?
- Minimal increase for one Task 1 ablation run.
- Potential small increase if extra diagnostics/retries are added.

## Required configuration/workflow changes
Minimum required:
1. Validate Codex shell spawn in same environment with current sandbox mode.
2. Correct shell path/runtime mapping used by Codex exec on Windows.
3. Re-run ONLY OPTIONAL_ABLATION for Task 1 after validation, preserving logs.

## Exact file/location where restriction manifests
- Manifest location (runtime):
  - `runtime_exports/prereqs/runs/task01_explain_jwt/optional-ablation/trial1_20260525T165939Z/codex.log`
  - error lines from `codex_core::exec`.

- Invocation definition (benchmark script):
  - `prereqs/scripts/run_task.sh` optional-ablation block using `codex exec --full-auto`.

## Recommended next action
Execute a targeted, non-benchmark Codex spawn diagnostic in `prereqs/fixtures/task01_explain_jwt` and capture verbose Codex logs; then apply Option A first.
