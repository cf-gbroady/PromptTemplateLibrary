---
name: pdf-legacy
summary: Compatibility pointer for the preferred PDF skill package.
description: Legacy PDF skill path retained for compatibility. Prefer Skills/pdf/SKILL.md for PDF creation, inspection, extraction, splitting, merging, summarization, and quality checks.
---

# PDF Legacy Compatibility Pointer

This legacy standalone skill path is retained so existing bookmarks, imports, and index entries continue to work.

For all new PDF work, use the preferred folder-based skill package:

- Preferred runtime skill: `Skills/pdf/SKILL.md`
- PDF workflows reference: `Skills/pdf/references/pdf_workflows.md`
- PDF accessibility checklist: `Skills/pdf/references/pdf_accessibility.md`
- Read-only inspection helper: `Skills/pdf/scripts/pdf_inspect.py`

## When to Use

Use this compatibility file only when a consumer still references `Skills/skills-pdf-v2.md` directly. Otherwise, load `Skills/pdf/SKILL.md`.

## Required Routing Behavior

1. Treat `Skills/pdf/SKILL.md` as the source of truth for PDF runtime instructions.
2. Preserve originals and never overwrite source PDFs.
3. Inspect PDFs before extraction, summarization, splitting, merging, or remediation.
4. Use the folder package references for detailed workflows rather than expanding this legacy file.
5. Report extraction, OCR, encryption, accessibility, and reading-order limitations clearly.

## Migration Note

This file intentionally replaces the former standalone PDF body with a compact pointer to reduce runtime context load and align with progressive-disclosure skill packaging.
