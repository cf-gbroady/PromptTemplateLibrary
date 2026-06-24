---
name: nebulaONE-SkillGen-Broady
summary: Create, research, package, and commit nebulaONE skills to PromptTemplateLibrary.
description: Use when Broady asks to turn the current conversation into a reusable nebulaONE skill package and commit it to PromptTemplateLibrary with researched files/helpers.
---

# nebulaONE-SkillGen-Broady

## Purpose

Use this personal skill when Broady wants to turn the current conversation into a complete nebulaONE skill package and commit it to the GitHub repository:

`https://github.com/cf-gbroady/PromptTemplateLibrary`

This skill may create a `SKILL.md` file, supporting documentation, executable helper files, tests/examples, folder structure, and `Skills/index.json` entries when those assets are useful for the skill being created.

Every generated skill package must be grounded in the conversation **and** targeted research from reputable AI-skill resources, official documentation, and relevant public repositories when tools are available.

## Repository Defaults

Unless Broady says otherwise, use:

- Repository owner: `cf-gbroady`
- Repository name: `PromptTemplateLibrary`
- Branch: `main`, or a new feature branch if review is preferable
- GitHub tree prefix: `https://github.com/cf-gbroady/PromptTemplateLibrary/tree/main/`
- GitHub raw prefix: `https://raw.githubusercontent.com/cf-gbroady/PromptTemplateLibrary/main/`
- Skills root: `Skills/`
- Package path pattern: `Skills/[skill-slug]/`
- Primary skill file: `Skills/[skill-slug]/SKILL.md`
- Optional helper path: `Skills/[skill-slug]/scripts/`
- Optional docs path: `Skills/[skill-slug]/docs/`
- Optional examples path: `Skills/[skill-slug]/examples/`
- Optional tests path: `Skills/[skill-slug]/tests/`
- Index file: `Skills/index.json`

## nebulaONE Skill Constraints

Every generated skill must respect these constraints:

- Description must be **less than 300 characters**.
- Description is the retrieval trigger / "when to use" text.
- Body must be **30,000 characters or less**.
- The body must contain all mandatory behavior needed at runtime.
- External links and helper files may be referenced, but do not assume nebulaONE injects external Markdown or code into the chat unless the runtime explicitly supports it.

## Required Intake Check

Inspect the full conversation and determine whether there is enough information to define:

1. Skill purpose and intended audience.
2. Trigger description under 300 characters.
3. Required outputs.
4. Required tools or external systems.
5. Whether helper code, docs, tests, examples, or folder structure are needed.
6. Whether the skill needs executable Code Interpreter helpers.
7. Safety, privacy, compliance, and confirmation rules.
8. GitHub target path and commit behavior.

If material information is missing, ask **one concise consolidated clarifying question** before creating or committing files.

## Research Workflow

Before finalizing a new or updated skill package, perform targeted research when tools are available:

1. Search Anthropic's public skills repository for a similar skill or relevant design pattern:
   - `https://github.com/anthropics/skills`
2. Search the target PromptTemplateLibrary repository for existing related skills to avoid duplicates and preserve naming, folder, and index conventions.
3. Search other reputable public GitHub repositories, official vendor docs, API docs, or public skill libraries for comparable skills, helper-code patterns, and best practices on the same topic.
4. Prefer primary and reputable sources:
   - official product documentation,
   - maintained source repositories,
   - public examples from AI platform vendors,
   - well-scoped standards or specifications.
5. Summarize what was found and how it influenced the proposed skill.
6. If research tools are unavailable or fail, say so plainly and proceed using the conversation plus model knowledge, with that caveat.

Do not fabricate repository contents, upstream behavior, APIs, helper capabilities, version support, or runtime features.

## Code Interpreter Helper Research and Validation

When a skill package includes executable helper code:

1. Research whether the helper can run in Code Interpreter with commonly available libraries.
2. Prefer Python standard library and commonly available Code Interpreter libraries.
3. Avoid unnecessary external dependencies.
4. If third-party libraries are needed, document them and provide graceful fallback behavior.
5. Use Code Interpreter, when available, to run:
   - syntax checks,
   - import checks,
   - minimal smoke tests,
   - small sample input/output tests.
6. Confirm helper files do not require network access unless explicitly documented.
7. Include clear CLI usage examples in the helper file or documentation.
8. Never assume Code Interpreter can execute a GitHub file directly from a `tree` URL.
9. Prefer raw GitHub URLs for helper download/reference links:
   `https://raw.githubusercontent.com/cf-gbroady/PromptTemplateLibrary/main/Skills/[skill-slug]/scripts/[helper].py`

If exact helper code must be available in Code Interpreter, recommend one of these patterns:

- Upload the helper file into the chat/session.
- Mount/package the helper in the runtime.
- Generate a minimal fit-for-purpose script from the instructions in `SKILL.md`.
- Download from a raw GitHub URL only if the runtime has network access and policy allows it.

## Token Conservation and Body Sizing

Create task-appropriate skill bodies. The goal is operational completeness without token bloat.

Use these default size targets:

| Skill complexity | Target body length |
|---|---:|
| Simple formatting, routing, or tone skill | 1,000–3,000 characters |
| Standard workflow skill | 3,000–8,000 characters |
| Tool-using or compliance-sensitive skill | 8,000–15,000 characters |
| Complex multi-tool operating procedure | 15,000–25,000 characters |
| Exceptional maximum-detail skill | Up to 30,000 characters |

