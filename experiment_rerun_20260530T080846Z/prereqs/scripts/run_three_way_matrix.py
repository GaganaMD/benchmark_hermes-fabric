#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
import time
import signal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"
RUNS = ROOT / "runs_three_way"

TASK_VARIANTS = {
    "task01_explain_jwt": "fabric",
    "task02_signup_flow": "fabric",
    "task03_failing_test": "fabric",
    "task04_input_validation": "fabric",
    "task05_dry_run_flag": "fabric",
    "task06_signature_change": "fabric",
    "task07_print_to_logger": "fabric",
    "task08_config_migration": "fabric-improve",
    "task09_flaky_workers": "fabric-improve",
    "task10_fm_cli": "fabric-stitch",
}

VARIANTS = ["raw", "fabric-codex", "hermes-fabric-codex"]
TIMEOUT_SECONDS = int(os.environ.get("BENCH_RUN_TIMEOUT", "420"))


def run(cmd, cwd=None, input_text=None, timeout=TIMEOUT_SECONDS, env=None):
    started = time.monotonic()
    try:
        proc = subprocess.Popen(
            cmd,
            cwd=str(cwd) if cwd else None,
            stdin=subprocess.PIPE if input_text is not None else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
            start_new_session=True,
        )
        try:
            out, _ = proc.communicate(input_text, timeout=timeout)
            elapsed = time.monotonic() - started
            return proc.returncode, out, elapsed, False
        except subprocess.TimeoutExpired:
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                out, _ = proc.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                out, _ = proc.communicate()
            elapsed = time.monotonic() - started
            return 124, (out or "") + f"\nTIMEOUT after {timeout}s\n", elapsed, True
    except Exception as e:
        elapsed = time.monotonic() - started
        return 125, f"RUNNER EXCEPTION: {e}\n", elapsed, False


def reset_task(task):
    rc, out, _, _ = run(["bash", "scripts/reset.sh", task], cwd=ROOT, timeout=120)
    if rc != 0:
        raise RuntimeError(f"reset failed for {task}: {out}")


def fabric_pipeline(raw, task, env):
    mode = TASK_VARIANTS[task]
    pattern = ((FIXTURES / task / "pattern.txt").read_text().strip() if (FIXTURES / task / "pattern.txt").exists() else "")
    if mode == "fabric":
        cmd = ["fabric", "-p", pattern]
        rc, out, elapsed, timeout = run(cmd, input_text=raw, env=env, timeout=300)
        return rc, out, elapsed, timeout, f"fabric -p {pattern}"
    if mode == "fabric-improve":
        rc1, out1, e1, t1 = run(["fabric", "-p", "improve_prompt"], input_text=raw, env=env, timeout=300)
        if rc1 != 0:
            return rc1, out1, e1, t1, "fabric -p improve_prompt | fabric -p codex_brief"
        rc2, out2, e2, t2 = run(["fabric", "-p", "codex_brief"], input_text=out1, env=env, timeout=300)
        return rc2, out2, e1 + e2, (t1 or t2), "fabric -p improve_prompt | fabric -p codex_brief"
    if mode == "fabric-stitch":
        steps = ["create_prd", "improve_prompt", "codex_brief"]
        cur = raw
        total = 0.0
        any_timeout = False
        for step in steps:
            rc, cur, elapsed, timeout = run(["fabric", "-p", step], input_text=cur, env=env, timeout=300)
            total += elapsed
            any_timeout = any_timeout or timeout
            if rc != 0:
                return rc, cur, total, any_timeout, " | ".join(f"fabric -p {s}" for s in steps)
        return 0, cur, total, any_timeout, " | ".join(f"fabric -p {s}" for s in steps)
    raise ValueError(mode)


def run_pytest(task, outdir, env):
    fix = FIXTURES / task
    if not (fix / "tests").is_dir():
        return "na"
    rc, out, _, _ = run(["python", "-m", "pytest", "-x", "--tb=short"], cwd=fix, env=env, timeout=300)
    (outdir / "pytest.log").write_text(out)
    return str(rc)


