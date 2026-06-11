---
name: accessibility
description: Ensures responses and generated artifacts meet WCAG 2.1 AA. Trigger for any user-facing output — Markdown answers, documents (docx/pdf/pptx), spreadsheets, charts, images, and HTML. Covers heading structure, alt text, color contrast, readable tables, link text, plain language, and accessible math.
license: Proprietary.
---

# Accessibility (WCAG 2.1 AA)

nebulaONE serves higher education and healthcare, where accessibility is often a legal requirement (Section 508, ADA, EN 301 549). Build every output to **WCAG 2.1 AA** by default. Model-agnostic.

## Quick checklist
- **Headings** are hierarchical and never skipped (H1 → H2 → H3). One H1/title per document.
- **Alt text** on every meaningful image/chart; mark purely decorative images as decorative.
- **Contrast** ≥ 4.5:1 for normal text, ≥ 3:1 for large text (≥18pt/14pt bold) and UI/graphic elements.
- **Color is never the only signal** — pair it with text, icons, or patterns.
- **Tables** have header rows/columns; no merged cells used purely for layout; no empty header cells.
- **Link text** is descriptive ("Refund policy (PDF)"), never "click here" or a bare URL.
- **Lists** use real list markup, not manual dashes in a paragraph.
- **Language** is plain; expand acronyms on first use; define jargon.
- **Math** uses KaTeX/LaTeX (screen-reader friendly) — not images of equations.

## Color contrast with the brand palette
Bright cyan `#00d4ff` fails AA as text on white. Use it for fills/rules only.

| Foreground | On white | Use for |
|---|---|---|
| `#0f2557` Deep Navy | ✅ ~13:1 | Body text, headings |
| `#1a3a6b` Navy Blue | ✅ ~9:1 | Headings, links |
| `#0099cc` Deep Cyan | ✅ ~3.4:1 | Large text / links only |
| `#00d4ff` Bright Cyan | ❌ | Fills, borders, accents — not text |

Always verify computed contrast for the actual pair you ship.

## Alt text that works
- Describe **function and content**, not appearance: "Bar chart: Q4 sales up 25% over Q3" beats "a blue bar chart."
- Keep it concise (~1 sentence). For complex charts, add a short data summary or a data table nearby.
- Decorative only → empty alt (`alt=""`) so screen readers skip it.

## Documents & decks
- Set document **title** metadata and use built-in **heading styles** (the docx/pdf/pptx skills do this).
- Provide a **table of contents** for long documents.
- Ensure reading order is logical; don't rely on absolute positioning to convey order.
- Captions for figures and tables.

## Data visualizations
- Don't encode meaning in hue alone — add labels, direct annotations, or patterns (see [skills-data.md](skills-data.md), which ships a colorblind-safe palette).
- Label axes with units; give every chart a descriptive title.

## Plain-language defaults
- Short sentences; active voice; one idea per sentence.
- Define the first use of any acronym: "FERPA (Family Educational Rights and Privacy Act)."
- Prefer concrete steps and examples over abstractions.

> ℹ️ This skill complements every output skill. When generating a document, deck, or chart, run this checklist before delivering.
