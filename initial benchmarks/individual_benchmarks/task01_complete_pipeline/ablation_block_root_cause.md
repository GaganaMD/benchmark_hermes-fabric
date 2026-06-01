# OPTIONAL_ABLATION block root cause (Task 1)

## Executive finding
The first hard failure in OPTIONAL_ABLATION was **inside Codex's Windows sandbox process launcher**, not in benchmark matrix policy code.

Primary error:
- `execution error: Io(Custom { kind: Other, error: "windows sandbox: spawn setup refresh" })`

Source evidence:
- `runtime_exports/prereqs/runs/task01_explain_jwt/optional-ablation/trial1_20260525T165939Z/codex.log`
  - line 23: `ERROR codex_core::exec: exec error: windows sandbox: spawn setup refresh`
  - line 26: `execution error: Io(Custom { kind: Other, error: "windows sandbox: spawn setup refresh" })`

## First failure point
In the OPTIONAL_ABLATION Codex run, the model's first tool actions attempted shell reads:
- `"C:\Program Files\7\pwsh.exe" -Command 'rg -n "jwt|access|refresh|validate|token" -S .'`
- `"C:\Program Files\7\pwsh.exe" -Command 'Get-Content -Path auth/jwt.py'`

Immediately after those calls, Codex emitted:
- `ERROR codex_core::exec: exec error: windows sandbox: spawn setup refresh`

This is the first observable failure in the ablation execution path.

## What specifically triggered the block
Trigger condition:
1. OPTIONAL_ABLATION launched Codex with `approval: never` and `sandbox: workspace-write`.
2. Codex tried to spawn a Windows shell command path (`C:\Program Files\7\pwsh.exe`) from within sandboxed execution.
3. Sandbox spawn refresh failed before command execution.

## Enforcing component
Enforced by:
- **Codex runtime sandbox subsystem** (`codex_core::exec`, `codex_core::tools::router`).

Not enforced by:
- `prereqs/scripts/run_task.sh` policy logic (script contains optional-ablation path and does not explicitly deny it).

## Classification
Best fit classification is mixed:
- sandbox based: YES
- runtime guardrail based: YES (sandbox spawn gate)
- path/tooling based: LIKELY (pwsh binary path used by Codex exec layer)
- configuration based: LIKELY CONTRIBUTOR (`approval: never`, sandbox mode)
- policy based (benchmark script hard-disable): NO evidence
- permission based (OS ACL): no direct evidence for this failure line
- missing dependency based: possible secondary contributor (if `pwsh.exe` path unavailable)
- session restriction based: no direct evidence

## Confidence
- High confidence on immediate blocker: `windows sandbox: spawn setup refresh`.
- Medium confidence on deeper cause (path/tooling vs sandbox bug) because stack trace is shallow in captured logs.

## Important correction
`benchmark_row.json` note says:
- `optional-ablation direct codex path was blocked by environment policy`

I found no direct log line proving a benchmark policy gate; the concrete logged blocker is Codex sandbox spawn failure.

## Recommended next action
Run a targeted diagnostic (no benchmark rerun) for Codex sandbox shell spawn in same fixture/workdir and capture full stderr with debug flags to disambiguate:
1) shell path resolution issue vs
2) sandbox launch defect vs
3) environment restrictions.
