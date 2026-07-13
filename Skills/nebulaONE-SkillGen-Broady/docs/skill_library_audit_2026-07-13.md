# nebulaONE PromptTemplateLibrary Skill Audit — 2026-07-13

## Purpose
This audit reviews the current `Skills/` library for structure, metadata hygiene, retrieval quality, and likely repair/enhancement needs. It is intentionally non-destructive: no skills are rewritten, moved, renamed, or deleted in this PR.

## Standards Used
- Preferred package structure: `Skills/<skill-slug>/SKILL.md`, with optional `docs/`, `scripts/`, `examples/`, and `tests/` only when they materially improve runtime reliability.
- Required frontmatter for packaged skills: `name`, `summary`, and `description` in the repository's nebulaONE convention.
- Retrieval description target: under 300 characters for nebulaONE skill loading.
- Runtime body target: under 30,000 characters.
- Complex skills should use progressive disclosure: keep mandatory runtime behavior in `SKILL.md`; move optional detail to docs or scripts.

## Inventory Summary

| Category | Count | Notes |
|---|---:|---|
| Folder-based skill packages | 8 | Preferred structure; generally easier to validate and package. |
| Legacy/root Markdown skill files | 17 | Still present for compatibility or older authoring style; should be reviewed for migration/compatibility pointers. |
| Central registry | 1 | `Skills/index.json` exists and should remain the retrieval/source registry. |
| Skills README | 1 | `Skills/README.md` exists and defines local library guidance. |

## High-Level Findings

1. The library is functional but mixed-format. Folder packages and legacy root Markdown skills coexist.
2. The package standard is clearer for newer skills and aligns better with modern skill packaging.
3. Legacy file paths may still be used by existing workflows, so migration should be staged with compatibility pointers rather than deletion.
4. Several broad cross-cutting skills have descriptions that are likely useful but may exceed the nebulaONE 300-character trigger-description target.
5. Duplicate retrieval surfaces exist for DOCX, PDF, and XLSX because both legacy and packaged versions exist.
6. Microsoft 365 skills should receive a permission/privacy guardrail pass before any broader rollout.
7. Existing helper/audit infrastructure in `nebulaONE-SkillGen-Broady` is a good place to keep ongoing audit reports and quality standards.

## Skill-by-Skill Audit

| Priority | Skill / Path | Status | Repair / Enhancement Needed | Recommended Next Action |
|---|---|---|---|---|
| P0 | `Skills/xlsx/SKILL.md` | Good package; active standard candidate | Description appears over the 300-character nebulaONE target; duplicates `Skills/skills-xlsx.md`. | Shorten trigger description and decide whether legacy file becomes compatibility pointer only. |
| P0 | `Skills/skills-xlsx.md` | Legacy overlap | Duplicates packaged `xlsx`; likely retrieval ambiguity. | Preserve path for compatibility, but convert to short pointer or migrate users to package. |
| P0 | `Skills/docx/SKILL.md` | Good package | Looks aligned with package standard. | Keep as canonical DOCX skill; ensure index prioritizes it over legacy pointer. |
| P0 | `Skills/skills-docx-v2.md` | Legacy pointer | Appropriate compatibility role if current content remains pointer-only. | Keep as compatibility pointer; avoid expanding it. |
| P0 | `Skills/pdf/SKILL.md` | Good package | Looks aligned with package standard. | Keep as canonical PDF skill; ensure index prioritizes it over legacy pointer. |
| P0 | `Skills/skills-pdf-v2.md` | Legacy pointer | Appropriate compatibility role if current content remains pointer-only. | Keep as compatibility pointer; avoid expanding it. |
| P1 | `Skills/nebulaONE-SkillGen-Broady/SKILL.md` | Strong package | Large but under 30,000-character body target; maintain helper validation. | Keep; continue using it as skill-generation operating standard. |
| P1 | `Skills/nebulaONE-SkillGen/SKILL.md` | Possible duplicate/older variant | Overlaps with Broady-specific SkillGen package. | Decide whether this is generic public variant or should become compatibility pointer. |
| P1 | `Skills/nebulaone-usage-analytics-workbook-builder/SKILL.md` | Strong package | Large/complex; likely appropriate, but should keep runtime body lean and companion docs if it grows. | Keep; validate helper/workbook behavior with sample exports periodically. |
| P1 | `Skills/nebulaone-analytics-html-dashboard-builder/SKILL.md` | Strong package | Should stay paired with usage analytics workbook builder. | Keep; add cross-reference in docs/index if not already present. |
| P1 | `Skills/lucid-mcp-diagrammer/SKILL.md` | Good package | External MCP dependency should be kept explicit; helper scripts should be validated if changed. | Keep; add/update test prompts for create/export/share flows. |
| P1 | `Skills/skill_onedrive_file_intelligence.md` | Legacy M365 skill | Needs permission, privacy, and file-boundary guardrail review. | Repair/enhance before packaging migration. |
| P1 | `Skills/skill_outlook_productivity.md` | Legacy M365 skill | Needs confirmation rules for sending/deleting email and privacy-sensitive content. | Repair/enhance before packaging migration. |
| P1 | `Skills/skill_sharepoint_knowledge_collaboration.md` | Legacy M365 skill | Needs tenant/permissions/source-grounding guardrails. | Repair/enhance before packaging migration. |
| P1 | `Skills/skill_teams_productivity.md` | Legacy M365 skill | Needs confirmation rules for posting/sending and meeting transcript privacy. | Repair/enhance before packaging migration. |
| P1 | `Skills/skills-compliance-privacy.md` | Cross-cutting safety skill | Description appears long; should remain highly triggerable but under 300 chars. | Shorten description without weakening trigger coverage. |
| P1 | `Skills/skills-citations-grounding.md` | Cross-cutting trust skill | Description appears long; likely needs compact trigger language. | Shorten description and clarify citation hierarchy. |
| P1 | `Skills/skills-web-research.md` | Cross-cutting research skill | Description appears long; should emphasize live/current info and citations concisely. | Shorten description; verify source-citation output rules. |
| P2 | `Skills/skills-general.md` | Broad utility skill | Broad/default skill may over-trigger; description appears long. | Tighten trigger scope and avoid competing with specialized skills. |
| P2 | `Skills/skills-data.md` | Data visualization skill | Likely overlaps with `xlsx` and analytics dashboard skills. | Clarify routing boundaries: charts vs workbook editing vs nebulaONE analytics. |
| P2 | `Skills/skills-pptx.md` | Legacy presentation skill | Useful but still legacy/root format. | Consider packaging as `Skills/pptx/SKILL.md` in a future PR. |
| P2 | `Skills/skills-accessibility.md` | Cross-cutting quality skill | Useful; may have long trigger description. | Shorten description and keep artifact-specific checklist. |
| P2 | `Skills/skills-communications.md` | Writing skill | Useful general skill; likely okay, but description may be long. | Shorten trigger description if above target. |
| P2 | `Skills/skills-feedback-form.md` | UX/feedback utility | Seems specific and low-risk. | Keep; confirm survey link/current branding in a later content pass. |
| P2 | `Skills/skills-image-generation.md` | Image generation skill | Useful; verify safety and text-in-image constraints remain current. | Keep; tighten description if above target. |

