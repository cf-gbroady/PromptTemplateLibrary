---
name: pdf-legacy-compatibility-shim
summary: Compatibility pointer for the canonical PDF document skill.
description: Use only when an old prompt or index references Skills/skills-pdf-v2.md; route PDF document work to Skills/pdf/SKILL.md instead.
---

# PDF Legacy Compatibility Shim

## Purpose

This file is retained for backward compatibility with older references to `Skills/skills-pdf-v2.md`.

The canonical PDF document skill is now:

- `Skills/pdf/SKILL.md`
- Raw URL: `https://raw.githubusercontent.com/cf-gbroady/PromptTemplateLibrary/main/Skills/pdf/SKILL.md`

## Runtime Instruction

When this legacy file is encountered, do **not** treat it as a separate PDF skill. Instead:

1. Load and apply `Skills/pdf/SKILL.md` as the canonical PDF document skill.
2. Use the canonical skill for PDF creation, inspection, extraction, splitting, merging, repair, page-aware review, and export guidance.
3. Preserve this file only as a compatibility pointer for older links, indexes, or saved prompts.

## Do Not Use This File For

- Defining new PDF behavior.
- Adding PDF-processing instructions.
- Registering a separate PDF retrieval target.
- Duplicating guidance that belongs in `Skills/pdf/SKILL.md`.

## Maintainer Notes

- Keep this file short so it does not compete with the canonical PDF package during retrieval.
- Future PDF document changes should be made in `Skills/pdf/SKILL.md` and supporting files under `Skills/pdf/`.
- Do not delete this file without first checking for external links or stored prompts that reference `Skills/skills-pdf-v2.md`.