Compression rules:

- Keep mandatory runtime behavior in `SKILL.md`.
- Move expanded explanations, examples, and background into `docs/` when they are useful but not required at runtime.
- Move executable logic into `scripts/` when appropriate, but include enough instructions in `SKILL.md` to use or regenerate a minimal helper when needed.
- Avoid duplicating the same rule across sections.
- Do not paste large external docs into the body; cite or summarize the operational rule.
- Use examples only when they materially improve execution.

## Package Design Rules

Create only the files that are useful for the skill. Common structures:

### Simple skill

```text
Skills/[skill-slug]/
  SKILL.md
```

### Skill with documentation

```text
Skills/[skill-slug]/
  SKILL.md
  docs/
    [supporting-doc].md
```

### Skill with executable helpers

```text
Skills/[skill-slug]/
  SKILL.md
  scripts/
    [helper].py
  docs/
    [supporting-doc].md
  examples/
    [example-input-or-config]
  tests/
    [test-helper].py
```

## `SKILL.md` Requirements

Every generated `SKILL.md` must include:

```markdown
---
name: [skill-slug]
summary: [one-sentence summary]
description: [trigger description under 300 characters]
---

# [Skill Display Name]

## Purpose
## When to Use
## Do Not Use When
## Inputs to Consider
## Research and Grounding
## Workflow
## Tool Use
## Output Requirements
## Guardrails
## Quality Checklist
```

Add other sections only when useful.

The skill body must be self-contained. If supporting docs exist, the `SKILL.md` may link to them, but all mandatory runtime behavior must also be summarized directly in `SKILL.md`.

## `Skills/index.json` Requirements

Update or create `Skills/index.json` with entries for the new or changed skill.

Use this pattern:

```json
{
  "repositoryPrefix": "https://github.com/cf-gbroady/PromptTemplateLibrary/tree/main/",
  "rawPrefix": "https://raw.githubusercontent.com/cf-gbroady/PromptTemplateLibrary/main/",
  "skills": [
    {
      "id": "[skill-slug]",
      "name": "[display name]",
      "title": "[nebulaONE skill title]",
      "summary": "[one-sentence summary]",
      "description": "[under 300 characters]",
      "path": "Skills/[skill-slug]/SKILL.md",
      "fullyQualifiedLink": "https://github.com/cf-gbroady/PromptTemplateLibrary/tree/main/Skills/[skill-slug]/SKILL.md",
      "rawSkillUrl": "https://raw.githubusercontent.com/cf-gbroady/PromptTemplateLibrary/main/Skills/[skill-slug]/SKILL.md",
      "helperUrls": []
    }
  ]
}
```

If the existing repository uses an array instead of a wrapped object, preserve the existing valid structure unless Broady asks to migrate it.

For helper files, include fully qualified raw URLs in `helperUrls` or equivalent existing fields.

## GitHub Commit Workflow

When Broady explicitly asks to upload, publish, or commit the generated skill package, proceed with the GitHub commit workflow.

Recommended flow:

1. Inspect existing repository structure and current `Skills/index.json`.
2. Create or update the package folder.
3. Update `Skills/index.json`.
4. Run secret scanning on any code/config-like file contents before committing, when a secret-scanning tool is available.
5. Commit files to `main` if Broady explicitly requested direct commit; otherwise use a feature branch and open a pull request.
6. Provide the commit SHA or PR link, changed-file list, research summary, validation results, and next recommended test.

Ask for confirmation before destructive actions such as deleting files, force-pushing, closing issues, or merging PRs.

## Output Requirements

For each run, provide:

- Proposed skill name and description character count.
- Research summary with links or caveats.
- File tree to be created or updated.
- Body length and whether it is within the 30,000-character limit.
- Validation performed on helper code.
- GitHub commit or PR details, if committed.
- Manual nebulaONE setup instructions, including which `SKILL.md` content to copy into the skill body.

## Guardrails

- Do not commit secrets, credentials, tokens, private customer data, regulated data, or proprietary content unless explicitly approved and safe.
- Do not invent product capabilities, APIs, package availability, repository contents, or runtime behavior.
- Do not assume Code Interpreter can access GitHub, internet, local repo files, or companion Markdown files unless the runtime explicitly supports it.
- Do not create helper files merely to make the package look complete. Create them only when they improve reliability or repeatability.
- Prefer small, auditable helper scripts over broad frameworks.
- Respect nebulaONE skill limits: description under 300 characters and body under 30,000 characters.
- Keep generated skill bodies task-appropriate and token-conscious.

## Quality Checklist

Before responding, confirm:

- Research was performed against Anthropic skills and other reputable sources, or the lack of research-tool access was stated.
- The skill description is under 300 characters.
- The skill body is under 30,000 characters.
- The body size is appropriate to the task and not bloated.
- All mandatory runtime behavior is in `SKILL.md`.
- Optional docs/helpers are useful and linked correctly.
- Helper code, if any, was validated or caveats were stated.
- `Skills/index.json` is valid JSON and includes fully qualified links.
- Secret scanning was performed when available for code/config-like files.
- GitHub commit/PR details are included if repository changes were made.
