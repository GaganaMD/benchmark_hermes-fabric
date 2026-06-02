# X Thread Draft: Three Benchmark Layers

## Positioning

This thread is stronger than only talking about Fabric latency because it shows a more complete benchmark arc:

1. Small coding tasks: controlled, fast, easy to verify.
2. Reconciliation task: spreadsheet/accounting reasoning with concrete line-item outputs.
3. Due diligence task: messy corpus traversal, extraction, synthesis, and artifact generation.

The main thesis:

> Agent benchmarks should not stop at toy coding tasks. The real question is how orchestration behaves as task ambiguity, data volume, and verification burden increase.

## X Thread

1/

I ran three layers of agent benchmarks:

1. small coding tasks
2. invoice reconciliation
3. full due diligence report generation

The pattern was useful: orchestration helps most when the task needs structure, verification, and recovery. But it also adds latency.

2/

Layer 1: coding tasks.

These were small repo tasks: explain code, fix tests, add validation, migrate config, build a small CLI, etc.

The comparison was:

| Setup | Avg latency | Median latency |
|---|---:|---:|
| Codex only | 59.1s | 40.8s |
| Fabric + Codex | 94.6s | 69.7s |
| Hermes + Fabric + Codex | 80.9s | 66.1s |

3/

On small coding tasks, direct Codex was usually fastest.

Fabric-style prompts improved structure:

- role framing
- output format
- constraints
- done-when checks
- verification reminders

But once those patterns were known, a direct prompt could often capture the same benefits with less orchestration overhead.

4/

Layer 2: reconciliation.

Task: reconcile Tally bills against Blinkit bills.

The output had to identify:

- matched invoices
- amount mismatches
- invoice number mismatches
- Tally-only invoices
- Blinkit-only / TDS reversal rows

This is closer to real finance work than a code toy problem.

5/

Reconciliation result:

| Finding | Count |
|---|---:|
| Matched with rounding tolerance | 26 |
| Amount mismatches | 3 |
| Probable invoice-number mismatch | 1 |
| Blinkit-only TDS reversal rows | 15 |
| Tally-only invoices | 28 |

The biggest unresolved bucket was 28 Tally-only invoices totaling INR 11,25,014.

6/

Reconciliation latency:

| Setup | Latency |
|---|---:|
| Codex only | 78s |
| Fabric + Codex | 83s |
| Hermes + Fabric + Codex | 270s |

This was interesting: Fabric added only modest latency here, but Hermes+Fabric+Codex spent much longer producing the more complete final report and supporting artifacts.

7/

Layer 3: due diligence.

Task: produce a complete DD report as a PowerPoint deck by recursively investigating a full target folder tree.

The corpus:

- 582 tree files
- 135 ZIP-contained files
- 717 total manifest items
- 0 extraction errors
- final 21-slide sourced deck

8/

DD latency:

| Setup | Latency | Output |
|---|---:|---|
| Codex only | 10m48s | 21-slide sourced deck |
| Fabric + Codex | 14m52s | deck + risk synthesis |
| Hermes + Fabric + Codex | 20m34s | deck + stronger QA/verification |

The Hermes+Fabric+Codex run was slower, but it also reported stricter QA: source resolution, placeholder checks, footer readability, manifest status, and deck hash.

9/

The DD task exposed the real distinction.

In small coding tasks, latency is very visible because the work is small.

In DD, the overhead starts to look more acceptable because the output needs:

- recursive inventory
- extraction coverage
- source mapping
- risk synthesis
- artifact generation
- verification

10/

My current take:

Fabric is not mainly valuable as a magical answer generator.

It is valuable as a structure generator.

Hermes-style orchestration is not mainly valuable for speed.

It is valuable for recovery, verification discipline, and making the final output auditable.

11/

So the right comparison is not just:

"Which stack is fastest?"

It is:

"At what task complexity does orchestration overhead become worth it?"

For small coding tasks, direct Codex with a strong prompt often wins.

For messy business workflows, the verification layer starts to matter.

12/

The benchmark pattern:

| Task layer | Best use of orchestration |
|---|---|
| Small coding tasks | Learn prompt structure, then use direct prompts |
| Reconciliation | Use structured matching criteria and output artifacts |
| Due diligence | Use orchestration for auditability, coverage, and QA |

13/

The practical workflow I would use now:

1. Start with direct Codex for scoped coding tasks.
2. Use Fabric patterns when prompt structure is unclear.
3. Use Hermes/Fabric-style orchestration when the task needs coverage guarantees, recovery, or audit trails.
4. Cache good prompt structures so repeated runs do not pay the same latency tax.

14/

The meta-takeaway:

Benchmarks should include tasks where the answer is not just "write code."

They should test:

- source grounding
- artifact generation
- multi-file/corpus traversal
- verification
- recovery behavior
- clarity of final reporting

That is where agent systems start to separate.

15/

The surprising lesson:

Prompt structure transfers across layers.

The same ingredients helped in coding, reconciliation, and DD:

- explicit goal
- strict scope
- output schema
- done-when checks
- source/verification requirements
- artifact expectations

The more complex the workflow, the more valuable those constraints become.

16/

I put the benchmark artifacts here:

https://github.com/GaganaMD/benchmark_hermes-fabric/tree/main

The repo includes the benchmark tables, reconciliation outputs, DD decks/PDFs, and supporting artifacts.

## Short Version

I ran three layers of agent benchmarks:

1. small coding tasks
2. invoice reconciliation
3. full due diligence report generation

The pattern:

- Direct Codex is fastest for small scoped coding tasks.
- Fabric helps by turning vague requests into structured prompts.
- Hermes/Fabric-style orchestration becomes more valuable when the task needs auditability, recovery, and verification.

Numbers:

| Layer | Codex | Fabric+Codex | Hermes+Fabric+Codex |
|---|---:|---:|---:|
| Coding tasks, avg | 59.1s | 94.6s | 80.9s |
| Reconciliation | 78s | 83s | 270s |
| Due diligence | 10m48s | 14m52s | 20m34s |

The key lesson: orchestration adds latency, but the value depends on task complexity.

For small tasks, use direct prompts. For messy corpus/business workflows, the verification layer can be worth the cost.

Artifacts:
https://github.com/GaganaMD/benchmark_hermes-fabric/tree/main

## Image/Card Copy

Title:
Agent Benchmarks Need Layers

Subtitle:
Coding tasks are not enough. Reconciliation and DD expose auditability, recovery, and verification behavior.

Table:

| Layer | Codex | Fabric+Codex | Hermes+Fabric+Codex |
|---|---:|---:|---:|
| Coding avg | 59.1s | 94.6s | 80.9s |
| Reconciliation | 78s | 83s | 270s |
| Due diligence | 10m48s | 14m52s | 20m34s |

Bottom line:
Use direct Codex for scoped coding. Use orchestration when coverage, audit trail, and recovery matter.

Repo:
https://github.com/GaganaMD/benchmark_hermes-fabric/tree/main

## Caveats

- These are local benchmark runs, not universal performance claims.
- Latency includes end-to-end agent runtime, not just model inference.
- Output quality is not reducible to speed; the DD and reconciliation tasks rewarded verification and artifact completeness.
- The strongest conclusion is about matching orchestration depth to task complexity.
- Repo/artifacts: https://github.com/GaganaMD/benchmark_hermes-fabric/tree/main
