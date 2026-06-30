# DOCX/PDF Legacy Pointer Remediation

## Scope

This follow-up replaces the legacy standalone DOCX/PDF skill bodies with compact compatibility pointers:

- `Skills/skills-docx-v2.md`
- `Skills/skills-pdf-v2.md`

The preferred folder-based packages remain the source of truth:

- `Skills/docx/SKILL.md`
- `Skills/pdf/SKILL.md`

## Rationale

PR #5 introduced modern progressive-disclosure packages for DOCX and PDF work. This follow-up reduces runtime context load from legacy paths while preserving backwards-compatible file locations for existing imports, bookmarks, and index entries.

## Guardrails

- Legacy paths are preserved.
- No preferred package files are changed.
- No helper scripts are changed.
- The compatibility files route users to the preferred package and restate only mandatory safety behavior.
- `Skills/index.json` already marks the preferred and legacy entries, so no index change is required in this pass.

## Validation

- Pointer descriptions are under 300 characters.
- Pointer bodies are under 30,000 characters.
- Existing preferred DOCX/PDF packages were read before this change.
- Existing legacy files were read before replacement.
