# Skill Quality Standards for PromptTemplateLibrary

## Purpose

Use this guide when creating, reviewing, or improving skills in `PromptTemplateLibrary`. It converts the current repository conventions plus public Agent Skills guidance into a practical checklist for repeatable skill maintenance.

## Grounding Sources

- Anthropic skill guidance emphasizes concise `SKILL.md` bodies, progressive disclosure through bundled resources, and helper scripts for deterministic operations.
- Anthropic and broader Agent Skills examples use a folder containing `SKILL.md` plus optional `scripts/`, references/docs, and assets.
- OpenAI's skills guidance frames skills as versioned procedure bundles anchored by `SKILL.md`, with scripts/assets used only when the workflow benefits from repeatability or deterministic execution.
- Public skill repositories such as Hugging Face skills and GitHub awesome-copilot show the same package pattern: clear frontmatter, task-specific instructions, and optional scripts/references/assets for specialized workflows.

## PromptTemplateLibrary Conventions Observed

The live library currently contains:

1. Folder-based skills such as `Skills/xlsx/SKILL.md`, `Skills/lucid-mcp-diagrammer/SKILL.md`, and nebulaONE analytics builders.
2. Legacy standalone skill files such as `Skills/skills-pdf-v2.md`, `Skills/skills-docx-v2.md`, and `Skills/skills-web-research.md`.
3. A central `Skills/index.json` used for discovery and manual setup metadata.
4. Existing helper scripts in some packages, notably `xlsx` and `lucid-mcp-diagrammer`.

Do not force-migrate standalone skills unless Broady requests it. Prefer targeted improvements that preserve working trigger names and existing links.

## Required Quality Bar

Each new or updated folder-based skill should include:

```text
Skills/[skill-slug]/
  SKILL.md
  scripts/       # only when deterministic helper code improves reliability
  docs/          # optional long-form guidance; mandatory runtime rules stay in SKILL.md
  examples/      # optional realistic examples/test inputs
  tests/         # optional helper smoke tests
```

Each `SKILL.md` should include frontmatter:

```yaml
---
name: skill-slug
summary: One-sentence human-readable summary.
description: Trigger-focused when-to-use description under 300 characters for nebulaONE.
---
```

## Description Rules

- Treat `description` as the retrieval trigger.
- Keep nebulaONE descriptions under 300 characters unless the repo owner approves a broader limit.
- Include likely user phrases and contexts.
- Avoid implementation details better suited for the body.
- Prefer third-person/action descriptions such as "Analyzes spreadsheets..." or "Use when...".
- Avoid vague descriptions such as "helps with documents".

## Body Rules

- Keep the runtime body under 30,000 characters.
- Put mandatory behavior directly in `SKILL.md`.
- Move long references, optional examples, and background material to `docs/` or `examples/`.
- Use progressive disclosure: reference companion files from `SKILL.md` only when the active task needs them.
- Use one-level links from `SKILL.md`; avoid nested reference chains.
- Use forward-slash paths.

## Helper Script Rules

Add helper scripts only when they prevent repeated work, improve determinism, or provide objective validation.

Good candidates:

- schema/frontmatter validation
- spreadsheet normalization
- deterministic report generation
- diagram import scaffolding
- syntax or artifact validation
- repeatable export/packaging operations

Avoid helpers that merely wrap one obvious command or duplicate instructions already handled reliably by the model.

Helper scripts should:

- use standard library or clearly documented dependencies
- run from the command line
- provide `--help`
- fail loudly with actionable errors
- write predictable outputs
- avoid network access unless explicitly documented
- include smoke-testable examples

## Audit Workflow

When asked to inspect or improve the skills library:

1. Read `Skills/`, `Skills/index.json`, and at least one representative folder-based skill.
2. Research current Agent Skills standards if web access is available.
3. Run `scripts/skill_package_audit.py` from this package against a local checkout when filesystem access is available:

```bash
python Skills/nebulaONE-SkillGen-Broady/scripts/skill_package_audit.py \
  --repo-root . \
  --json-out /tmp/skill_audit.json \
  --md-out /tmp/skill_audit.md
```

4. Prioritize fixes:
   - missing/invalid frontmatter
   - descriptions that do not trigger correctly
   - missing runtime instructions
   - unreferenced or absent helper scripts where deterministic work is repeated
   - index drift
   - oversized bodies that need progressive disclosure
5. Make targeted changes on a feature branch and open a PR.
6. Report description character counts, body character counts, helper validation, index validation, and secret scanning.

## Migration Guidance

For standalone `.md` skills, prefer one of these paths:

- **Leave as-is** when the skill is working and indexed.
- **Add a folder-based successor** only when helper scripts/docs are needed.
- **Migrate to `Skills/[slug]/SKILL.md`** only when Broady explicitly approves link/path changes.

When migrating, preserve trigger identity, old links where practical, and update `Skills/index.json`.

## Review Checklist

Before committing skill changes:

- [ ] Current file/folder state was inspected.
- [ ] Relevant external standards or product docs were checked, or lack of research access was stated.
- [ ] Frontmatter has `name`, `summary` where supported, and `description`.
- [ ] Description is under 300 characters for nebulaONE.
- [ ] Body is under 30,000 characters.
- [ ] Mandatory runtime instructions are in `SKILL.md`.
- [ ] Companion files are useful and linked or clearly discoverable.
- [ ] Helper scripts pass syntax/import/smoke tests.
- [ ] `Skills/index.json` remains valid JSON when changed.
- [ ] No secrets or sensitive data are committed.
- [ ] PR summary includes changed files, validation, and follow-up recommendations.
