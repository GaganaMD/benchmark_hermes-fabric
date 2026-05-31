#!/usr/bin/env python3
"""Three-way coding-agent benchmark runner using prereqs 2 fixtures as source of truth."""
import json
import os
import re
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"
RUNS = ROOT / "runs_three_way_prereqs2"
TIMEOUT_SECONDS = int(os.environ.get("BENCH_RUN_TIMEOUT", "900"))
FABRIC_TIMEOUT_SECONDS = int(os.environ.get("BENCH_FABRIC_TIMEOUT", "420"))
VERIFY_TIMEOUT_SECONDS = int(os.environ.get("BENCH_VERIFY_TIMEOUT", "300"))

TASKS = [
    ("T1", "task01_explain_jwt", "fabric"),
    ("T2", "task02_signup_flow", "fabric"),
    ("T3", "task03_failing_test", "fabric"),
    ("T4", "task04_input_validation", "fabric"),
    ("T5", "task05_dry_run_flag", "fabric"),
    ("T6", "task06_signature_change", "fabric"),
    ("T7", "task07_print_to_logger", "fabric"),
    ("T8", "task08_config_migration", "fabric-improve"),
    ("T9", "task09_flaky_workers", "fabric-improve"),
    ("T10", "task10_fm_cli", "fabric-stitch"),
]
VARIANTS = ["raw", "fabric-codex", "hermes-fabric-codex"]


def run(cmd, cwd=None, input_text=None, timeout=TIMEOUT_SECONDS, env=None):
    started = time.monotonic()
    try:
        # Use a real temp file for child stdout instead of a PIPE. Some Codex
        # subprocess trees can leave inherited pipe FDs open after the wrapper is
        # killed, which makes communicate() hang while collecting output.
        with tempfile.TemporaryFile(mode="w+", encoding="utf-8", errors="replace") as stdout_file:
            proc = subprocess.Popen(
                cmd,
                cwd=str(cwd) if cwd else None,
                stdin=subprocess.PIPE if input_text is not None else None,
                stdout=stdout_file,
                stderr=subprocess.STDOUT,
                text=True,
                env=env,
                start_new_session=True,
            )
            try:
                proc.communicate(input_text, timeout=timeout)
                stdout_file.seek(0)
                return proc.returncode, stdout_file.read() or "", time.monotonic() - started, False
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    proc.wait(timeout=10)
                stdout_file.seek(0)
                out = stdout_file.read() or ""
                return 124, out + f"\nTIMEOUT after {timeout}s\n", time.monotonic() - started, True
    except Exception as e:
        return 125, f"RUNNER EXCEPTION: {type(e).__name__}: {e}\n", time.monotonic() - started, False


def reset_task(task_slug):
    rc, out, _, _ = run(["bash", "scripts/reset.sh", task_slug], cwd=ROOT, timeout=120)
    if rc != 0:
        raise RuntimeError(f"reset failed for {task_slug}: {out}")


def build_fabric_input(raw, task_slug, pattern):
    """Build the text sent to Fabric from prereqs 2 task files.

    For explain_code patterns, Fabric needs actual code on stdin or it returns a
    generic explanation. For codex_brief-style coding tasks, prereqs 2 ships a
    task-specific brief.md; use it as the task-specific prompt material instead
    of the raw one-liner so the Fabric output is repo/task-specific.
    """
    fix = FIXTURES / task_slug
    brief = (fix / "brief.md").read_text().rstrip("\n") if (fix / "brief.md").exists() else raw
    if pattern == "explain_code":
        parts = ["RAW PROMPT:\n" + raw, "TASK BRIEF:\n" + brief]
        # Include small source files relevant to read-only explanation tasks.
        for rel in ["auth/jwt.py", "api/handlers.py", "services/user.py", "db/repo.py"]:
            p = fix / rel
            if p.exists():
                parts.append(f"--- {rel} ---\n" + p.read_text())
        return "\n\n".join(parts)
    if pattern == "codex_brief":
        return brief
    return raw + "\n\nTASK BRIEF:\n" + brief


