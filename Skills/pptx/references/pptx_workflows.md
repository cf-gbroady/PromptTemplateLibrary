# PPTX Workflows

## Contents
- Creation workflow
- Editing workflow
- Extraction and summarization
- Data-driven presentations
- Tables, charts, and images
- Validation checklist
- Library limitations and fallbacks

## Creation Workflow

Use this workflow when creating a new `.pptx` file.

1. Identify the audience, purpose, slide count, tone, brand constraints, and required output filename.
2. Build an outline before creating slides.
3. Use a template if supplied; otherwise use built-in layouts and placeholders.
4. Keep each slide focused on one message.
5. Add speaker notes for narration, assumptions, and detailed explanations that should not crowd the slide.
6. Save to a new `.pptx` file and inspect it before returning it.

Recommended `python-pptx` pattern:

```python
from pptx import Presentation

prs = Presentation()
title_slide = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide)
slide.shapes.title.text = "Quarterly Business Review"
slide.placeholders[1].text = "Prepared for leadership"
prs.save("quarterly_business_review.pptx")
```

## Editing Workflow

Use this workflow when editing an existing deck.

1. Copy the input to a new output filename.
2. Inspect first:
   ```bash
   python scripts/pptx_inspect.py input.pptx --markdown
   ```
3. Confirm slide numbers and target content before editing.
4. Prefer placeholder updates over absolute-position shape insertion.
5. If changing layout, preserve titles, speaker notes, and meaningful visual descriptions.
6. Reopen or inspect the output file after saving.

## Extraction and Summarization

For extracting text, outline, slide titles, or notes:
- Use `scripts/pptx_inspect.py` for first-pass slide text and structural metadata.
- Use `python-pptx` when available for richer access to slides, shapes, notes, and document properties.
- For corpus indexing, include slide number, title, extracted text, notes presence, media count, and warnings.

## Data-Driven Presentations

For decks generated from spreadsheets, JSON, CSV, analytics outputs, or notebooks:

1. Validate input data before creating slides.
2. Decide the story before selecting charts.
3. Use one chart or table per slide unless the comparison requires multiple panels.
4. Include labels and notes explaining source, assumptions, and date ranges.
5. Avoid screenshot-only charts unless the underlying data or accessible explanation is also included.
6. If combining with spreadsheet analysis, use the XLSX skill for data preparation first.

## Tables, Charts, and Images

- Use tables only for compact data grids; prefer charts or bullets for narrative comparisons.
- Keep tables simple: header row, no merged/split cells, no nested tables.
- For charts, include title, labels, units, source, and a text takeaway.
- For images, preserve aspect ratio and add nearby explanatory text or alt text where supported.
- Use placeholders for pictures, charts, and tables when templates provide them.

## Validation Checklist

Before returning a deck:
- [ ] Output file opens or is structurally inspectable.
- [ ] Slide count and major sections match the request.
- [ ] Every slide has a meaningful title or title-like first text.
- [ ] Fonts are readable and slides are not crowded.
- [ ] Images, charts, and tables have explanations or need manual alt-text review.
- [ ] Data claims have source notes where relevant.
- [ ] Original input file was not overwritten.
- [ ] Any manual accessibility checks are reported.

## Library Limitations and Fallbacks

`python-pptx` is the default library for most creation/editing tasks when available. It can create, read, and update PowerPoint files and supports slides, placeholders, images, tables, charts, and core properties.

Some PowerPoint features may require manual review or Open XML-level work:
- Advanced animations and transitions.
- Complex SmartArt editing.
- Full fidelity reading-order remediation.
- Complete alt-text authoring support across all object types.
- Embedded media caption verification.
- Pixel-perfect rendering validation.

When a feature cannot be fully verified programmatically, state the limitation and provide a manual PowerPoint check.
