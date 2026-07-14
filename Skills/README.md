---
name: skills-library-readme
description: Index and authoring standard for the Skills library. Read this first when adding, editing, or reviewing a skill. Defines packaging, metadata, safety, accessibility, validation, and optional product-profile conventions.
---

# Skills Library

This folder contains reusable Agent Skills. A skill is loaded on demand when its description matches the user's request. Skills must remain model-agnostic unless a package is intentionally scoped to a named product or runtime.

## Default scope

General-purpose skills must not assume:

- a specific company, customer, tenant, deployment architecture, or identity provider;
- access to private knowledge sources, web search, image generation, Code Interpreter, or MCP tools unless the runtime confirms them;
- a particular industry, compliance certification, brand palette, font, or hosting environment;
- that uploaded or connected content is safe to disclose, publish, or send to external tools.

State required capabilities in the skill and provide graceful fallback behavior when they are unavailable.

## Authoring contract

1. Use YAML frontmatter with these required fields:

   ```yaml
   ---
   name: kebab-case-skill-name
   description: A compact statement of what the skill does and when it should trigger.
   ---
   ```

   Repository packages may also include `summary` when supported by `Skills/index.json`.

2. Keep `name` concise, unique, and stable. Use lowercase kebab-case for new package folders and skill identifiers.

3. Treat `description` as retrieval metadata. Name the user's likely intent, files, products, and trigger phrases. Keep nebulaONE descriptions below 300 characters.

4. Keep mandatory runtime behavior in `SKILL.md`. Use `scripts/` for deterministic repeated operations and `docs/`, `examples/`, or `tests/` for supporting material.

5. Preserve model neutrality. Say `the agent` or `the assistant`, not a specific model, unless the skill only works with that model.

6. State tool and access requirements explicitly. Never imply access to a file, tenant, inbox, website, API, or connected service that the runtime has not confirmed.

7. Include task-appropriate safety rules for privacy, regulated data, permissions, external communications, destructive actions, and human review.

8. Validate code, JSON, links, metadata limits, and generated artifacts before committing.

## General output defaults

Unless the user or an intentionally scoped skill provides a profile:

- use neutral, accessible styling rather than a product palette;
- follow WCAG 2.1 AA contrast and structural guidance;
- minimize personal or regulated data and avoid unnecessary reproduction;
- cite only sources actually used and never fabricate links or locators;
- label assumptions, incomplete coverage, and unsupported claims;
- ask before external publication, sending messages, changing permissions, or destructive actions.

## Optional product profiles

Product-specific packages may define a named profile for branding, architecture, privacy, or tool behavior. The package must:

1. identify the profile in its title, purpose, or `When to Use` section;
2. keep product-specific defaults inside that package rather than imposing them on unrelated skills;
3. distinguish verified capabilities from deployment-specific assumptions;
4. avoid unverified security, compliance, residency, or architecture claims;
5. provide neutral behavior when the user requests unbranded output.

The nebulaONE analytics packages are intentionally product-specific. Their palette and admin terminology may remain within those packages, but they are not defaults for the rest of the library.

## Styling profiles

For general-purpose documents, decks, charts, and HTML:

- prefer the user's supplied brand guide or template;
- otherwise use an accessible neutral theme;
- do not infer a company palette from repository ownership or unrelated skills;
- keep semantic colors meaningful and verify contrast.

A product palette may be used only when the user requests it or the active skill is explicitly product-specific.

## Skill index

| Skill | File | Triggers on |
|---|---|---|
| Library standard | `README.md` | Authoring or reviewing skills |
| General output and formatting | `skills-general.md` | Tables, callouts, math, collapsibles, pills, quizzes |
| Data visualization | `skills-data.md` | Uploaded data, charts, dashboards, trends |
| Word documents | `docx/SKILL.md` | Create or analyze `.docx` |
| PDF documents | `pdf/SKILL.md` | Create or analyze `.pdf` |
| PowerPoint | `skills-pptx.md` | Build or edit `.pptx` decks |
| Spreadsheets | `xlsx/SKILL.md` | Create or analyze spreadsheet files |
| Feedback bar | `skills-feedback-form.md` | Append a configured feedback widget |
| Citations and grounding | `skills-citations-grounding.md` | Answer from supplied or connected sources |
| Accessibility | `skills-accessibility.md` | User-facing documents and output |
| Image generation | `skills-image-generation.md` | Images, illustrations, or graphic concepts |
| Privacy and compliance | `skills-compliance-privacy.md` | Personal or regulated data |
| Communications | `skills-communications.md` | Emails, announcements, memos, summaries |
| Web research | `skills-web-research.md` | Current or externally verified information |

Use `Skills/index.json` as the machine-readable registry. Preserve its live schema when adding or updating entries.

## Maintenance

- Keep one primary concern per skill.
- Prefer folder packages with `SKILL.md` for new or substantially migrated skills.
- Preserve compatibility shims when legacy paths are still referenced.
- Update `Skills/index.json` when names, descriptions, paths, links, helpers, triggers, or tags change.
- Run package tests and the proprietary-information scanner before publishing.
- Do not commit customer data, credentials, generated customer analytics, or private deployment details.
