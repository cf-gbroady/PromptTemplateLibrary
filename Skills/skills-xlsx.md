---
name: xlsx-legacy-compatibility-shim
summary: Compatibility pointer for the canonical XLSX spreadsheet skill.
description: Use only when an old prompt or index references Skills/skills-xlsx.md; route spreadsheet work to Skills/xlsx/SKILL.md instead.
---

# XLSX Legacy Compatibility Shim

## Purpose

This file is retained for backward compatibility with older references to `Skills/skills-xlsx.md`.

The canonical spreadsheet skill is now:

- `Skills/xlsx/SKILL.md`
- Raw URL: `https://raw.githubusercontent.com/cf-gbroady/PromptTemplateLibrary/main/Skills/xlsx/SKILL.md`

## Runtime Instruction

When this legacy file is encountered, do **not** treat it as a separate spreadsheet skill. Instead:

1. Load and apply `Skills/xlsx/SKILL.md` as the canonical XLSX/spreadsheet skill.
2. Use the canonical skill for spreadsheet files, workbook creation, workbook repair, tabular data cleanup, formulas, pivots, charts, validation, and spreadsheet export.
3. Preserve this file only as a compatibility pointer for older links, indexes, or saved prompts.

## Do Not Use This File For

- Defining new spreadsheet behavior.
- Adding workbook-processing instructions.
- Registering a separate XLSX retrieval target.
- Duplicating guidance that belongs in `Skills/xlsx/SKILL.md`.

## Maintainer Notes

- Keep this file short so it does not compete with the canonical XLSX package during retrieval.
- Future spreadsheet changes should be made in `Skills/xlsx/SKILL.md` and supporting files under `Skills/xlsx/`.
- Do not delete this file without first checking for external links or stored prompts that reference `Skills/skills-xlsx.md`.
