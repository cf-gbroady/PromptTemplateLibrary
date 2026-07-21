# Skills Marketplace Readiness

This repository is moving toward a portable, user-friendly skill catalog that can later be adapted to one or more skills marketplaces.

## User discovery

Use [`Skills/index.json`](index.json) as the machine-readable catalog and this directory's [`README.md`](README.md) as the human-facing authoring guide. Each catalog entry should clearly answer:

- What does the skill do?
- When should it trigger?
- What input or tools does it require?
- Where is its canonical `SKILL.md`?
- Is it general-purpose or intentionally product-specific?

## Canonical portable package

New and migrated skills should use:

```text
Skills/<skill-name>/
  SKILL.md
  scripts/       # optional deterministic helpers
  references/    # optional supporting documentation
  assets/        # optional templates or static resources
  tests/         # optional repository validation
  evals/         # optional trigger or behavior evaluations
```

The `name` in `SKILL.md` must match the folder name. The description must state both what the skill does and when to use it.

## Compatibility paths

Legacy root Markdown files may remain as concise compatibility shims while links are migrated. They should point to the canonical package and should not compete as a second full implementation.

## Marketplace adapter boundary

The repository does not assume a specific future marketplace schema. Instead:

1. `SKILL.md` remains the portable runtime source.
2. `Skills/index.json` remains the repository catalog.
3. Marketplace-specific manifests should be generated as adapters from those sources.
4. Adapter-specific fields must not become mandatory runtime instructions unless the target marketplace requires them.
5. Publishing remains a separate, reviewed action; validation must never publish automatically.

## Readiness checks

Run from the repository root:

```bash
python Skills/nebulaONE-SkillGen-Broady/scripts/skills_marketplace_audit.py \
  --json-output Skills/nebulaONE-SkillGen-Broady/docs/marketplace_readiness_report.json \
  --markdown-output Skills/nebulaONE-SkillGen-Broady/docs/marketplace_readiness_report.md
```

The audit checks:

- index JSON validity and required fields;
- duplicate IDs and paths;
- indexed paths and canonical package coverage;
- folder/frontmatter name alignment;
- description and body limits;
- raw and browser-link consistency;
- legacy paths that still require migration.

## Publication checklist

Before exporting a skill to a marketplace:

- confirm ownership and license terms for instructions, code, templates, and assets;
- remove customer data, credentials, private deployment details, and internal-only links;
- validate the package and run its tests;
- review description triggers for false positives and false negatives;
- document required tools, network access, dependencies, and fallback behavior;
- provide screenshots or examples only when they contain no sensitive data;
- assign a release version in the marketplace adapter;
- require human approval before publication.

## Current migration order

1. Keep DOCX, PDF, PPTX, and XLSX folder packages canonical.
2. Convert remaining full legacy skill files into package folders or compatibility shims.
3. Normalize catalog descriptions, tags, and triggers.
4. Add targeted evals for skills with overlapping retrieval.
5. Generate marketplace-specific manifests only after a target schema is confirmed.
