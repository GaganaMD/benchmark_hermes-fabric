# Prompt diff
variant: fabric
trial: trial1_20260526T095002Z

raw_bytes=116
final_bytes=1921

```diff
- explain the data flow from `api/handlers.py` through `services/user.py` into `db/repo.py` when a new user signs up.
+ ANSWER:
+ When a new user signs up, the flow typically moves through three layers with clear responsibility boundaries:
+ 
+ 1. **`api/handlers.py` (request/response layer)**
+    - Receives the signup HTTP request (e.g., JSON with email/password/name).
+    - Parses and validates request shape/basic constraints (required fields, format checks).
+    - Calls into the service layer (likely something like `services.user.create_user(...)`).
+    - Translates service results/exceptions into HTTP responses (e.g., `201 Created`, `400 Bad Request`, `409 Conflict`).
+ 
+ 2. **`services/user.py` (business logic layer)**
+    - Implements signup rules:
+      - normalize inputs (email lowercasing, trimming),
+      - enforce domain rules (password policy, unique email requirement),
+      - hash password before persistence,
+      - maybe trigger side effects (welcome email, audit event).
+    - Coordinates with `db/repo.py` for data access:
+      - checks whether user exists,
+      - builds a user entity/model,
+      - requests insert/save.
+    - Returns either a domain object/DTO for the handler or raises domain-specific errors (e.g., `UserAlreadyExists`).
```