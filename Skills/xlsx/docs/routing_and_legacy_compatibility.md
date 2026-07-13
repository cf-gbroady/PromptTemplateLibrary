# XLSX Canonical Routing and Legacy Compatibility

## Purpose

This document defines the canonical routing decision for spreadsheet skills in `PromptTemplateLibrary`.

## Canonical Skill

Use `Skills/xlsx/SKILL.md` as the canonical spreadsheet skill for new nebulaONE and Prompt Library usage.

The canonical XLSX package should be preferred when the user asks to:

- open, inspect, read, clean, normalize, transform, repair, validate, edit, or create spreadsheet files;
- work with `.xlsx`, `.xlsm`, `.csv`, `.tsv`, or spreadsheet-like tabular files;
- create workbook deliverables with formulas, formatting, charts, summaries, or validation checks;
- convert tabular inputs into spreadsheet workbooks;
- preserve workbook formulas, sheet structure, formatting, and source documentation.

## Legacy Skill

`Skills/skills-xlsx.md` is retained for compatibility with older references and manual setup flows.

Do not delete or rename the legacy skill without a separate migration PR. If both skills are available to a runtime, prefer the folder-based package because it supports progressive disclosure through companion documentation and helper scripts.

## Trigger Hygiene Rules

Descriptions and index entries for spreadsheet skills should:

1. Identify the skill as spreadsheet-specific.
2. Include common user language: Excel, spreadsheet, workbook, CSV, XLSX, formulas, pivot tables, charts, clean data, and validate.
3. Avoid over-triggering for unrelated data analysis where no spreadsheet file or spreadsheet deliverable is involved.
4. Route nebulaONE usage analytics exports to the nebulaONE analytics workbook skill when the workbook matches that domain-specific export shape.
5. Route generic spreadsheet manipulation, repair, and workbook generation to `Skills/xlsx/SKILL.md`.

## Near-Miss Routing

Use a different skill when:

- The user asks for a nebulaONE usage analytics workbook from the standard nebulaONE usage export: use `Skills/nebulaone-usage-analytics-workbook-builder/SKILL.md`.
- The user asks for a dashboard from an enriched nebulaONE analytics workbook: use `Skills/nebulaone-analytics-html-dashboard-builder/SKILL.md`.
- The user asks for PDF, DOCX, or PPTX document work without spreadsheet input/output: use the corresponding document skill.
- The user asks for a general explanation of a table pasted in chat and does not want a spreadsheet file: answer directly unless spreadsheet output is requested.

## Recommended Future Repair

A later migration PR should decide whether to:

- convert `Skills/skills-xlsx.md` into a short compatibility shim;
- remove `Skills/skills-xlsx.md` from retrieval surfaces while keeping it in the repository for history;
- update `Skills/index.json` fields to mark `Skills/xlsx/SKILL.md` as canonical and `Skills/skills-xlsx.md` as legacy-only;
- add automated index checks for duplicate trigger descriptions.
