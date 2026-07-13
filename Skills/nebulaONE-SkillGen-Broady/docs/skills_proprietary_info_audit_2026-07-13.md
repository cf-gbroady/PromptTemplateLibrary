# Skills Proprietary-Information Audit — 2026-07-13

## Purpose

This audit checks the `Skills/` section for Cloudforce, nebulaONE, proprietary, internal, tenant, customer, and secret-like references before additional public/general-purpose skills are added.

## Scope

Non-destructive audit of the live `Skills/` tree on `main` after PR #19 was merged.

## Confirmed Findings

### P0 — Cloudforce references

Confirmed Cloudforce mentions were found in:

| Path | Finding | Risk |
|---|---|---|
| `Skills/README.md` | Describes the Skills Library as for nebulaONE and Cloudforce's multi-model Azure-based enterprise GenAI gateway. | Public/general library branding and architecture exposure. |
| `Skills/nebulaone-analytics-html-dashboard-builder/SKILL.md` | Uses `Cloudforce-branded` and default title/theme strings containing Cloudforce. | Branded output defaults may leak company branding into generated artifacts. |

Recommended remediation: replace Cloudforce-specific wording with neutral language unless the skill is intentionally private/internal.

### P0 — nebulaONE references

`nebulaONE` references are widespread and appear in:

- README/library standards.
- SkillGen packages and audit docs.
- Analytics workbook/dashboard skills.
- General, data, communications, image-generation, accessibility, citations, compliance/privacy, XLSX routing, and other skill documentation.

Risk depends on intended audience:

- If this repository is public/general-purpose, these should be neutralized or isolated into platform-specific skills.
- If this repository is intentionally nebulaONE-specific, these are mostly expected but still need review for confidential implementation detail.

### P0 — Explicit `license: Proprietary` metadata

Several legacy standalone skills contain `license: Proprietary`, including at least:

- `Skills/skills-web-research.md`
- `Skills/skills-pptx.md`
- `Skills/skills-compliance-privacy.md`
- `Skills/skills-communications.md`
- `Skills/skills-citations-grounding.md`
- `Skills/skills-accessibility.md`
- `Skills/skills-feedback-form.md`
- `Skills/skills-image-generation.md`

Recommended remediation: decide whether this repo should keep proprietary license metadata or replace it with a repository-wide license reference.

### P1 — Platform architecture assumptions

Potentially sensitive platform assumptions appear in:

- `Skills/README.md`: Azure-based enterprise GenAI gateway; customer proprietary data in Azure tenant.
- `Skills/skills-compliance-privacy.md`: customer Azure tenant, SSO/RBAC, compliance positioning.
- `Skills/skills-citations-grounding.md`: RAG over customer private data in Azure tenant.

Recommended remediation: neutralize architecture claims in general-purpose skills; keep detailed architecture only in private/platform-specific documentation if approved.

### P1 — Brand palette and branded UI defaults

Brand palette/default output references appear in:

- `Skills/README.md`
- `Skills/skills-data.md`
- `Skills/skills-general.md`
- `Skills/skills-image-generation.md`
- `Skills/skills-pptx.md`
- `Skills/skills-feedback-form.md`
- `Skills/nebulaone-analytics-html-dashboard-builder/SKILL.md`

Recommended remediation: use neutral defaults such as `user-provided brand guidelines` or `accessible default palette` in general skills.

### P1 — Secret-like search results

Targeted searches for `password` returned benign PDF workflow references to encrypted/password-protected PDFs. Targeted searches for `confidential`, `internal`, and `tenant` mostly returned guardrails or safety language, not exposed secrets. Some GitHub code-search calls were rate-limited, so a follow-up local/scripted scan is recommended.

## Recommended Repair Sequence

1. Decide policy: remove all Cloudforce/nebulaONE mentions, or keep approved platform-specific skills only.
2. Create a debranding PR for `Skills/README.md` and general-purpose skills.
3. Create a platform-isolation PR for analytics/SkillGen skills that intentionally remain nebulaONE-specific.
4. Normalize or remove `license: Proprietary` metadata where appropriate.
5. Add a reusable proprietary-info scan script/eval under `Skills/nebulaONE-SkillGen-Broady/`.
6. Re-run audit after cleanup.

## Notes and Limitations

- This PR is non-destructive and does not rewrite any skill content.
- GitHub code search rate limiting prevented a fully exhaustive search during this pass.
- Secret scanning via GitHub Advanced Security is not enabled for this repository, so this audit should be supplemented with a local regex/secret scanner in a later PR.
