# PromptTemplateLibrary Skills Enhancement Audit

## Scope

This audit records the June 2026 inspection of `cf-gbroady/PromptTemplateLibrary` under `Skills/`, with emphasis on practical improvements that preserve existing behavior while moving the library toward modern Agent Skills conventions.

## Live Repository Shape Observed

The live `Skills/` directory contains both:

- folder-based packages with `SKILL.md`, such as:
  - `Skills/xlsx/SKILL.md`
  - `Skills/lucid-mcp-diagrammer/SKILL.md`
  - `Skills/nebulaONE-SkillGen-Broady/SKILL.md`
  - `Skills/nebulaONE-SkillGen/SKILL.md`
  - `Skills/nebulaone-usage-analytics-workbook-builder/SKILL.md`
  - `Skills/nebulaone-analytics-html-dashboard-builder/SKILL.md`
- legacy standalone markdown skills, such as:
  - `Skills/skills-pdf-v2.md`
  - `Skills/skills-docx-v2.md`
  - `Skills/skills-pptx.md`
  - `Skills/skills-xlsx.md`
  - `Skills/skills-web-research.md`
  - `Skills/skills-compliance-privacy.md`
  - `Skills/skills-citations-grounding.md`
  - `Skills/skills-accessibility.md`

This mixed structure should be treated as intentional until a dedicated migration is approved.

## External Standards Consulted

The enhancement plan was grounded in current public Agent Skills guidance and examples:

- Skills should be concise, structured, discoverable, and tested against real usage.
- `SKILL.md` frontmatter should include a clear `name` and `description`; descriptions drive retrieval/triggering.
- Complex skills should use progressive disclosure by moving long references or deterministic logic to companion files.
- Helper scripts are appropriate when they reduce repeated work, improve deterministic execution, or validate high-risk outputs.
- Common package convention is a skill folder containing `SKILL.md` plus optional `scripts/`, references/docs, examples, and assets.

## Changes Added by This Enhancement

### 1. Reusable audit helper

Added:

```text
Skills/nebulaONE-SkillGen-Broady/scripts/skill_package_audit.py
```

Purpose:

- Scan folder-based and standalone skills.
- Validate frontmatter presence.
- Check `name`, `description`, description length, and body length.
- Detect likely `Skills/index.json` coverage drift.
- Emit JSON and Markdown audit reports.
- Run without third-party dependencies.

### 2. Maintainer standards document

Added:

```text
Skills/nebulaONE-SkillGen-Broady/docs/skill_quality_standards.md
```

Purpose:

- Capture repo-specific standards.
- Preserve the nebulaONE 300-character description target.
- Document when to add helper scripts.
- Provide a migration policy for standalone `.md` skills.
- Define a review checklist for future skill updates.

## Priority Recommendations

| Priority | Area | Recommendation |
|---:|---|---|
| P0 | Safety | Continue secret scanning any helper scripts, docs with URLs, config-like files, or generated examples before commit. |
| P1 | Index drift | Run the new audit helper on a local checkout and compare results to `Skills/index.json`. Update index entries only where paths, descriptions, or helper links have changed. |
| P1 | Description quality | Review descriptions over the nebulaONE 300-character target and compress only when trigger accuracy will not suffer. |
| P1 | Legacy standalone skills | Do not mass-convert standalone files yet; create folder-based successors only when scripts/docs are needed. |
| P2 | Helper opportunities | Consider adding deterministic helpers for document/PDF/PPTX validation only after observing repeated model-generated helper code or recurring output failures. |
| P2 | Progressive disclosure | For large skill bodies, move optional background/reference material into `docs/`, while keeping mandatory runtime steps in `SKILL.md`. |
| P3 | Test prompts | Add 3 realistic trigger/use-case prompts per high-value skill before rewriting the skill body. |

## Suggested Next Batch

1. Run `skill_package_audit.py` against a local clone and save the generated report.
2. Use the report to identify the top 5 drift items.
3. Update only those top 5 items in a separate PR.
4. For any skill with repeated deterministic work, add a helper script plus a smoke test.
5. Request human review before migrating any standalone markdown skill into a folder package.

## Validation Notes

The new audit helper was syntax-checked and smoke-tested with a miniature sample `Skills/` tree containing one valid package and one invalid standalone file. It correctly emitted a non-zero exit for missing frontmatter/name/description errors.
