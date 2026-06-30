# PDF Accessibility and Quality Checklist

Use this checklist when reviewing or creating PDFs that will be shared, published, archived, or used by people relying on assistive technology.

## Source-First Rule

Fix accessibility in the source document whenever possible. DOCX, HTML, InDesign, or other structured sources usually produce better accessible PDFs than remediating a finished PDF.

## Core Checks

- PDF is tagged with meaningful structure.
- Heading levels are logical and do not skip levels without reason.
- Reading order matches the intended content order.
- Document language is specified.
- Title and metadata are appropriate.
- Bookmarks exist for longer documents when useful.
- Images have alt text or are marked decorative.
- Data tables identify header cells and scope.
- Links have descriptive text.
- Form fields have accessible names.
- Fonts and text extraction support reliable reading.

## Automated vs Manual Verification

Automated checks can identify common failures but cannot prove full accessibility. Manual checks are required for:
- reading order,
- heading meaning,
- image alt-text quality,
- table header correctness,
- form label usefulness,
- screen-reader navigation.

## Reporting Language

Use precise language:
- “Automated inspection found…”
- “Manual verification is still required for…”
- “This appears to be scanned and likely needs OCR…”
- “No tagged-structure verification was performed in this runtime.”

Do not say “PDF/UA compliant” or “WCAG compliant” unless the file has passed appropriate validation and manual review.
