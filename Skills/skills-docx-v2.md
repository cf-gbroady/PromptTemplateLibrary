---
name: docx-legacy
summary: Compatibility pointer for the preferred DOCX skill package.
description: Legacy DOCX skill path retained for compatibility. Prefer Skills/docx/SKILL.md for Microsoft Word .docx creation, editing, inspection, extraction, and quality checks.
---

# DOCX Legacy Compatibility Pointer

This legacy standalone skill path is retained so existing bookmarks, imports, and index entries continue to work.

For all new DOCX work, use the preferred folder-based skill package:

- Preferred runtime skill: `Skills/docx/SKILL.md`
- DOCX workflows reference: `Skills/docx/references/docx_workflows.md`
- Accessibility and quality checklist: `Skills/docx/references/accessibility_quality.md`
- Read-only inspection helper: `Skills/docx/scripts/docx_inspect.py`

## When to Use

Use this compatibility file only when a consumer still references `Skills/skills-docx-v2.md` directly. Otherwise, load `Skills/docx/SKILL.md`.

## Required Routing Behavior

1. Treat `Skills/docx/SKILL.md` as the source of truth for DOCX runtime instructions.
2. Preserve originals and never overwrite user-uploaded or repository source documents.
3. Inspect existing `.docx` files before editing them.
4. Use the folder package references for detailed workflows rather than expanding this legacy file.
5. Report any dependency or accessibility limitations clearly.

## Migration Note

This file intentionally replaces the former oversized standalone DOCX body with a compact pointer to reduce runtime context load and align with progressive-disclosure skill packaging.
