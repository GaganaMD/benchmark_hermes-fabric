# TASK
Explain the data flow from `api/handlers.py` → `services/user.py` → `db/repo.py` when a new user signs up.

# OUTPUT FORMAT
## ENTRYPOINT
Function and `file:line` where the request lands.

## CALL CHAIN
Ordered list of cross-file calls. Format: `file:line — caller() → file:line callee()`.

## STATE MUTATIONS
What gets written to the DB, in order, with the SQL statement.

## EXIT PATHS
All return paths (201, 400, 409). For each, the `file:line` where the response is shaped and the trigger condition.

# CONSTRAINTS
- Cite `file:line` for every claim.
- Mark unverified hops with "(?)".
- Do not modify any file.

# VERIFICATION
None — read-only.
