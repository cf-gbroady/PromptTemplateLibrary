# Safety/Meta Skills Description Baseline

## Purpose

This note starts the safety/meta skill repair sequence for:

- `Skills/skills-citations-grounding.md`
- `Skills/skills-compliance-privacy.md`
- `Skills/skills-web-research.md`

The first repair should focus on trigger-description hygiene and evaluation coverage before broad body rewrites.

## Why This Is Next

These skills affect trust, privacy, and factual grounding across many workflows. Their frontmatter descriptions should be compact enough for nebulaONE retrieval while still specific enough to avoid under-triggering or over-triggering.

External skill-authoring guidance treats the frontmatter description as the primary discovery signal and recommends describing both what the skill does and when to use it.

## Proposed Description Targets

| Skill | Current Issue | Proposed Target Description |
|---|---|---|
| `citations-grounding` | Description is long and mixes many examples into metadata. | `Use when responses require citations, source grounding, quote handling, evidence checks, or clear separation between sourced facts and analysis.` |
| `compliance-privacy` | Description is long and should be tightened without losing PII/PHI/regulated-data triggers. | `Use when content may include PII, PHI, student, financial, or regulated data; supports minimization, redaction, safe exports, and privacy review.` |
| `web-research` | Description is long and should emphasize current/external verification concisely. | `Use when current or externally verifiable facts are needed, including latest events, prices, products, people, policies, or source-backed research.` |

## Repair Plan

1. Preserve each skill's existing path and identity.
2. Shorten only the YAML `description` fields in the first direct repair PR.
3. Keep descriptions under 300 characters.
4. Avoid changing the body unless the body contradicts the shortened trigger.
5. Add trigger examples that verify when each skill should and should not activate.
6. After metadata repair, do a second pass on body content for:
   - citation hierarchy and no-fabricated-source rules,
   - privacy minimization and redaction workflows,
   - web source quality, recency, and citation output requirements.

## Trigger Boundary Notes

- Use `citations-grounding` for private knowledge sources, uploaded documents, RAG answers, quotes, and evidence chains.
- Use `compliance-privacy` when user data may contain regulated, personal, student, patient, financial, employment, or confidential information.
- Use `web-research` when the answer depends on current/public external facts or facts that should be verified against live sources.
- More than one safety/meta skill may apply. For example, a current public-policy question with personal data can require both web research and privacy handling.

## Validation Checklist for the Next PR

- [ ] All three descriptions are under 300 characters.
- [ ] Frontmatter remains valid YAML.
- [ ] Existing body content is preserved unless a contradiction is found.
- [ ] `Skills/index.json` entries are checked for consistency with the shortened descriptions.
- [ ] Trigger evals include positive and negative examples.
- [ ] No secrets, customer data, credentials, or private regulated data are introduced.