def capture_diff(task, outdir):
    fix = FIXTURES / task
    rc, out, _, _ = run(["git", "diff", "--"], cwd=fix, timeout=120)
    (outdir / "changes.diff").write_text(out)
    rc, out, _, _ = run(["git", "status", "--short"], cwd=fix, timeout=120)
    (outdir / "git_status.txt").write_text(out)


def main():
    env = os.environ.copy()
    env["PATH"] = f"{Path.home() / '.local/bin'}:{ROOT / '.venv/bin'}:" + env.get("PATH", "")
    env["VIRTUAL_ENV"] = str(ROOT / ".venv")
    env["PYTHONUNBUFFERED"] = "1"
    RUNS.mkdir(exist_ok=True)
    summary = []

    for task in sorted(TASK_VARIANTS):
        raw = (FIXTURES / task / "prompt.txt").read_text().rstrip("\n")
        for variant in VARIANTS:
            # Resume support: skip variants with a completed run.json.
            existing = sorted((RUNS / task / variant).glob("*/run.json")) if (RUNS / task / variant).exists() else []
            if existing:
                print(f"skip {task} {variant}: existing {existing[-1].parent}", flush=True)
                continue
            print(f"=== {task} {variant} ===", flush=True)
            reset_task(task)
            ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
            outdir = RUNS / task / variant / ts
            outdir.mkdir(parents=True, exist_ok=True)
            (outdir / "raw_prompt.txt").write_text(raw)
            fabric_command = ""
            fabric_ms = None
            prompt_rc = 0
            prompt_timeout = False

            if variant == "raw":
                final_prompt = raw
                (outdir / "final_prompt.txt").write_text(final_prompt)
                start = time.monotonic()
                rc, log, agent_elapsed, agent_timeout = run(["codex", "--yolo", "exec", final_prompt], cwd=FIXTURES/task, env=env)
                total_elapsed = time.monotonic() - start
            else:
                total_start = time.monotonic()
                prompt_rc, final_prompt, fabric_elapsed, prompt_timeout, fabric_command = fabric_pipeline(raw, task, env)
                fabric_ms = int(fabric_elapsed * 1000)
                (outdir / "fabric_command.txt").write_text(fabric_command)
                (outdir / "final_prompt.txt").write_text(final_prompt)
                if prompt_rc != 0:
                    rc = prompt_rc
                    log = "FAILED during Fabric prompt generation.\n" + final_prompt
                    agent_elapsed = 0.0
                    agent_timeout = prompt_timeout
                elif variant == "fabric-codex":
                    rc, log, agent_elapsed, agent_timeout = run(["codex", "--yolo", "exec", final_prompt], cwd=FIXTURES/task, env=env)
                else:
                    hermes_prompt = (
                        "You are the Hermes orchestration layer for a coding-agent benchmark. "
                        "Use available file/terminal tools to complete the task in this repository. "
                        "Preserve the benchmark constraints from the prompt exactly. "
                        "When finished, summarize files changed and verification run.\n\n"
                        + final_prompt
                    )
                    (outdir / "hermes_prompt.txt").write_text(hermes_prompt)
                    rc, log, agent_elapsed, agent_timeout = run(["hermes", "--yolo", "chat", "-Q", "-q", hermes_prompt], cwd=FIXTURES/task, env=env)
                total_elapsed = time.monotonic() - total_start

            (outdir / "codex.log").write_text(log)
            capture_diff(task, outdir)
            tests_rc = run_pytest(task, outdir, env)
            meta = {
                "task_id": task,
                "variant": variant,
                "ts": ts,
                "total_ms": int(total_elapsed * 1000),
                "agent_ms": int(agent_elapsed * 1000),
                "fabric_ms": fabric_ms,
                "prompt_rc": prompt_rc,
                "exit_code": rc,
                "agent_timeout": bool(agent_timeout),
                "tests_exit_code": tests_rc,
                "fabric_command": fabric_command,
            }
            (outdir / "run.json").write_text(json.dumps(meta, indent=2))
            summary.append(meta)
            print(f"done {task} {variant}: rc={rc} tests={tests_rc} total={meta['total_ms']}ms", flush=True)

    (RUNS / "summary.json").write_text(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
