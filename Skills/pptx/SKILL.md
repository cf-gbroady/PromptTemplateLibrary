---
name: pptx
summary: PowerPoint PPTX creation, editing, inspection, and accessibility workflows.
description: Use when creating, editing, inspecting, extracting, or quality-checking Microsoft PowerPoint .pptx presentations, including slides, layouts, charts, images, metadata, and accessibility.
---

# PPTX

## Purpose

Use this skill for Microsoft PowerPoint `.pptx` work: creating presentations, editing existing decks, extracting slide content, inspecting structure, adding images/charts/tables, preparing data-driven decks, and checking presentation quality or accessibility.

## When to Use

Use this skill when the user asks to:
- Create or modify a `.pptx` deck.
- Generate presentation slides from data, notes, outlines, documents, or reports.
- Inspect slides, layouts, placeholders, images, notes, metadata, or embedded media.
- Add or update tables, charts, screenshots, logos, speaker notes, or slide titles.
- Check PowerPoint accessibility, including reading order, alt text, titles, contrast, tables, and media captions.
- Convert presentation content into an outline, summary, or another document format.

## Do Not Use When

Do not use this skill for:
- Spreadsheet-only work; use the XLSX skill.
- Word document work; use the DOCX skill.
- PDF extraction or PDF assembly; use the PDF skill.
- Image generation alone unless the image is being placed into a presentation.
- Requests that only ask for presentation advice and do not require file creation, editing, inspection, or quality checks.

## Core Workflow

1. Clarify the task type: create, edit, inspect, extract, summarize, validate, or convert.
2. Preserve originals. If editing an existing file, write a new output file instead of overwriting the input.
3. Inspect existing decks before editing:
   ```bash
   python scripts/pptx_inspect.py input.pptx --json
   ```
4. Choose the right workflow:
   - Creation/editing: read `references/pptx_workflows.md`.
   - Accessibility/quality review: read `references/pptx_accessibility.md`.
5. Prefer template/layout placeholders over manually positioned text boxes when building slides.
6. Validate the output by reopening or inspecting the generated `.pptx`.
7. Report the output filename, what changed, and any limitations or manual checks needed.

## Tool and Library Guidance

- Prefer `python-pptx` for creating, reading, and updating `.pptx` files when it is available.
- Use the bundled `scripts/pptx_inspect.py` for read-only structural inspection without external dependencies.
- If `python-pptx` is unavailable and package installation is not allowed, use standard-library ZIP/XML inspection for extraction and analysis; explain any creation/editing limitation.
- Do not assume PowerPoint is installed. Workflows should run in a headless Python environment when possible.

## Quality Requirements

For generated or edited decks:
- Every slide should have a unique, meaningful title, visible or accessibility-preserving hidden.
- Use built-in layouts and placeholders when possible.
- Keep slides concise; avoid crowding and tiny fonts.
- Add alt text or surrounding explanatory text for meaningful visuals.
- Mark purely decorative visuals as decorative when the authoring environment supports it.
- Use readable fonts, sufficient contrast, and descriptive hyperlink text.
- Use simple tables with headers; avoid tables for layout.
- For media, include captions/transcripts or state that they require manual verification.
- Include speaker notes when the user needs presenter guidance or visual descriptions.

## Output Requirements

When creating or editing files:
- Save the output as a new `.pptx` file.
- Summarize slide count, major sections, and notable design/accessibility choices.
- List any manual checks that cannot be fully verified programmatically, especially reading order, contrast, alt-text quality, animations, and media captions.
