# DOCX/PDF Progressive-Disclosure Remediation Report

## Scope

This remediation pass creates modern folder-based packages for DOCX and PDF work while preserving the existing legacy standalone files:

- Legacy retained: `Skills/skills-docx-v2.md`
- Legacy retained: `Skills/skills-pdf-v2.md`
- New preferred package: `Skills/docx/SKILL.md`
- New preferred package: `Skills/pdf/SKILL.md`

## Why This Change

The live library contained a large DOCX standalone skill and a PDF standalone skill. Current Agent Skills guidance favors a compact `SKILL.md` frontmatter/body with one-level references and executable helpers for deterministic operations. This structure reduces runtime context load while keeping detailed workflows available on demand.

## Research Applied

- Agent Skills structure and progressive disclosure: folder packages anchored by `SKILL.md`, with optional `references/`, `scripts/`, and assets.
- Skill authoring best practices: concise descriptions, one-level references, validation loops, and scripts for deterministic work.
- DOCX implementation: `python-docx` for creating/updating Word files and core properties; OpenXML ZIP/XML inspection for read-only fallback checks.
- PDF implementation: `pypdf` for page operations and metadata; `pdfplumber` for layout-aware extraction, tables, and visual debugging.
- Accessibility: source-first remediation, semantic headings, alt text, document language, reading order, table headers, and manual verification.

## Files Added

```text
Skills/docx/
  SKILL.md
  references/
    docx_workflows.md
    accessibility_quality.md
  scripts/
    docx_inspect.py

Skills/pdf/
  SKILL.md
  references/
    pdf_workflows.md
    pdf_accessibility.md
  scripts/
    pdf_inspect.py
```

## Guardrails

- No legacy skill files were deleted.
- No existing source document handling rules were weakened.
- Helper scripts do not use network access.
- Helper scripts are read-only inspectors.
- Full accessibility compliance is not claimed from automated checks alone.

## Follow-Up Recommendations

1. After this PR is merged and tested, optionally replace the oversized legacy `skills-docx-v2.md` body with a compatibility pointer to `Skills/docx/SKILL.md`.
2. Consider replacing `skills-pdf-v2.md` with a compatibility pointer after consumers confirm the new `Skills/pdf/` package is discoverable.
3. Add sample fixture files only if real recurring tests require them.
4. Run the skill audit helper against the repository after merging to confirm body-size and index status.
