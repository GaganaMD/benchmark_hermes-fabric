# X Thread Draft: Fabric Latency vs Prompt Transfer

## Short Thread

1/

I spent some time benchmarking Codex-only vs Fabric+Codex vs Hermes+Fabric+Codex across coding tasks and a long-form due diligence task.

The interesting result was not "Fabric does not work."

It was: a lot of the Fabric benefit seems to come from prompt structure that can be fed directly into Codex.

2/

The tradeoff showed up clearly in latency.

Across 10 coding benchmark tasks:

| Setup | Avg latency | Median latency | Notes |
|---|---:|---:|---|
| Codex only | 59.1s | 40.8s | Baseline direct prompt |
| Fabric + Codex | 94.6s | 69.7s | Structured prompt, extra orchestration |
| Hermes + Fabric + Codex | 80.9s | 66.1s | More structured recovery/verification |

Fabric+Codex was ~1.6x Codex-only on average for comparable rows.

3/

On the due diligence task, the pattern was similar.

Task: recursively inspect 582 files, expand/review 135 ZIP-contained files, extract content, map findings to sources, and produce a 21-slide sourced PPTX deck.

| Setup | Latency | Output |
|---|---:|---|
| Codex only | 10m 48s | 21-slide PPTX, sourced audit artifacts |
| Fabric + Codex | 14m 52s | Same deck target plus Fabric risk synthesis |
| Hermes + Fabric + Codex | 20m 34s | Same deck target plus stronger QA/verification reporting |

4/

The useful part of Fabric was not magic.

It was mostly:

- explicit role/task framing
- output schema
- constraints
- done-when checks
- risk/edge-case orientation
- verification reminders

Those are prompt features. They can be embedded directly into the Codex prompt.

5/

Example:

Instead of:

"make the workers more reliable"

Use:

"Improve worker reliability by adding bounded retries for BrokerError, exponential backoff, idempotency by task_id, injectable sleep for tests, and regression tests for retry success, retry exhaustion, and duplicate task execution. Run pytest -x and targeted tests."

That captures most of the Fabric-style value without a separate prompt transformation step.

6/

My current read:

Fabric is valuable as a prompt design library and thinking scaffold.

But if you already know the structure you want, routing through Fabric can add latency without adding much new information.

The better workflow may be:

1. Use Fabric patterns to discover good prompt shapes.
2. Distill those patterns into reusable direct prompts.
3. Feed those directly to Codex for lower latency.

7/

This matters because agent latency compounds.

Every orchestration layer adds:

- prompt construction time
- extra context
- more output tokens
- more chances for mismatch between the transformed prompt and the actual repo state

For tight coding loops, that overhead can dominate.

8/

What I would not conclude:

"Never use Fabric."

What I would conclude:

If the task is ambiguous, high-risk, or benefits from a known reasoning pattern, Fabric can help.

If the task is already well-scoped, a high-quality direct Codex prompt can often get comparable behavior faster.

9/

The benchmark result I care about:

Prompt quality transferred.

Once the Fabric pattern revealed what the model needed, the same ingredients could be expressed directly:

- goal
- constraints
- accepted files/scope
- verification commands
- failure modes
- final answer format

That is the durable artifact.

10/

The practical takeaway:

Treat Fabric less like a runtime dependency and more like a prompt compiler you can learn from.

Use it to find structure.
Then cache the structure in your own benchmark prompts.

That gives you most of the reliability gain while avoiding a meaningful chunk of orchestration latency.

Benchmark artifacts:
https://github.com/GaganaMD/benchmark_hermes-fabric/tree/main

## Single-Post Version

I benchmarked Codex-only vs Fabric+Codex vs Hermes+Fabric+Codex.

The main finding: Fabric helps mostly by adding prompt structure, but that structure can often be fed directly into Codex.

In 10 coding tasks:

- Codex only: 59.1s avg
- Fabric+Codex: 94.6s avg
- Hermes+Fabric+Codex: 80.9s avg

In a larger DD task:

- Codex only: 10m48s
- Fabric+Codex: 14m52s
- Hermes+Fabric+Codex: 20m34s

Fabric-style prompting improved task framing: constraints, output schema, done-when checks, and verification steps.

But once you know that structure, you can put it directly into the Codex prompt and avoid extra orchestration latency.

My takeaway: use Fabric to discover prompt patterns, then distill those patterns into direct prompts for faster repeated runs.

Artifacts:
https://github.com/GaganaMD/benchmark_hermes-fabric/tree/main

## Image/Card Copy

Title:
Prompt Structure Transfers. Latency Does Too.

Table:

| Benchmark | Codex | Fabric+Codex | Hermes+Fabric+Codex |
|---|---:|---:|---:|
| 10 coding tasks, avg | 59.1s | 94.6s | 80.9s |
| 10 coding tasks, median | 40.8s | 69.7s | 66.1s |
| Vlayx DD deck | 10m48s | 14m52s | 20m34s |

Caption:
Fabric-style structure helps: role, constraints, output schema, done-when checks, verification. But once learned, much of it can be encoded directly in the Codex prompt.

Takeaway:
Use Fabric to discover patterns. Cache those patterns as direct prompts when latency matters.

Repo:
https://github.com/GaganaMD/benchmark_hermes-fabric/tree/main

## Caveats

- These are local benchmark runs, not a universal model claim.
- Fabric can still be valuable for ambiguous tasks, prompt discovery, and structured reasoning.
- The strongest claim is about prompt transfer: the useful structure can often be reused directly.
- Latency includes end-to-end agent runtime, not only model inference.
- Repo/artifacts: https://github.com/GaganaMD/benchmark_hermes-fabric/tree/main
