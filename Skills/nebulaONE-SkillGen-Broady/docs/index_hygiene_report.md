# Skills Index Hygiene Report

This PR normalizes `Skills/index.json` for retrieval hygiene after the second-pass prioritization merge.

## Scope

- Preserves the existing JSON array schema.
- Keeps all existing skill paths intact.
- Adds missing folder-based and legacy skill entries.
- Adds `repositoryPrefix`, `fullyQualifiedLink`, and `rawSkillUrl` consistently.
- Adds concise retrieval descriptions under the nebulaONE 300-character limit.
- Adds lightweight tags for filtering and future remediation planning.

## Guardrails

- No skill files are moved, deleted, or rewritten.
- Legacy standalone Markdown skills remain indexed at their current paths.
- `skills-xlsx.md` is marked as legacy/duplicate-review because `Skills/xlsx/SKILL.md` now exists as the preferred folder-based spreadsheet skill.
- `skills-docx-v2.md` is marked `progressive-disclosure-needed` because it is oversized relative to the nebulaONE skill body target and should be handled in a later PR.

## Validation Performed

- `Skills/index.json` parses as valid JSON.
- Indexed paths were selected from the live `Skills/` tree on `main`.
- All descriptions are below 300 characters.
- Link fields use the repository's canonical `main` URLs:
  - `https://github.com/cf-gbroady/PromptTemplateLibrary/tree/main/`
  - `https://raw.githubusercontent.com/cf-gbroady/PromptTemplateLibrary/main/`

## Recommended Next PR

Proceed with DOCX/PDF progressive-disclosure remediation:

1. Split oversized operational references out of `skills-docx-v2.md` only after deciding whether to preserve the legacy flat file or create a folder package.
2. Keep mandatory runtime behavior in the primary skill file.
3. Move long reference material, examples, or helper details into supporting docs only when runtime does not require immediate injection.
