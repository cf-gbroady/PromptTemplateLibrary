# Repair PR 3 — DOCX/PDF Legacy Compatibility Shims

Date: 2026-07-13

## Purpose

This repair continues the skill-library canonicalization work after the XLSX routing and shim repairs.

The goal is to reduce duplicate retrieval surfaces while preserving legacy paths that may still be referenced by old prompts, indexes, or external links.

## Files Converted

- `Skills/skills-docx-v2.md`
- `Skills/skills-pdf-v2.md`

## Canonical Packages

- DOCX: `Skills/docx/SKILL.md`
- PDF: `Skills/pdf/SKILL.md`

## Repair Pattern

Each legacy file is converted into a short compatibility shim that:

1. Preserves the old path.
2. Uses concise frontmatter.
3. Points runtime behavior to the canonical folder-based package.
4. Warns maintainers not to add new behavior to the legacy file.
5. Reduces retrieval competition between old standalone files and modern packaged skills.

## Validation Notes

- Shim descriptions are under the 300-character nebulaONE trigger limit.
- Shim bodies are intentionally short and far below the 30,000-character body limit.
- No files are deleted or renamed.
- `Skills/index.json` already includes legacy compatibility entries for these paths, so this PR does not require an index update.

## Follow-Up Candidates

After this PR, the next likely repair area is the Microsoft 365 skill set:

- `Skills/skill_onedrive_file_intelligence.md`
- `Skills/skill_outlook_productivity.md`
- `Skills/skill_sharepoint_knowledge_collaboration.md`
- `Skills/skill_teams_productivity.md`

Recommended focus: confirmation rules, privacy guardrails, permission boundaries, and Graph/API assumption checks.
