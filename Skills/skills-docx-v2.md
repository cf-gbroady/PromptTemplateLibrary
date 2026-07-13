---
name: docx-legacy-compatibility-shim
summary: Compatibility pointer for the canonical DOCX Word document skill.
description: Use only when an old prompt or index references Skills/skills-docx-v2.md; route Word document work to Skills/docx/SKILL.md instead.
---

# DOCX Legacy Compatibility Shim

## Purpose

This file is retained for backward compatibility with older references to `Skills/skills-docx-v2.md`.

The canonical Word document skill is now:

- `Skills/docx/SKILL.md`
- Raw URL: `https://raw.githubusercontent.com/cf-gbroady/PromptTemplateLibrary/main/Skills/docx/SKILL.md`

## Runtime Instruction

When this legacy file is encountered, do **not** treat it as a separate DOCX skill. Instead:

1. Load and apply `Skills/docx/SKILL.md` as the canonical DOCX/Word document skill.
2. Use the canonical skill for Word document creation, editing, inspection, cleanup, style preservation, accessibility checks, and export guidance.
3. Preserve this file only as a compatibility pointer for older links, indexes, or saved prompts.

## Do Not Use This File For

- Defining new Word document behavior.
- Adding DOCX-processing instructions.
- Registering a separate DOCX retrieval target.
- Duplicating guidance that belongs in `Skills/docx/SKILL.md`.

## Maintainer Notes

- Keep this file short so it does not compete with the canonical DOCX package during retrieval.
- Future Word document changes should be made in `Skills/docx/SKILL.md` and supporting files under `Skills/docx/`.
- Do not delete this file without first checking for external links or stored prompts that reference `Skills/skills-docx-v2.md`.
