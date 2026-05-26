# OPTIONAL_ABLATION policy analysis

## Question
Was OPTIONAL_ABLATION blocked by policy, environment, permission, sandbox, config, tooling path, runtime guardrail, dependency, or session restriction?

## Evidence reviewed
- `runtime_exports/prereqs/runs/task01_explain_jwt/optional-ablation/trial1_20260525T165939Z/codex.log`
- `prereqs/scripts/run_task.sh`
- `benchmarks/logs/matrix*.log`
- `bridge/out/logs/{pipeline.log,hermes_runner.log,fabric_runner.log}`
- `benchmarks/logs/{hermes_runner.log,fabric_runner.log,pipeline.log}` (where present)
- `benchmark_row.json` note text

## Findings by category
1) policy based
- Evidence: none for a hard policy-deny event.
- `run_task.sh` includes OPTIONAL_ABLATION execution code; no explicit deny branch.
- Conclusion: **Not proven as policy-based blocker**.

2) environment based
- Evidence: codex running on Windows host with sandbox mode; shell spawn fails.
- Conclusion: **Contributing factor likely**.

3) permission based
- No direct ACL/permission-denied message tied to OPTIONAL_ABLATION failure.
- Conclusion: **Not primary per available logs**.

4) sandbox based
- Direct evidence: `windows sandbox: spawn setup refresh`.
- Conclusion: **Primary**.

5) configuration based
- Direct context evidence: `approval: never`, `sandbox: workspace-write` in codex session header.
- Conclusion: **Likely contributor**.

6) path/tooling based
- Codex attempts `C:\Program Files\7\pwsh.exe` command path.
- If path invalid/unavailable in sandbox context, spawn setup may fail.
- Conclusion: **Likely contributor (needs targeted validation)**.

7) runtime guardrail based
- Sandbox exec layer blocks tool execution before command runs.
- Conclusion: **Primary (operationally equivalent to runtime guardrail)**.

8) missing dependency based
- Not directly evidenced for this failure string; possible but unproven.

9) session restriction based
- No explicit session policy restriction in logs.

## Most defensible root-cause statement
OPTIONAL_ABLATION failed because Codex's sandboxed exec subsystem could not initialize process spawn (`windows sandbox: spawn setup refresh`) when trying to run shell-based file inspection commands. This is a sandbox/runtime execution failure, with probable configuration/path coupling.

## Gap
No deeper stack trace in captured artifacts to distinguish:
- sandbox engine defect
- shell binary path resolution failure
- sandbox compatibility issue on this Windows setup

## Recommended next action
Perform a minimal one-command Codex sandbox spawn diagnostic in the same fixture/workdir (no benchmark run), capturing full debug logs to isolate whether the root is shell path resolution or sandbox engine init.