def fabric_pipeline(raw, task_slug, mode, env):
    pattern = ""
    pattern_path = FIXTURES / task_slug / "pattern.txt"
    if pattern_path.exists():
        pattern = pattern_path.read_text().strip()
    fabric_input = build_fabric_input(raw, task_slug, pattern)
    if mode == "fabric":
        rc, out, elapsed, timeout = run(["fabric", "-p", pattern], input_text=fabric_input, env=env, timeout=FABRIC_TIMEOUT_SECONDS)
        return rc, out, elapsed, timeout, f"fabric -p {pattern}"
    if mode == "fabric-improve":
        rc1, out1, e1, t1 = run(["fabric", "-p", "improve_prompt"], input_text=fabric_input, env=env, timeout=FABRIC_TIMEOUT_SECONDS)
        if rc1 != 0:
            return rc1, out1, e1, t1, "fabric -p improve_prompt | fabric -p codex_brief"
        rc2, out2, e2, t2 = run(["fabric", "-p", "codex_brief"], input_text=out1, env=env, timeout=FABRIC_TIMEOUT_SECONDS)
        return rc2, out2, e1 + e2, (t1 or t2), "fabric -p improve_prompt | fabric -p codex_brief"
    if mode == "fabric-stitch":
        steps = ["create_prd", "improve_prompt", "codex_brief"]
        cur = fabric_input
        total = 0.0
        any_timeout = False
        for step in steps:
            rc, cur, elapsed, timeout = run(["fabric", "-p", step], input_text=cur, env=env, timeout=FABRIC_TIMEOUT_SECONDS)
            total += elapsed
            any_timeout = any_timeout or timeout
            if rc != 0:
                return rc, cur, total, any_timeout, " | ".join(f"fabric -p {s}" for s in steps)
        return 0, cur, total, any_timeout, " | ".join(f"fabric -p {s}" for s in steps)
    raise ValueError(mode)


def write_cmd_log(outdir, name, command, rc, out, elapsed, timeout=False):
    payload = {
        "name": name,
        "command": command,
        "exit_code": rc,
        "elapsed_ms": int(elapsed * 1000),
        "timeout": bool(timeout),
        "output": out,
    }
    (outdir / f"verify_{name}.json").write_text(json.dumps(payload, indent=2))
    return payload


def command_available(cmd, env):
    rc, out, _, _ = run(["bash", "-lc", f"command -v {cmd}"], env=env, timeout=20)
    return rc == 0, out.strip()


def py_scan_decode_packet(cwd, outdir, env):
    script = r'''
from pathlib import Path
for p in sorted(Path('src').rglob('*.py')):
    for i, line in enumerate(p.read_text().splitlines(), 1):
        if 'decode_packet(' in line:
            print(f"{p}:{i}:{line}")
'''
    return run(["python3", "-c", script], cwd=cwd, env=env, timeout=60)


def py_scan_print(cwd, outdir, env):
    script = r'''
import ast
from pathlib import Path
for p in sorted(Path('src').rglob('*.py')):
    try:
        tree = ast.parse(p.read_text())
    except SyntaxError as e:
        print(f"{p}:{e.lineno}:SYNTAX_ERROR:{e.msg}")
        continue
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'print':
            print(f"{p}:{node.lineno}:print(...)")
'''
    return run(["python3", "-c", script], cwd=cwd, env=env, timeout=60)


def verify_t5_dry_run(cwd, outdir, env):
    script = r'''
import subprocess, sys
from pathlib import Path
attempts = [
    [sys.executable, '-m', 'src.cli', '--dry-run', 'write', 'dryrun_probe.txt', '--content', 'probe'],
    [sys.executable, '-m', 'src.cli', 'write', '--dry-run', 'dryrun_probe.txt', '--content', 'probe'],
]
for cmd in attempts:
    p = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print('$ ' + ' '.join(cmd))
    print('rc=', p.returncode)
    print(p.stdout)
    if p.returncode == 0:
        exists = Path('dryrun_probe.txt').exists()
        print('dryrun_probe_exists=', exists)
        if exists:
            Path('dryrun_probe.txt').unlink()
            raise SystemExit(1)
        raise SystemExit(0)
print('No dry-run invocation form succeeded')
raise SystemExit(1)
'''
    return run(["python3", "-c", script], cwd=cwd, env=env, timeout=60)


