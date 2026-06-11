---
name: skills-library-readme
description: Index and authoring standard for the nebulaONE Skills library. Read this first when adding, editing, or reviewing a skill. Defines the Agent Skills frontmatter contract, the nebulaONE brand palette, and platform conventions every skill must follow.
---

# nebulaONE Skills Library

This folder contains **Agent Skills** for the [nebulaONE](https://nebulaone.ai/) platform — Cloudforce's multi-model, Azure-based enterprise GenAI gateway. A skill is a self-contained Markdown file that an agent loads on demand when its `description` matches the user's request. Skills extend any model the platform runs (OpenAI, Anthropic, Meta, Mistral, and others), so **skills must stay model-agnostic** — never assume a specific model is executing.

## Platform context every skill should assume

nebulaONE agents typically have access to:

- **Knowledge sources / RAG** over the customer's own proprietary data (private to their Azure tenant).
- **Web/internet search** for current information.
- **Image generation** (multimodal output).
- A **Python code interpreter** (the document/data skills rely on this).
- **MCP integrations** (e.g., Microsoft Learn for authoritative Azure docs).
- **SSO + role-based access control**, with a **compliance posture** spanning HIPAA, FERPA, SOC 2, and GDPR.

Primary verticals are **higher education and healthcare**, so privacy (PII/PHI), accessibility (WCAG 2.1 AA), and source-grounded answers are first-class concerns, not afterthoughts.

## Authoring contract (every skill file)

1. **YAML frontmatter is required** and must use exactly these keys:
   ```yaml
   ---
   name: kebab-case-skill-name
   description: One or two sentences, third person, that say WHAT the skill does and WHEN to trigger it. Pack it with the words a user would actually use, because this text is the only thing the agent sees when deciding to load the skill.
   ---
   ```
   - `name` is lowercase, hyphenated, and unique within the folder.
   - `description` is the single most important line in the file. Lead with the trigger ("When a user uploads a spreadsheet and asks for charts…"), not with marketing.
   - Do **not** name a specific model ("When Claude needs to…", "GPT Agent"). Use "the agent" or "the assistant".

2. **Body** holds the procedure: when to use, step-by-step workflow, code/templates, and guardrails. Keep code runnable and imports correct.

3. **Stay platform-agnostic in tone** but **nebulaONE-specific in defaults** (brand palette, compliance notes, citation discipline).

## Canonical nebulaONE brand palette

Use this everywhere a skill produces branded output (documents, decks, charts, HTML). It is derived from the nebulaONE product UI.

| Role | Name | Hex | RGB |
|------|------|-----|-----|
| Primary | Deep Navy | `#0f2557` | 15, 37, 87 |
| Secondary | Navy Blue | `#1a3a6b` | 26, 58, 107 |
| Accent (text-safe) | Deep Cyan | `#0099cc` | 0, 153, 204 |
| Accent (bright) | Cyan | `#00d4ff` | 0, 212, 255 |
| Supporting | Indigo | `#9381ff` | 147, 129, 255 |
| Muted | Violet | `#beb6cf` | 190, 182, 207 |
| Subtle fill | Light Cyan | `#bef0ff` | 190, 240, 255 |
| Alert | Magenta | `#b62850` | 182, 40, 80 |
| Body text | Dark Gray | `#333333` | 51, 51, 51 |
| Caption / muted | Light Gray | `#666666` | 102, 102, 102 |

> ⚠️ **Contrast rule:** bright cyan `#00d4ff` is low-contrast on white. Use it for fills, rules, borders, and accents — never for small body text. For text on white, use `#0f2557` or `#0099cc`. Always verify WCAG AA (4.5:1) for text.

**Typography:** `Segoe UI` is the nebulaONE/Microsoft brand font — use it for HTML and PowerPoint. For `.docx` use Calibri / Calibri Light (Office-native and always available). For ReportLab PDFs use Helvetica (a built-in font that needs no embedding).

## Skill index

| Skill | File | Triggers on |
|-------|------|-------------|
| Library standard (this file) | `README.md` | Authoring or reviewing skills |
| General output & formatting | `skills-general.md` | Tables, callouts, math, collapsibles, pills, quizzes |
| Data visualization | `skills-data.md` | Uploaded data → charts, dashboards, trends |
| Word documents | `skills-docx-v2.md` | Create/analyze `.docx` |
| PDF documents | `skills-pdf-v2.md` | Create/analyze/merge `.pdf` |
| PowerPoint | `skills-pptx.md` | Build/edit `.pptx` decks |
| Spreadsheets | `skills-xlsx.md` | Create/analyze `.xlsx`, models, formulas |
| Feedback bar | `skills-feedback-form.md` | Append feedback widget to responses |
| Citations & RAG grounding | `skills-citations-grounding.md` | Answering from knowledge sources; citing sources |
| Accessibility (WCAG 2.1 AA) | `skills-accessibility.md` | Any user-facing document/output |
| Image generation | `skills-image-generation.md` | "Make an image / illustration / diagram" |
| Privacy & compliance | `skills-compliance-privacy.md` | PII/PHI, FERPA/HIPAA-sensitive content |
| Communications & writing | `skills-communications.md` | Emails, announcements, memos, summaries |
| Web research | `skills-web-research.md` | Current events, "look up / latest / cite sources" |

## Maintenance

- One concern per skill. If a skill grows two unrelated triggers, split it.
- When you add a skill, add a row to the index above.
- Test any code block before committing — the document skills run in the live code interpreter.
