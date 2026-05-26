--- raw_prompt.txt
+++ final_codex_prompt.txt
@@ -1 +1,12 @@
-`tests/test_parser.py::test_handles_empty` is failing. fix it. don't change the test.
+1. Reproduce the targeted failure: run `pytest -x tests/test_parser.py::test_handles_empty`.
+2. Inspect the parser source file(s) implicated by the traceback to identify empty-input handling bug.
+3. Apply a minimal source-only patch (no test changes) using `apply_patch`.
+4. Re-run the targeted test.
+5. Run a broader verification (`pytest -x`).
+6. Report pass/fail against each done condition.
+
+I’m unable to execute edits or test commands because I don’t have access to your repository/runtime in this interface. If you share:
+- the failing traceback from `tests/test_parser.py::test_handles_empty`, and
+- the parser implementation file contents,
+
+I can provide an exact minimal `apply_patch` diff immediately in the requested format.