# Repair PR 1: XLSX Description Hygiene and Canonical Routing

## Scope

This repair pass starts the first follow-up from the skill library standards audit.

It is intentionally non-destructive:

- No legacy skill files are deleted.
- No skill bodies are broadly rewritten.
- The folder-based `Skills/xlsx/SKILL.md` package is documented as the canonical spreadsheet skill for new usage.
- `Skills/skills-xlsx.md` remains available for compatibility until a later migration PR decides whether to convert it into a shim or remove it from retrieval surfaces.

## Research Basis

- Skill packages should use a folder with `SKILL.md` as the entry point.
- YAML frontmatter should include `name` and `description`.
- Descriptions drive skill discovery and should clearly state what the skill does and when to use it.
- Larger or more complex skills should use progressive disclosure through companion files and helper scripts.

## Changes Added

1. `Skills/xlsx/docs/routing_and_legacy_compatibility.md`
   - Defines `Skills/xlsx/SKILL.md` as the canonical spreadsheet skill.
   - Describes when to prefer the legacy standalone file.
   - Lists routing near-misses for nebulaONE analytics, dashboards, PDF, DOCX, PPTX, and simple table explanation.

2. `Skills/xlsx/evals/trigger_routing_evals.json`
   - Adds representative should-trigger and should-not-trigger prompts.
   - Documents expected routing for canonical XLSX, nebulaONE analytics, dashboard, PDF, PPTX, and no-skill cases.

## Validation

- JSON syntax validated locally.
- Description/body-length repair impact is documentation-only in this PR.
- Legacy file deletion intentionally deferred.
- `Skills/index.json` intentionally left unchanged in this PR to avoid changing runtime retrieval behavior before review.

## Recommended Next PR

After this PR is reviewed, the next repair should update `Skills/index.json` and, if approved, convert `Skills/skills-xlsx.md` into a short compatibility shim that points to `Skills/xlsx/SKILL.md`.
