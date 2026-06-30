# Second-Pass Skill Remediation Prioritization

## Purpose

This document prioritizes the next safe enhancement pass for `cf-gbroady/PromptTemplateLibrary` after the initial audit helper and standards package were merged.

The goal is to improve runtime reliability, discoverability, and maintainability of the skill library without breaking existing links, changing active skill identities, or moving legacy standalone files without explicit approval.

## Current Repository State

- `Skills/` contains both modern folder-based packages such as `Skills/xlsx/SKILL.md` and legacy standalone Markdown skills such as `Skills/skills-docx-v2.md`.
- `Skills/index.json` exists and should remain the canonical machine-readable index until a broader index migration is explicitly approved.
- `Skills/nebulaONE-SkillGen-Broady/scripts/skill_package_audit.py` is now available for local quality checks and should be run before each skill-maintenance PR.
- Some legacy skills are large enough to merit decomposition into package folders with companion references or helper scripts, but path migration should be deliberate.

## Prioritization Criteria

Use this order when selecting work for follow-up PRs:

1. **Runtime retrieval risk**
   - Missing or weak trigger descriptions.
   - Skill descriptions over the nebulaONE 300-character target.
   - Ambiguous skill names that could over-trigger or under-trigger.
2. **Operational reliability risk**
   - Instructions that depend on manual, repeated, deterministic steps that should be supported by scripts.
   - Skills that produce files but lack validation steps, naming/versioning rules, or failure handling.
3. **Safety and compliance risk**
   - Skills involving privacy, compliance, regulated data, citations, source handling, or external systems.
   - Instructions that allow destructive actions without confirmation.
4. **Maintenance burden**
   - Oversized monolithic skill files where progressive disclosure would make behavior easier to maintain.
   - Duplicate or overlapping legacy and package-based skills.
5. **User value**
   - Frequently used document, spreadsheet, PDF, and productivity skills.
   - Skills that support common enterprise workflows or recurring nebulaONE administration tasks.

## Recommended Second-Pass Work Items

| Priority | Target | Recommended Action | Rationale | Risk |
|---:|---|---|---|---|
| P0 | `Skills/index.json` | Run audit helper and reconcile index coverage for all skill packages and retained standalone skills. | Discoverability depends on a complete, valid index. | Low if path identities are preserved. |
| P0 | `Skills/skills-docx-v2.md` | Split into a folder package in a future PR only after confirming path compatibility; meanwhile add a remediation note and audit it for body length, trigger clarity, and helper opportunities. | File is large and likely exceeds ideal runtime size; DOCX work benefits from deterministic helpers. | Medium because path migration may break consumers. |
| P0 | `Skills/skills-pdf-v2.md` | Review for trigger precision, validation/failure handling, and whether extraction/inspection helper guidance should be externalized. | PDF workflows often need strict source-grounding, page citation, and file-handling rules. | Low to medium. |
| P1 | `Skills/skills-xlsx.md` and `Skills/xlsx/SKILL.md` | Compare overlap and decide whether the folder-based `xlsx` package supersedes or complements the legacy standalone file. | Duplicate spreadsheet skills can cause retrieval ambiguity. | Medium if content is merged incorrectly. |
| P1 | Microsoft 365 standalone skills | Review `skill_onedrive_file_intelligence.md`, `skill_outlook_productivity.md`, `skill_sharepoint_knowledge_collaboration.md`, and `skill_teams_productivity.md` for confirmation rules, privacy guardrails, and Graph/API assumptions. | Enterprise collaboration skills need careful permission and data-boundary instructions. | Low if edits are instruction-only. |
| P1 | Safety/meta skills | Review `skills-citations-grounding.md`, `skills-compliance-privacy.md`, and `skills-web-research.md` against source-citation and privacy standards. | These skills affect trust and safety across many workflows. | Low. |
| P2 | Short general skills | Normalize frontmatter and trigger descriptions where missing or weak. | Improves retrieval and index quality. | Low. |

## Proposed PR Sequence

### PR 3 — Index and retrieval hygiene

Scope:
- Run the audit helper against a local clone.
- Update `Skills/index.json` entries where paths, raw URLs, descriptions, or tags are missing or stale.
- Do not move skill files.
- Do not rewrite large skill bodies.

Acceptance criteria:
- `Skills/index.json` parses as valid JSON.
- Every folder-based `Skills/*/SKILL.md` package has an index entry.
- Retained standalone skills are either indexed or explicitly listed as legacy/unindexed with rationale.
- Descriptions are under 300 characters where this repo uses nebulaONE retrieval constraints.

### PR 4 — DOCX and PDF progressive-disclosure remediation

Scope:
- Evaluate `skills-docx-v2.md` and `skills-pdf-v2.md`.
- Extract long reference material into `docs/` or `references/` only if it does not weaken runtime instructions.
- Add or reference deterministic helper guidance only when it reduces repeated manual work.
- Preserve existing public paths unless a migration is approved.

Acceptance criteria:
- Mandatory runtime behavior remains in the loaded skill body.
- Body size is reduced or justified.
- File-generation naming/versioning and validation rules are explicit.
- No destructive actions are allowed without confirmation.

### PR 5 — Spreadsheet skill consolidation decision

Scope:
- Compare `Skills/skills-xlsx.md` and `Skills/xlsx/SKILL.md`.
- Decide whether to deprecate, cross-link, or merge overlapping behavior.
- Avoid deletion unless explicitly approved.

Acceptance criteria:
- The intended trigger boundary for each spreadsheet skill is explicit.
- `Skills/index.json` reflects the active package strategy.
- Any deprecation note preserves compatibility for existing users.

## Required Validation for Each PR

Before opening each follow-up PR:

1. Run `python Skills/nebulaONE-SkillGen-Broady/scripts/skill_package_audit.py Skills --index Skills/index.json --markdown-report /tmp/skills-audit.md --json-report /tmp/skills-audit.json`.
2. Validate any changed JSON with `python -m json.tool`.
3. Run syntax checks for any changed `.py` files.
4. Run smoke tests for any helper scripts changed or added.
5. Scan code/config-like changed content for secrets when tooling is available.
6. Report description character counts and body character counts for every changed `SKILL.md`.

## Guardrails

- Do not delete, rename, or move legacy standalone skill files without explicit approval.
- Do not add helper files merely for completeness.
- Do not paste long external standards into skill bodies.
- Preserve all mandatory runtime behavior in `SKILL.md`.
- Use companion docs only for extended references, examples, migration plans, or maintainer guidance.
- Keep changes auditable and grouped by remediation theme.
