---
name: nebulaONE-SkillGen
summary: Create a researched, reusable nebulaONE SKILL.md file from the current conversation.
description: Use when asked to turn the current conversation into a reusable nebulaONE SKILL.md file. Produces only the skill file, grounded by targeted research when tools are available.
---

# nebulaONE-SkillGen

## Purpose

Use this skill to convert the current conversation into a clean, reusable `SKILL.md` file that any nebulaONE user can manually copy into a nebulaONE skill.

This skill creates **only one Markdown file**: `SKILL.md`. Do not create helper code, folders, docs, GitHub commits, pull requests, images, spreadsheets, or additional artifacts unless the user explicitly asks outside this skill's scope.

The generated skill should be grounded in the current conversation **and** targeted research from reputable AI-skill resources when research tools are available.

## nebulaONE Skill Constraints

Every generated skill must respect these nebulaONE limits:

- Skill title/name: concise, unique, and appropriate to the task.
- Description: **less than 300 characters**.
- Description purpose: acts as the "when to use" trigger used to retrieve and inject the skill body.
- Body: **maximum 30,000 characters**.
- Body purpose: operational instructions added to the prompt/conversation when the skill triggers.

If a skill would exceed 30,000 body characters, compress it while preserving mandatory behavior, safety rules, inputs, outputs, tool requirements, examples, and failure behavior.

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

## Research Requirement

Before finalizing the skill, perform targeted research when search or browsing tools are available.

Minimum research pattern:

1. Search Anthropic's public skills repository for relevant examples, naming conventions, structure, or helper patterns:
   - `https://github.com/anthropics/skills`
2. Search the user's available PromptTemplateLibrary or other provided skill library for related or duplicate skills.
3. Search reputable AI-skills, prompt-engineering, tool-use, or public documentation sources relevant to the requested skill topic.
4. Prefer primary sources: official docs, well-maintained public repositories, vendor docs, and source code over blogs or summaries.
5. Summarize only the research findings that materially affected the generated skill.

If research tools are unavailable, say so briefly and proceed using the conversation and model knowledge. Do not fabricate research results, repository contents, or external claims.

## Token Conservation and Body Sizing

Generate a body that is appropriately sized for the task. Favor precision over length.

Use these size targets unless the user requests otherwise:

| Skill complexity | Target body length |
|---|---:|
| Simple formatting, routing, or tone skill | 1,000–3,000 characters |
| Standard workflow skill | 3,000–8,000 characters |
| Tool-using or compliance-sensitive skill | 8,000–15,000 characters |
| Complex multi-tool operating procedure | 15,000–25,000 characters |
| Exceptional maximum-detail skill | Up to 30,000 characters |

Avoid token bloat:

- Do not include long background explanations unless needed at runtime.
- Do not duplicate the same rule in multiple sections.
- Do not include examples that do not change behavior.
- Do not paste large external references into the skill body; summarize the operational rule.
- Include all mandatory runtime behavior directly in `SKILL.md`.

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

## Research and Grounding

- [What was searched or what sources should be checked.]
- [Which findings influenced the skill.]
- [Any limitations if research was unavailable.]

## Workflow

1. [Step-by-step operating process.]
2. [Clarify only when required.]
3. [Use tools only when needed.]
4. [Produce the required output.]

## Tool Use

- [Which tools to use and when.]
- [Which tools not to use.]

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
- Put all mandatory runtime instructions in the body.
- Keep triggers specific enough to avoid accidental loading.
- Keep the description under 300 characters and optimized for retrieval.
- Use direct imperative instructions.
- Avoid hidden assumptions.
- Avoid product or capability claims not supported by the conversation or reputable sources.
- If the skill uses tools, specify when to use them and when not to.
- If the skill may create or modify files, specify file-naming, versioning, and validation rules.
- If the skill may perform destructive or external actions, require confirmation unless the conversation explicitly authorizes that action.
- Make body length task-appropriate; avoid token bloat while preserving all mandatory behavior.

## Final Response After File Creation

After creating `SKILL.md`, respond briefly with:

1. The skill name.
2. The description character count.
3. A link or attachment to the generated Markdown file.
4. Research sources checked or a note that research tools were unavailable.
5. Any assumptions or open items requiring future iteration.
