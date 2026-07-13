# PPTX Accessibility and Quality

## Contents
- Accessibility-first defaults
- Slide titles
- Reading order
- Alt text and decorative visuals
- Color, fonts, spacing, and layout
- Tables and charts
- Hyperlinks and media
- Manual review checklist

## Accessibility-First Defaults

Accessible PowerPoint work starts with structure:
- Use built-in slide layouts and placeholders instead of blank slides filled with manual text boxes.
- Give each slide a unique, descriptive title.
- Keep slide content concise and use speaker notes for detail.
- Avoid using color alone to convey meaning.
- Prefer accessible templates when the user provides or requests a reusable deck style.

## Slide Titles

Every slide should have a meaningful title. If the visual design does not allow a visible title, keep an accessibility-preserving hidden title where possible and note that manual verification is required in PowerPoint.

Poor titles:
- `Slide 1`
- `Overview`
- Duplicate titles repeated across many slides

Better titles:
- `Enrollment increased 12% year over year`
- `Three risks affect the Q4 launch`
- `Budget variance is concentrated in travel`

## Reading Order

Screen readers read objects based on the deck's object/reading order, not necessarily the visual top-to-bottom layout. For complex slides:
- Use built-in layouts where possible.
- Group logical units when that improves comprehension.
- Avoid scattering related text and visuals across unrelated shapes.
- Inspect manually in PowerPoint's Reading Order pane or Selection Pane when final accessibility is required.
- Remember that some panes display reading order top-to-bottom and others bottom-to-top; verify with the tool being used.

Programmatic inspection can flag crowded slides and missing title-like text, but it cannot guarantee final screen-reader reading order.

## Alt Text and Decorative Visuals

For meaningful visuals:
- Provide concise alt text or an equivalent explanation on the slide.
- Describe the insight, not only the visual type.
- For charts, include the takeaway, axes/units, and important values.
- Do not start alt text with phrases like “image of” or “picture of.”

For decorative visuals:
- Mark as decorative when authoring tools support it.
- If that cannot be set programmatically, report it as a manual check.

## Color, Fonts, Spacing, and Layout

- Use readable sans-serif fonts.
- Use larger text for body copy; avoid dense paragraphs.
- Keep enough white space for projection and screen sharing.
- Maintain strong contrast between text and background.
- Do not use color as the only indicator; add text labels, symbols, patterns, or direct annotations.

## Tables and Charts

Tables:
- Use only for data, not layout.
- Include header rows.
- Avoid merged cells, split cells, nested tables, and blank cells that hide meaning.

Charts:
- Include descriptive titles, labels, units, legends, and data source notes.
- Add a plain-language takeaway on or near the slide.
- Ensure the color palette remains understandable without color perception.

## Hyperlinks and Media

- Use descriptive hyperlink text; avoid “click here,” “more,” and bare URLs unless the URL itself is the content.
- Videos need captions/subtitles and, where needed, audio description or transcript.
- Audio needs a transcript or equivalent text summary.
- Media captions and playback behavior usually require manual verification.

## Manual Review Checklist

Use this checklist before final delivery when accessibility matters:
- [ ] PowerPoint Accessibility Checker reviewed.
- [ ] Every slide has a unique title.
- [ ] Reading order verified for complex slides.
- [ ] Meaningful visuals have alt text or equivalent visible explanation.
- [ ] Decorative visuals are marked decorative where supported.
- [ ] Contrast is sufficient, especially on gradients or image backgrounds.
- [ ] Text is readable at expected presentation size.
- [ ] Tables are simple and have headers.
- [ ] Hyperlinks use descriptive text.
- [ ] Media has captions/transcripts or a documented remediation need.
- [ ] Deck tested with keyboard navigation or a screen reader when required.
