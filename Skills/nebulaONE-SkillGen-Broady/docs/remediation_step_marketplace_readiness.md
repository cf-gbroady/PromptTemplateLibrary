# Remediation Step: Marketplace Readiness Baseline

## Purpose

Establish a portable catalog and validation boundary so users can discover skills consistently and future marketplace integrations can consume stable source artifacts.

## Changes

- Adds a human-facing marketplace-readiness guide.
- Adds a standard-library audit helper for `Skills/index.json` and canonical packages.
- Adds a versioned policy for required catalog fields, package limits, and failure severity.
- Adds unit tests for valid packages, legacy paths, unindexed packages, name mismatches, and report generation.
- Keeps publication out of the validator; publishing must remain a separate reviewed action.

## Design decisions

- `SKILL.md` remains the portable runtime source.
- `Skills/index.json` remains the repository catalog.
- Marketplace-specific manifests will be adapters rather than replacements for either source.
- Legacy files are reported as migration work, not deleted automatically.
- Product-specific packages remain valid when their scope is explicit.

## Follow-up backlog

1. Run the audit against the full repository and triage high-severity findings.
2. Point the PowerPoint index entry to `Skills/pptx/SKILL.md` and convert the legacy body to a compatibility shim.
3. Package remaining general root skills one at a time.
4. Add ownership/license review fields once the target marketplace requirements are known.
5. Add CI after the baseline report is clean enough to avoid blocking unrelated work.
