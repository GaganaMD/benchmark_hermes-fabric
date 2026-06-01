# task02_comparative_summary

Batch: 20260526T094832Z
Scope: Task02 only; sequential variants only; no matrix scheduler.

Succeeded: hermes
Partially failed: none
Timeout/sandbox constrained: raw, fabric, fabric-improve, fabric-stitch, hermes-fabric

Existing earlier successful hermes-fabric run retained: trial1_20260526T091744Z.
New comparative run preserved without overwriting prior history.

## Per-variant runtime snapshot
- raw: status=timeout, rc=124, total_ms=90000, prompt_expansion=1.00, artifacts=18/18
- fabric: status=timeout, rc=124, total_ms=90000, prompt_expansion=16.56, artifacts=18/18
- fabric-improve: status=timeout, rc=124, total_ms=90000, prompt_expansion=5.47, artifacts=18/18
- fabric-stitch: status=timeout, rc=124, total_ms=90000, prompt_expansion=na, artifacts=15/18
- hermes: status=success, rc=0, total_ms=54870, prompt_expansion=1.00, artifacts=18/18
- hermes-fabric: status=timeout, rc=124, total_ms=90000, prompt_expansion=14.81, artifacts=18/18

## Known issues
- Five variants hit timeout wrapper (90s) and were marked timeout_inferred when native run.json was absent.
- Semantic output quality/hallucination cannot be concluded from runtime-only evidence.