# Task03 Comparative Summary

Batch: batch_20260526T103101Z
Task: task03_failing_test

| Variant | rc | Runtime(ms) | Success | Notes |
|---|---:|---:|---|---|
| raw | 0 | 65851 | yes | sandbox_error_detected |
| fabric | 0 | 48042 | yes | sandbox_error_detected |
| fabric-improve | 0 | 58749 | yes | sandbox_error_detected |
| fabric-stitch | 0 | 105804 | yes | sandbox_error_detected |
| hermes | 124 | 300000 | timeout | timeout_signal;run_json_inferred;partial_artifacts |
| hermes-fabric | 0 | 40629 | yes |  |

Scope lock honored: Task 3 only; sequential variants; no matrix scheduler.
