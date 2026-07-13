# PPTX Progressive-Disclosure Remediation Report

## Summary

This remediation adds a preferred folder-based PPTX skill package while preserving the existing legacy standalone `Skills/skills-pptx.md` path.

## Changes

- Added `Skills/pptx/SKILL.md` as the preferred runtime entry point.
- Added one-level reference files:
  - `Skills/pptx/references/pptx_workflows.md`
  - `Skills/pptx/references/pptx_accessibility.md`
- Added a read-only, standard-library inspection helper:
  - `Skills/pptx/scripts/pptx_inspect.py`
- Added a smoke test for the helper:
  - `Skills/pptx/tests/test_pptx_inspect.py`
- Updated `Skills/index.json` so retrieval can prefer the folder-based PPTX package while retaining the legacy standalone PPTX entry.

## Research Basis

- Agent Skills guidance favors folder-based packages with a top-level `SKILL.md`, concise frontmatter, progressive disclosure, and optional scripts or references loaded only when needed.
- Skill authoring guidance recommends keeping `SKILL.md` concise, using one-level references, and placing deterministic/repetitive logic in executable scripts.
- `python-pptx` is the primary Python library for creating, reading, and updating PowerPoint 2007+ `.pptx` files without requiring PowerPoint to be installed.
- PowerPoint accessibility guidance emphasizes built-in layouts, unique slide titles, reading order, alt text, readable fonts, sufficient contrast, simple tables, descriptive links, and media captions/transcripts.

## Compatibility

The legacy file `Skills/skills-pptx.md` is preserved in this PR. After this package is reviewed and merged, a follow-up PR can replace the legacy standalone body with a concise compatibility pointer, matching the DOCX/PDF remediation pattern.

## Validation

- `pptx_inspect.py` uses only the Python standard library.
- The helper is read-only and does not modify `.pptx` files.
- Syntax and smoke tests were run locally before committing.
- `Skills/index.json` was validated as JSON.
- Descriptions were kept under the nebulaONE 300-character trigger target.

## Next Step

After this PR is merged, replace `Skills/skills-pptx.md` with a compact compatibility pointer to `Skills/pptx/SKILL.md`.
