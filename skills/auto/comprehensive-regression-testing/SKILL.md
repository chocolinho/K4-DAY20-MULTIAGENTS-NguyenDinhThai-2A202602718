---
name: comprehensive-regression-testing
description: Use when fixing bugs in a codebase to ensure every fixed bug is covered by a dedicated regression test.
---
1. Create or open a dedicated regression test file (e.g., `tests/test_regressions.py`).
2. Add at least one distinct test function for each bug or edge case fixed.
3. Ensure all tests pass successfully by running the test runner with the correct pythonpath.
4. Record each fix in the changelog (`CHANGELOG.md`) under the appropriate heading with standard bullets.
