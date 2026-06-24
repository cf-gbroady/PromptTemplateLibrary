---
name: nebulaONE-SkillGen
summary: Create a reusable nebulaONE skill.md file from the current conversation.
description: Use when asked to turn the current conversation into a reusable nebulaONE skill.md file. Produces only the skill file; does not create helpers, folders, or GitHub commits.
---

# nebulaONE-SkillGen

## Purpose

Use this skill to convert the current conversation into a clean, reusable `skill.md` file that any nebulaONE user can manually copy into a nebulaONE skill.

This skill creates **only one Markdown file**: `SKILL.md`. Do not create helper code, folders, docs, GitHub commits, pull requests, images, spreadsheets, or additional artifacts unless the user explicitly asks outside this skill's scope.

## nebulaONE Skill Constraints

Every generated skill must respect these nebulaONE limits:

- Skill title/name: concise, unique, and appropriate to the task.
- Description: **less than 300 characters**.
- Description purpose: acts as the "when to use" trigger used to retrieve and inject the skill body.
- Body: **maximum 30,000 characters**.
- Body purpose: operational instructions added to the prompt/conversation when the skill triggers.

If a skill would exceed 30,000 body characters, compress it while preserving mandatory behavior, safety rules, inputs, outputs, and examples.

## Required Inputs

Before creating the file, inspect the entire conversation up to this point and determine whether there is enough information to define:

1. Skill name/title.
2. Trigger description under 300 characters.
3. Intended user/audience.
4. Task the skill should perform.
5. Inputs the skill expects.
6. Outputs the skill must produce.
7. Tools or capabilities it should use, if any.
8. Guardrails, exclusions, and failure behavior.
9. Quality checks before responding.

If any required information is missing or materially ambiguous, ask **one concise consolidated clarifying question** before creating the file.

## Output Rule

When enough information is available:

- Produce a downloadable Markdown file named `SKILL.md`.
- Do not paste the full file body into chat unless artifact/file creation is unavailable.
- In chat, provide only a brief explanation of what the file does and its recommended title/description.
- The generated file must be ready for a user to copy into nebulaONE.

## Required `SKILL.md` Structure

Generate the file using this structure:

```markdown
---
name: [unique-skill-name]
summary: [one-sentence summary]
description: [trigger description under 300 characters]
---

# [Skill Display Name]

## Purpose

[What this skill does and when it should be loaded.]

## When to Use

- [Specific trigger condition]
- [Specific trigger condition]

## Do Not Use When

- [Exclusion or non-trigger]
- [Exclusion or non-trigger]

## Inputs to Consider

- [Conversation content, uploaded files, URLs, tool outputs, user-provided context, etc.]

## Workflow

1. [Step-by-step operating process.]
2. [Clarify only when required.]
3. [Use tools only when needed.]
4. [Produce the required output.]

## Output Requirements

- [Format]
- [Completeness standard]
- [Quality standard]

## Guardrails

- [Security, privacy, accuracy, compliance, and user-confirmation rules.]

## Quality Checklist

Before responding, confirm:

- [Checklist item]
- [Checklist item]
```

## Writing Standards

- Make the generated skill self-contained.
- Put all mandatory instructions in the body; do not rely on external documents unless the user explicitly wants references.
- Keep triggers specific enough to avoid accidental loading.
- Keep the description under 300 characters and optimized for retrieval.
- Use direct imperative instructions.
- Avoid hidden assumptions.
- Avoid product or capability claims not supported by the conversation.
- If the skill uses tools, specify when to use them and when not to.
- If the skill may create or modify files, specify file-naming, versioning, and validation rules.
- If the skill may perform destructive or external actions, require confirmation unless the conversation explicitly authorizes that action.

## Final Response After File Creation

After creating `SKILL.md`, respond briefly with:

1. The skill name.
2. The description character count.
3. A link or attachment to the generated Markdown file.
4. Any assumptions or open items requiring future iteration.
