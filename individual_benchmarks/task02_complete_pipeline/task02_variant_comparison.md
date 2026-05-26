# task02_variant_comparison

| Variant | Trial | Success | Status | Runtime(ms) | Raw Prompt Bytes | Final Prompt Bytes | Expansion Ratio | codex.log Bytes | Artifact Completeness | Sandbox/Runtime Issues |
|---|---|---:|---|---:|---:|---:|---:|---:|---|---|
| raw | trial1_20260526T094832Z | no | timeout | 90000 | 116 | 116 | 1.00 | 118 | 18/18 | timeout_90s |
| fabric | trial1_20260526T095002Z | no | timeout | 90000 | 116 | 1921 | 16.56 | 118 | 18/18 | timeout_90s |
| fabric-improve | trial1_20260526T095133Z | no | timeout | 90000 | 116 | 634 | 5.47 | 118 | 18/18 | timeout_90s |
| fabric-stitch | trial1_20260526T095303Z | no | timeout | 90000 | 116 | None | na | None | 15/18 | timeout_90s |
| hermes | trial1_20260526T095433Z | yes | success | 54870 | 116 | 116 | 1.00 | 2275 | 18/18 | none_observed |
| hermes-fabric | trial1_20260526T095528Z | no | timeout | 90000 | 116 | 1718 | 14.81 | 0 | 18/18 | timeout_90s |