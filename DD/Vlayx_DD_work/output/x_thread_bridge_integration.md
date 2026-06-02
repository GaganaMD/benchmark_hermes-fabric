# X Thread Draft: Hermes + Fabric Bridge

## Positioning

This should probably come before the benchmark-results thread.

The bridge post answers:

> What did we actually build?

Then the benchmark thread answers:

> How did it behave across coding, reconciliation, and due diligence tasks?

The strongest framing is not "we glued two tools together." It is:

> I wanted Fabric's reusable reasoning patterns and Hermes' agentic synthesis/recovery without modifying either codebase, so I built a lightweight bridge around files, config, subprocesses, and logs.

## X Thread

1/

Before benchmarking Fabric, Hermes, and Codex together, I built a small bridge between Fabric and Hermes.

The goal was simple:

Use Fabric for structured chunk-level analysis.
Use Hermes for final synthesis and agentic follow-through.
Do it without modifying either project.

2/

The bridge is intentionally lightweight.

No vector DB.
No web service.
No framework-heavy orchestration layer.
No source changes in Fabric.
No source changes in Hermes.

Just Python, config, subprocesses, Markdown files, and logs.

Repo:
https://github.com/GaganaMD/benchmark_hermes-fabric/tree/main

3/

The pipeline looks like this:

```text
input document
  -> chunker.py
  -> Fabric patterns per chunk
  -> fabric_outputs/*.md
  -> combined_context.md
  -> Hermes prompt
  -> Hermes final synthesis
```

Fabric handles repeated local analysis.
Hermes handles the combined reasoning pass.

4/

Why a bridge instead of directly merging the tools?

Because the integration boundary matters.

Keeping the bridge separate means:

- Fabric can remain Fabric
- Hermes can remain Hermes
- commands are configurable
- logs are reproducible
- intermediate artifacts are inspectable
- failures are easier to debug

5/

The important files:

```text
bridge/run_pipeline.py
bridge/chunker.py
bridge/fabric_runner.py
bridge/hermes_runner.py
bridge/config.yaml
bridge/out/
```

The output directory becomes the audit trail:

```text
fabric_outputs/
combined_context.md
hermes_prompt.txt
hermes_final_output.md
logs/
```

6/

This design makes the integration auditable.

You can inspect:

- what each Fabric pattern produced
- how chunk outputs were combined
- the exact prompt sent to Hermes
- the final Hermes output
- execution logs

That matters when the task is bigger than a single prompt.

7/

The first intuition:

Fabric is good at applying named reasoning patterns repeatedly.

Hermes is better suited for higher-level synthesis, recovery behavior, and agentic workflow control.

The bridge lets them play different roles instead of forcing one tool to do everything.

8/

Where this becomes useful:

- long documents
- due diligence corpora
- reconciliation workflows
- research notes
- multi-file analysis
- tasks where you need a traceable path from raw input to final output

The intermediate files are not clutter. They are evidence.

9/

This also changed how I think about benchmarking agents.

For tiny coding tasks, orchestration overhead is very visible.

For messy workflows, the question changes:

Did the system preserve context?
Did it produce artifacts?
Can I inspect intermediate reasoning?
Can it recover and verify?

10/

That is why the later benchmarks covered three layers:

1. small coding tasks
2. invoice reconciliation
3. full due diligence deck generation

The bridge made it possible to test not just final answers, but workflow behavior.

11/

My takeaway from building the bridge:

Agent integrations should start boring.

Files.
Config.
Logs.
Subprocesses.
Clear boundaries.

Once the workflow proves useful, then you can decide whether deeper integration is worth it.

12/

The bridge is not the final product.

It is the simplest useful integration surface:

- chunk input
- apply Fabric patterns
- aggregate context
- send to Hermes
- save every intermediate artifact

That was enough to run meaningful benchmarks.

## Short Version

Before running the benchmarks, I built a lightweight bridge between Fabric and Hermes.

The idea:

- Fabric does chunk-level pattern analysis.
- Hermes does final synthesis/recovery.
- A Python bridge coordinates the flow without modifying either project.

Pipeline:

```text
input -> chunks -> Fabric patterns -> combined_context.md -> Hermes -> final output
```

The bridge writes every intermediate artifact, including Fabric outputs, combined context, Hermes prompt, final output, and logs.

This made the later benchmarks more useful because I could inspect not just the final answer, but the workflow path.

Repo:
https://github.com/GaganaMD/benchmark_hermes-fabric/tree/main

## Image/Card Copy

Title:
Building a Fabric -> Hermes Bridge

Flow:

```text
Input
  -> Chunker
  -> Fabric patterns
  -> Combined context
  -> Hermes synthesis
  -> Final artifact
```

Design constraints:

- no Fabric source changes
- no Hermes source changes
- config-first commands
- file-based audit trail
- reproducible logs

Repo:
https://github.com/GaganaMD/benchmark_hermes-fabric/tree/main

## Suggested Posting Order

1. Bridge/integration thread: explains the system.
2. Three-layer benchmark thread: explains how the system behaved.
3. Fabric latency/prompt-transfer thread: narrower technical conclusion.

## Caveats

- This bridge is intentionally minimal, not a full orchestration platform.
- It uses subprocess and file boundaries, which are slower than internal APIs but easier to inspect.
- The goal was benchmarkability and auditability, not maximum throughput.
