# Due Diligence Benchmark Comparison

This file is a benchmark-facing summary of the due diligence experiment. It intentionally avoids publishing the underlying company reports, source registers, manifests, extracted text, preview HTML, or detailed source-linked audit trail.

## Benchmark Setup

| Task | Prompt Character Length | Codex Output | Codex Latency | Fabric Enhanced Prompt Character Length | Fabric + Codex Output | Fabric + Codex Latency | Hermes + Fabric + Codex Output | Hermes + Fabric + Codex Latency |
| --- | ---: | --- | ---: | ---: | --- | ---: | --- | ---: |
| Due diligence corpus review | 1,140 | Generated a complete sourced deck and audit artifacts from a recursive folder review. | 10m 48s | 1,758 | Generated the deck target plus Fabric risk-synthesis framing and follow-up structure. | 14m 52s | Generated the deck target with the strongest verification/QA summary and artifact traceability. | 20m 34s |

## Corpus And Output Metrics

| Metric | Value |
| --- | ---: |
| Tree files inventoried | 582 |
| ZIP-contained files expanded/reviewed | 135 |
| Total manifest items reviewed | 717 |
| Extraction errors | 0 |
| Final deck slide count | 21 |

## Benchmark Takeaways

| Setup | What It Showed | Tradeoff |
| --- | --- | --- |
| Codex only | Direct prompting can complete the full artifact-generation task when the done-when criteria are explicit. | Fastest DD run in this benchmark. |
| Fabric + Codex | Fabric-style risk framing and follow-up structure helped shape the synthesis. | Added prompt/orchestration latency. |
| Hermes + Fabric + Codex | The layered workflow produced the strongest QA-style completion summary and traceability checks. | Slowest DD run, but most audit-oriented. |

## Public Safety Boundary

The public repository should keep benchmark-safe summaries like this file, latency charts, thread drafts, and generated benchmark images.

The following remain local-only because they are derived from the private diligence corpus and may contain confidential business, financial, tax, contractual, employment, credential, or source-trace information:

- generated PPTX/PDF diligence reports
- preview HTML files
- manifests and coverage files
- source registers
- image-review files
- extracted text
- ZIP-expanded corpus files
- detailed source-linked risk synthesis files