def verify_t8_behavior(cwd, outdir, env):
    script = r'''
import importlib, inspect, tempfile, warnings, sys
from pathlib import Path
sys.path.insert(0, str(Path('.').resolve()))
import src.config as c
print('python', sys.version.split()[0])
print('tomllib_available', importlib.util.find_spec('tomllib') is not None)
print('src.config symbols', [name for name in dir(c) if not name.startswith('_')])
# Prefer load_config if present; otherwise report inability to dynamically verify.
fn = getattr(c, 'load_config', None)
print('load_config_present', callable(fn))
if not callable(fn):
    raise SystemExit(1)
with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    (root/'config.ini').write_text('[app]\nname=ini-app\nworkers=2\n')
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter('always')
        try:
            ini_val = fn(root/'config.ini')
        except TypeError:
            ini_val = fn(str(root/'config.ini'))
        print('ini_load_ok', bool(ini_val), 'warnings', [(w.category.__name__, str(w.message)) for w in rec])
    (root/'config.toml').write_text('[app]\nname="toml-app"\nworkers=3\n')
    try:
        toml_val = fn(root/'config.toml')
    except TypeError:
        toml_val = fn(str(root/'config.toml'))
    print('toml_load_ok', bool(toml_val), toml_val)
'''
    return run(["python3", "-c", script], cwd=cwd, env=env, timeout=60)


def verify_t10_cli(cwd, outdir, env):
    script = r'''
from pathlib import Path
import re
root = Path('tools/fm')
print('tools/fm exists', root.exists())
for rel in ['__init__.py', 'cli.py']:
    print(rel, (root/rel).exists())
text = ''
for p in root.rglob('*.py'):
    text += '\n# FILE ' + str(p) + '\n' + p.read_text()
for cmd in ['list', 'move', 'tag', 'search-by-tag']:
    print('command_marker', cmd, cmd in text or cmd.replace('-', '_') in text)
print('sqlite_marker', 'sqlite3' in text or '.sqlite' in text or '.db' in text)
print('colocated_marker', 'managed root' in text.lower() or 'root' in text.lower())
'''
    return run(["python3", "-c", script], cwd=cwd, env=env, timeout=60)


def run_verifications(task_id, task_slug, outdir, env):
    cwd = FIXTURES / task_slug
    results = []
    def add(name, cmd, timeout=VERIFY_TIMEOUT_SECONDS):
        rc, out, elapsed, to = run(cmd, cwd=cwd, env=env, timeout=timeout)
        results.append(write_cmd_log(outdir, name, cmd, rc, out, elapsed, to))
        return rc
    def add_shell(name, shell_cmd, timeout=VERIFY_TIMEOUT_SECONDS):
        return add(name, ["bash", "-lc", shell_cmd], timeout)

    if task_id in {"T1", "T2"}:
        add("git_diff_readonly", ["git", "diff", "--"])
        add("git_status_readonly", ["git", "status", "--short"])
    elif task_id == "T3":
        add("pytest_target", ["python3", "-m", "pytest", "tests/test_parser.py::test_handles_empty", "-q"])
        add("git_diff_tests", ["git", "diff", "--", "tests/"])
    elif task_id == "T4":
        add("pytest_parser", ["python3", "-m", "pytest", "tests/test_parser.py", "-q"])
    elif task_id == "T5":
        add("pytest_cli", ["python3", "-m", "pytest", "tests/test_cli.py", "-q"])
        rc, out, elapsed, to = verify_t5_dry_run(cwd, outdir, env)
        results.append(write_cmd_log(outdir, "dry_run_no_write", ["python3", "<dry-run probe>"], rc, out, elapsed, to))
    elif task_id == "T6":
        rg_ok, rg_path = command_available("rg", env)
        if rg_ok:
            add("scan_decode_packet", ["rg", "-n", "decode_packet(", "src/"])
        else:
            rc, out, elapsed, to = py_scan_decode_packet(cwd, outdir, env)
            out = "rg unavailable; used Python fallback.\n" + out
            results.append(write_cmd_log(outdir, "scan_decode_packet", ["python3", "<fallback scan decode_packet>"], rc, out, elapsed, to))
        add("pytest_proto", ["python3", "-m", "pytest", "tests/test_proto.py", "-q"])
        add("git_diff_test_proto", ["git", "diff", "--", "tests/test_proto.py"])
    elif task_id == "T7":
        rg_ok, rg_path = command_available("rg", env)
        if rg_ok:
            add("scan_print_src", ["rg", "-n", "print(", "src/"])
        else:
            rc, out, elapsed, to = py_scan_print(cwd, outdir, env)
            out = "rg unavailable; used Python AST fallback.\n" + out
            results.append(write_cmd_log(outdir, "scan_print_src", ["python3", "<fallback AST scan print calls>"], rc, out, elapsed, to))
        add("pytest_all", ["python3", "-m", "pytest", "-q"])
        add("git_diff_scripts", ["git", "diff", "--", "scripts/"])
    elif task_id == "T8":
        add("pytest_config", ["python3", "-m", "pytest", "tests/test_config.py", "-q"])
        add("pytest_all", ["python3", "-m", "pytest", "-q"])
        rc, out, elapsed, to = verify_t8_behavior(cwd, outdir, env)
        results.append(write_cmd_log(outdir, "config_behavior", ["python3", "<toml/ini behavior probe>"], rc, out, elapsed, to))
    elif task_id == "T9":
        add("pytest_workers", ["python3", "-m", "pytest", "tests/test_workers.py", "-q"])
        soak_candidates = [p for p in cwd.rglob("*soak*") if p.is_file()]
        if soak_candidates:
            p = soak_candidates[0]
            add("soak_script", ["bash", "-lc", f"chmod +x {p.relative_to(cwd)!s}; {p.relative_to(cwd)!s}"], timeout=600)
        else:
            (outdir / "soak_script.txt").write_text("No soak script found in task folder.\n")
    elif task_id == "T10":
        add("pytest_all", ["python3", "-m", "pytest", "-q"])
        rc, out, elapsed, to = verify_t10_cli(cwd, outdir, env)
        results.append(write_cmd_log(outdir, "fm_cli_shape", ["python3", "<tools/fm shape probe>"], rc, out, elapsed, to))
    (outdir / "verification_summary.json").write_text(json.dumps(results, indent=2))
    return results


