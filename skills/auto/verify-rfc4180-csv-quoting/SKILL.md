---
name: verify-rfc4180-csv-quoting
description: Use when formatting or parsing CSV rows containing special characters like commas, double quotes, or newlines according to RFC 4180.
---
1. Inspect any string fields in CSV rows that may contain commas, double quotes, or newlines.
2. Ensure fields containing these characters are wrapped in leading and trailing double quotes (`"`).
3. Escape any internal double quotes by replacing each `"` with two double quotes (`""`).
4. Write unit tests explicitly covering fields with commas and double quotes, and run tests to verify compliance.
