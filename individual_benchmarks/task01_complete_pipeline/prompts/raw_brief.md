# TASK
Explain how `auth/jwt.py` validates and refreshes access tokens.

# OUTPUT FORMAT
Produce four sections, in this order:

## PURPOSE
2–3 sentences on what the module is for.

## FLOW
Numbered list for each public function (`issue`, `validate`, `refresh`).
Cite `auth/jwt.py:<line>` for every step.

## EDGE CASES
Bulleted list. Each item: one-line description + the exception or sentinel returned.

## GOTCHAS
Anything a caller could plausibly get wrong (refresh-as-access, missing `typ`, expired tokens, secret rotation, clock skew).

# CONSTRAINTS
- Do not modify any file.
- Do not invent function names not present in `auth/jwt.py`.
- If a claim is not directly supported by code, omit it.

# VERIFICATION
None — read-only.