def capture_diff(task_slug, outdir):
    cwd = FIXTURES / task_slug
    rc, out, _, _ = run(["git", "diff", "--"], cwd=cwd, timeout=120)
    (outdir / "changes.diff").write_text(out)
    rc, out, _, _ = run(["git", "status", "--short"], cwd=cwd, timeout=120)
    (outdir / "git_status.txt").write_text(out)


def is_completed_run(path):
    try:
        meta = json.loads(path.read_text())
    except Exception:
        return False
    # Treat transient prompt-generation/network failures and timeouts as
    # incomplete so resume can produce a comparable run without deleting the
    # failed artifact.
    if meta.get("prompt_rc", 0) != 0 or meta.get("prompt_timeout") or meta.get("agent_timeout"):
        return False
    for v in meta.get("verification", []) or []:
        if "No module named pytest" in (v.get("output") or ""):
            return False
    return True


def main():
    env = os.environ.copy()
    env["PATH"] = f"{ROOT / '.venv/bin'}:{Path.home() / '.local/bin'}:{env.get('PATH','')}"
    env["VIRTUAL_ENV"] = str(ROOT / ".venv")
    env["PYTHONUNBUFFERED"] = "1"
    RUNS.mkdir(exist_ok=True)
    summary = []

    # Tool inventory
    tools = {}
    for tool in ["codex", "fabric", "hermes", "rg", "python3"]:
        ok, path = command_available(tool, env)
        tools[tool] = {"available": ok, "path": path}
    (RUNS / "tool_inventory.json").write_text(json.dumps(tools, indent=2))

    for task_id, task_slug, mode in TASKS:
        raw = (FIXTURES / task_slug / "prompt.txt").read_text().rstrip("\n")
        for variant in VARIANTS:
            existing = sorted((RUNS / task_slug / variant).glob("*/run.json")) if (RUNS / task_slug / variant).exists() else []
            completed = [p for p in existing if is_completed_run(p)]
            if completed:
                print(f"skip {task_slug} {variant}: existing {completed[-1].parent}", flush=True)
                continue
            print(f"=== {task_slug} {variant} ===", flush=True)
            reset_task(task_slug)
            ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
            outdir = RUNS / task_slug / variant / ts
            outdir.mkdir(parents=True, exist_ok=True)
            (outdir / "raw_prompt.txt").write_text(raw)
            fabric_command = ""
            fabric_ms = None
            prompt_rc = 0
            prompt_timeout = False
            agent_timeout = False
            agent_elapsed = 0.0
            final_prompt = ""
            start_total = time.monotonic()

            if variant == "raw":
                final_prompt = raw
                (outdir / "final_prompt.txt").write_text(final_prompt)
                rc, log, agent_elapsed, agent_timeout = run(["codex", "--yolo", "exec", final_prompt], cwd=FIXTURES/task_slug, env=env)
            else:
                # Generate Fabric once per task when possible. The Hermes+Fabric
                # variant should receive the exact same Fabric-enhanced prompt as
                # Fabric+Codex, not a second non-deterministic Fabric sample.
                reused_fabric = False
                if variant == "hermes-fabric-codex":
                    prior = sorted((RUNS / task_slug / "fabric-codex").glob("*/final_prompt.txt")) if (RUNS / task_slug / "fabric-codex").exists() else []
                    prior_meta = sorted((RUNS / task_slug / "fabric-codex").glob("*/run.json")) if (RUNS / task_slug / "fabric-codex").exists() else []
                    completed_meta = [p for p in prior_meta if is_completed_run(p)]
                    if prior and completed_meta:
                        meta_dir = completed_meta[-1].parent
                        prompt_file = meta_dir / "final_prompt.txt"
                        final_prompt = prompt_file.read_text()
                        fabric_command_path = meta_dir / "fabric_command.txt"
                        fabric_command = fabric_command_path.read_text() if fabric_command_path.exists() else "reused from fabric-codex"
                        fabric_ms = 0
                        prompt_rc = 0
                        prompt_timeout = False
                        reused_fabric = True
                if not reused_fabric:
                    prompt_rc, final_prompt, fabric_elapsed, prompt_timeout, fabric_command = fabric_pipeline(raw, task_slug, mode, env)
                    fabric_ms = int(fabric_elapsed * 1000)
                (outdir / "fabric_command.txt").write_text(fabric_command)
                (outdir / "final_prompt.txt").write_text(final_prompt)
                if prompt_rc != 0:
                    rc = prompt_rc
                    log = "FAILED during Fabric prompt generation.\n" + final_prompt
                    agent_timeout = prompt_timeout
                elif variant == "fabric-codex":
                    codex_prompt = (
                        "You are Codex running inside this repository. The text below is the exact Fabric-enhanced prompt/context. "
                        "Do not treat any statement like 'I cannot edit/run commands' as applying to you; you can inspect files, edit files, and run verification in this repo. "
                        "Complete the underlying task and report verification.\n\n"
                        + final_prompt
                    )
                    (outdir / "codex_input_prompt.txt").write_text(codex_prompt)
                    rc, log, agent_elapsed, agent_timeout = run(["codex", "--yolo", "exec", codex_prompt], cwd=FIXTURES/task_slug, env=env)
                else:
                    hermes_prompt = (
                        "You are the Hermes orchestration layer for a coding-agent benchmark. "
                        "Use available file and terminal tools to complete the task in this repository. "
                        "Preserve benchmark constraints exactly. Inspect the repository before editing. "
                        "Run the task-specific verification commands before finalizing. "
                        "When finished, summarize files changed, verification run, and any recovery behavior.\n\n"
                        + final_prompt
                    )
                    (outdir / "hermes_prompt.txt").write_text(hermes_prompt)
                    rc, log, agent_elapsed, agent_timeout = run(["hermes", "--yolo", "chat", "-Q", "-q", hermes_prompt], cwd=FIXTURES/task_slug, env=env)
            total_elapsed = time.monotonic() - start_total
            (outdir / "codex.log").write_text(log)
            capture_diff(task_slug, outdir)
            verification = run_verifications(task_id, task_slug, outdir, env)
            meta = {
                "task": task_id,
                "task_id": task_slug,
                "variant": variant,
                "ts": ts,
                "total_ms": int(total_elapsed * 1000),
                "agent_ms": int(agent_elapsed * 1000),
                "fabric_ms": fabric_ms,
                "prompt_rc": prompt_rc,
                "exit_code": rc,
                "agent_timeout": bool(agent_timeout),
                "prompt_timeout": bool(prompt_timeout),
                "fabric_command": fabric_command,
                "verification": verification,
            }
            (outdir / "run.json").write_text(json.dumps(meta, indent=2))
            summary.append(meta)
            vnote = ",".join(f"{v['name']}={v['exit_code']}" for v in verification)
            print(f"done {task_slug} {variant}: rc={rc} verify=[{vnote}] total={meta['total_ms']}ms", flush=True)
    (RUNS / "summary.json").write_text(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
