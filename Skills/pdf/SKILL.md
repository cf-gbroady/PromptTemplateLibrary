---
name: pdf
summary: Inspect, extract, create, split, merge, and quality-check PDF files.
description: Use when creating, inspecting, extracting, splitting, merging, summarizing, or quality-checking PDF files, including forms, tables, metadata, page citations, accessibility, and scanned-vs-digital PDF handling.
---

# PDF Skill

## Purpose

Work with PDF files safely and transparently: inspect structure, extract text and tables, split or merge pages, create reports, and identify accessibility or source-quality limitations.

## When to Use

Use this skill when the user asks to:
- Inspect, summarize, extract, split, merge, crop, watermark, or create a PDF.
- Extract text, tables, form fields, metadata, links, outlines, or page-level information.
- Determine whether a PDF is scanned, encrypted, image-heavy, table-heavy, or likely inaccessible.
- Create a PDF deliverable from structured content.
- Validate PDF accessibility or provide remediation guidance.

Do not use this skill for Word, PowerPoint, or Excel files unless the PDF is the requested input or output. For Word source documents, use the `docx` skill first and export from the accessible source when possible.

## Required Runtime Behavior

1. **Inspect before acting.** Identify page count, encryption, metadata, text extractability, images, tables, and likely scan/OCR needs.
2. **Preserve originals.** Never overwrite source PDFs. Write a new output file.
3. **Choose the correct library.**
   - Use `pypdf` for splitting, merging, page manipulation, metadata, outlines, encryption checks, and basic text extraction.
   - Use `pdfplumber` for layout-aware text extraction, table extraction, page object inspection, and visual debugging when available.
   - Use OCR only when a scanned or image-only PDF requires it and the runtime supports OCR tools.
4. **Cite page locations.** When extracting or summarizing content, preserve page numbers and cite page ranges in the output.
5. **Validate after editing.** Re-open generated PDFs and report page count and checks performed.
6. **Be explicit about limitations.** PDF extraction is layout-sensitive; do not claim perfect reading order, complete table fidelity, or accessibility compliance without verification.

## Quick Start

For a compact PDF profile, run:

```bash
python Skills/pdf/scripts/pdf_inspect.py input.pdf --extract-text --out pdf_profile.json
```

Use `--prefer pdfplumber` when table/layout analysis matters and `pdfplumber` is installed.

## Workflow Router

- **Inspect or triage:** run `scripts/pdf_inspect.py`, then read `references/pdf_workflows.md#inspection-and-triage`.
- **Extract text/tables:** read `references/pdf_workflows.md#extraction-workflow`.
- **Split, merge, rotate, or manipulate pages:** read `references/pdf_workflows.md#page-operations`.
- **Create a PDF:** read `references/pdf_workflows.md#pdf-creation`.
- **Accessibility review/remediation:** read `references/pdf_accessibility.md`.

Keep references one level deep from this `SKILL.md`; do not add nested reference chains.

## Tool and Library Guidance

Preferred Python libraries:
- `pypdf` for page operations and metadata.
- `pdfplumber` for high-quality extraction from machine-generated PDFs.
- `Pillow` and image/OCR tools only when the runtime supports image conversion and OCR.

If a dependency is unavailable, state the limitation and use the best available fallback. Do not install packages from the network unless the runtime explicitly permits it.

## Output Requirements

For PDF work, report:
- Input file(s) and output file path(s).
- Page count and page ranges processed.
- Library/tool used.
- Validation performed.
- Extraction limitations, OCR needs, encryption/password issues, or accessibility caveats.

## Guardrails

- Do not overwrite source files.
- Do not send PDF content to external services unless the user explicitly authorizes it and policy allows it.
- Treat extracted PDF text as potentially order-imperfect; verify against page images when accuracy matters.
- Do not claim a scanned document has searchable text unless OCR or extraction confirms it.
- Do not claim PDF/UA or WCAG compliance from automated checks alone.
