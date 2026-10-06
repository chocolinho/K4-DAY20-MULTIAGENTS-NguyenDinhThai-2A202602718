---
name: adhere-to-strict-naming-and-formatting-rules
description: Use when generating structured output files or package metadata to ensure all keys, fields, service names, and formats strictly match requirements.
---
1. Read all formatting constraints and schema requirements in the task instructions twice.
2. Implement explicit normalization logic for identifiers (e.g., lower-casing, replacing hyphens with underscores, canonical spellings) right before outputting.
3. Validate output fields against the exact naming keys required (e.g., `schema_version`, integer cents for money, specific headers in CSV files).
4. Run a validation check or script over generated output files to verify that all constraints are met before finishing.
