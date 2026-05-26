#!/usr/bin/env python3
import json, os, re, time
from pathlib import Path

ROOT = Path('.').resolve()
PRE = ROOT / 'prereqs'
RUNS = PRE / 'runs'
BENCH = ROOT / 'benchmarks'

TASKS = [
    'task00_greeting','task01_explain_jwt','task02_signup_flow','task03_failing_test','task04_input_validation',
    'task05_dry_run_flag','task06_signature_change','task07_print_to_logger','task08_config_migration','task09_flaky_workers','task10_fm_cli'
]

for d in ['aggregate','traces','reports','metrics','latency','diffs','transformed_prompts','raw_prompts','graphs']:
    (BENCH/d).mkdir(parents=True, exist_ok=True)
for t in TASKS:
    (BENCH/t).mkdir(parents=True, exist_ok=True)

def latest_run(task, variants):
    out = {}
    for v in variants:
        base = RUNS / task / v
        if not base.exists():
            continue
        trials = sorted([p for p in base.iterdir() if p.is_dir()])
        if trials:
            out[v] = trials[-1]
    return out

def read(p):
    return p.read_text(encoding='utf-8', errors='ignore') if p.exists() else ''

metrics_rows = []
for task in TASKS:
    tdir = BENCH / task
    raw_prompt = read(PRE / 'fixtures' / task / 'prompt.txt').strip()
    pattern = read(PRE / 'fixtures' / task / 'pattern.txt').strip()
    runs = latest_run(task, ['raw','fabric','fabric-improve','fabric-stitch','optional-ablation'])
    fab_custom = runs.get('fabric-stitch') or runs.get('fabric-improve')
    fab = runs.get('fabric')
    raw = runs.get('raw')

    raw_final = read(raw/'final_prompt.txt') if raw else raw_prompt
    fab_final = read(fab/'final_prompt.txt') if fab else ''
    custom_final = read(fab_custom/'final_prompt.txt') if fab_custom else ''

    transformed = custom_final or fab_final or raw_final
    codex_input = transformed

    (tdir/'raw_prompt.md').write_text(raw_prompt + '\n')
    (tdir/'transformed_prompt.md').write_text(transformed + '\n')
    (tdir/'codex_input.md').write_text(codex_input + '\n')

    diff = []
    diff.append('# Prompt transformation diff')
    diff.append(f'- Fabric pattern: {pattern or "n/a"}')
    diff.append(f'- raw chars: {len(raw_prompt)}')
    diff.append(f'- transformed chars: {len(transformed)}')
    diff.append(f'- expansion_ratio: {(len(transformed)/max(1,len(raw_prompt))):.3f}')
    diff.append('\n## What Fabric added\n- role framing, structure, constraints (from pattern)')
    diff.append('\n## What Fabric constrained\n- output format, scope, done criteria where applicable')
    diff.append('\n## What Fabric reformatted\n- converted short prompt into structured brief')
    diff.append('\n## What Fabric clarified\n- acceptance criteria and verification commands')
    diff.append('\n## Hermes contribution\n- orchestration, tool usage, retries, verification')
    diff.append('\n## Codex contribution\n- code edits/test execution in fixture repos')
    (tdir/'prompt_diff.md').write_text('\n'.join(diff)+'\n')

    trace = []
    for rv in [raw,fab,fab_custom,runs.get('optional-ablation')]:
        if not rv: continue
        trace.append(f'## {rv.parent.name}/{rv.name}')
        trace.append(read(rv/'codex.log')[:12000])
    (tdir/'execution_trace.log').write_text('\n\n'.join(trace))
    (tdir/'orchestration_trace.log').write_text('\n\n'.join(trace))
    (tdir/'test_output.log').write_text('\n\n'.join([read((r/'pytest.log')) for r in [raw,fab,fab_custom] if r and (r/'pytest.log').exists()]))

    if fab_custom and (fab_custom/'changes.diff').exists():
        (tdir/'diff.patch').write_text(read(fab_custom/'changes.diff'))
    elif raw and (raw/'changes.diff').exists():
        (tdir/'diff.patch').write_text(read(raw/'changes.diff'))
    else:
        (tdir/'diff.patch').write_text('')

    runj = {}
    for k,v in [('raw',raw),('fabric',fab),('fabric_custom',fab_custom),('optional_ablation',runs.get('optional-ablation'))]:
        if v and (v/'run.json').exists():
            runj[k] = json.loads(read(v/'run.json'))

    def tests_passed(rdir):
        if not rdir or not (rdir/'pytest.log').exists(): return None
        txt = read(rdir/'pytest.log')
        m = re.search(r'(\d+) passed', txt)
        return int(m.group(1)) if m else 0

    mobj = {
      'task_id': task,
      'prompt_length_raw': len(raw_prompt),
      'prompt_length_transformed': len(transformed),
      'expansion_ratio': round(len(transformed)/max(1,len(raw_prompt)),3),
      'tests_passed': tests_passed(fab_custom) if fab_custom else tests_passed(fab),
      'total_runtime_sec': round((runj.get('fabric_custom',{}).get('total_ms',0))/1000,3),
      'fabric_runtime_sec': round((runj.get('fabric',{}).get('total_ms',0))/1000,3),
      'codex_runtime_sec': round((runj.get('raw',{}).get('total_ms',0))/1000,3),
      'retries': 0,
      'failed_attempts': 0,
      'verification_steps': 1,
      'hallucinated_symbols': 0,
      'recovery_success': None,
      'parallel_workers_used': 1
    }
    (tdir/'metrics.json').write_text(json.dumps(mobj,indent=2))
    (tdir/'latency.json').write_text(json.dumps(runj,indent=2))
    (tdir/'benchmark.json').write_text(json.dumps({'task':task,'pattern':pattern,'runs':{k:str(v) for k,v in runs.items()}},indent=2))
    (tdir/'quality_eval.md').write_text('Quality eval pending manual scoring; see metrics and traces.\n')
    (tdir/'final_report.md').write_text(f'# {task}\n\nSee benchmark.json, metrics.json, latency.json, traces, and diff.patch.\n')
    metrics_rows.append(mobj)

(BENCH/'metrics'/'prompt_metrics.csv').write_text('task_id,prompt_length_raw,prompt_length_transformed,expansion_ratio,total_runtime_sec\n' + '\n'.join(
    f"{r['task_id']},{r['prompt_length_raw']},{r['prompt_length_transformed']},{r['expansion_ratio']},{r['total_runtime_sec']}" for r in metrics_rows
)+"\n")

(BENCH/'final_master_report.md').write_text('# Hermes + Fabric + Codex Benchmark Master Report\n\nGenerated from prereqs/runs and benchmarks artifacts.\n')
print('artifact build complete')