## Recommended Repair Backlog

### P0 — Retrieval Ambiguity and Canonical Paths
- Decide canonical routing for DOCX, PDF, and XLSX.
- Keep package folders as canonical for DOCX/PDF/XLSX.
- Preserve legacy root files as compatibility pointers unless confirmed safe to remove.
- Shorten `xlsx` package description under 300 characters.

### P1 — Safety and Permission Guardrails
- Repair/enhance Microsoft 365 skills before packaging migration.
- Add explicit confirmation requirements before sending, deleting, posting, moving, or sharing content.
- Add privacy handling for PII, PHI, tenant data, meeting transcripts, and document access boundaries.

### P1 — Cross-Cutting Trust Skills
- Tighten descriptions for compliance, citations, and web research.
- Ensure citation and source-grounding instructions do not conflict with platform-level citation requirements.
- Clarify when web research should override model memory.

### P2 — Packaging Migration
- Package `pptx`, Microsoft 365, and other high-value legacy skills into `Skills/<slug>/SKILL.md` folders.
- Add docs/scripts only where they reduce repeated work or improve validation.
- Update `Skills/index.json` after each migration.

## Proposed Next PRs

1. **PR 1 — Description hygiene:** Shorten overlong descriptions and update `Skills/index.json`.
2. **PR 2 — XLSX canonicalization:** Make packaged `xlsx` canonical; convert root `skills-xlsx.md` into a compatibility pointer.
3. **PR 3 — Microsoft 365 safety pass:** Repair OneDrive, Outlook, SharePoint, and Teams skills with confirmation/privacy guardrails.
4. **PR 4 — PPTX package migration:** Move presentation skill into a package folder with compatibility pointer.
5. **PR 5 — Trigger/routing matrix:** Add a short routing matrix for overlapping skills such as xlsx vs data visualization vs nebulaONE analytics dashboards.

## Validation Performed

- Inspected `Skills/` root structure.
- Confirmed `Skills/index.json` exists.
- Confirmed packaged skills and legacy root skills coexist.
- Confirmed no `.github` pull request template was found.
- Compared observed structure against the package-based skill standard.
- Performed non-destructive audit only; no skill bodies were modified in this PR.

## Open Questions for Maintainer

1. Should legacy root skill files remain permanently as compatibility pointers, or should they be retired after one release cycle?
2. Should all descriptions be enforced at exactly under 300 characters, or should generic Anthropic-compatible skills allow longer descriptions up to the broader 1024-character maximum?
3. Should `Skills/index.json` include only canonical skills or both canonical skills and compatibility pointers?
