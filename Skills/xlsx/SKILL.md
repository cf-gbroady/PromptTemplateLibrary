---
name: xlsx
summary: Create, inspect, clean, edit, validate, and deliver spreadsheet files.
description: Use this skill when the user's primary input or output is a spreadsheet file or spreadsheet-like tabular file, including .xlsx, .xlsm, .csv, or .tsv. Trigger for requests to open, read, analyze, clean, normalize, transform, create, edit, format, chart, repair, validate, or convert spreadsheet files. The final deliverable must be a spreadsheet file unless the user explicitly asks only for explanation or planning.
---

# xlsx Skill

## Runtime Companion Files

This skill is self-contained for nebulaONE trigger-loading. Admins may manually copy the full contents of this `SKILL.md` into a nebulaONE skill named `xlsx`.

Companion files are maintained in the PromptTemplateLibrary:

- Executable helper source (raw, preferred for Code Interpreter fetch): https://raw.githubusercontent.com/cf-gbroady/PromptTemplateLibrary/main/Skills/xlsx/scripts/xlsx_tools.py
- Executable helper source (GitHub view): https://github.com/cf-gbroady/PromptTemplateLibrary/tree/main/Skills/xlsx/scripts/xlsx_tools.py
- Hardcoded source documentation: https://github.com/cf-gbroady/PromptTemplateLibrary/tree/main/Skills/xlsx/docs/hardcoded_source_documentation.md
- Canonical skill source: https://github.com/cf-gbroady/PromptTemplateLibrary/tree/main/Skills/xlsx/SKILL.md

When Code Interpreter is used, do not assume this GitHub link automatically exists as a local file in the sandbox. If the sandbox has internet access and policy permits retrieving public GitHub raw files, download the helper from the raw URL above before importing it. If internet access is unavailable, either ask the user/admin to upload `xlsx_tools.py` into the chat or regenerate only the minimal helper logic required for the task.

Recommended Code Interpreter bootstrap when network access is available:

```python
from pathlib import Path
import urllib.request

helper_url = "https://raw.githubusercontent.com/cf-gbroady/PromptTemplateLibrary/main/Skills/xlsx/scripts/xlsx_tools.py"
helper_path = Path("/mnt/data/xlsx_tools.py")
urllib.request.urlretrieve(helper_url, helper_path)
```

## Purpose

Use this skill to produce reliable spreadsheet workbooks, especially Excel `.xlsx` files, that are useful, editable, auditable, and free of formula errors.

This skill applies when a spreadsheet file is the main input, main output, or required artifact.

## Do Not Use This Skill For

Do not trigger this skill when the primary deliverable is:

- A Word document
- A PDF report
- An HTML report or dashboard
- A standalone Python script with no spreadsheet deliverable
- A database pipeline
- A Google Sheets API integration
- A general data-analysis conversation where no spreadsheet file is requested or needed

If the user wants a narrative report plus a workbook, use this skill for the workbook portion.

## Required Output Standard

When delivering a spreadsheet:

1. Deliver an actual spreadsheet file when possible.
2. Use a clean, professional, consistent font and layout.
3. Preserve existing workbook styles, formulas, worksheet names, tables, charts, validations, named ranges, and template conventions unless the user asks to change them.
4. Existing workbook or customer template conventions override generic formatting preferences.
5. All formulas must recalculate successfully before delivery.
6. Deliver only when formula error count is zero, unless the user explicitly asks to inspect a broken workbook and the errors are the subject of the deliverable.
7. If hardcoded values are introduced, document the source of those values in nearby cells, comments, or a dedicated `Sources` worksheet.

## Tool Selection

Use the right tool for the job:

| Tool | Use for |
|---|---|
| `pandas` | Data cleaning, normalization, reshaping, aggregation, analysis, joining, deduplication, CSV/TSV loading, and bulk transforms |
| `openpyxl` | Excel formulas, formatting, existing workbook edits, comments, sheets, styles, tables, freeze panes, workbook structure, and formula inspection |
| LibreOffice / headless recalculation | Recalculating formulas and verifying workbook health before final delivery |

Important: do not save a workbook opened with `openpyxl.load_workbook(..., data_only=True)`. That can replace formulas with cached values and permanently lose formula logic. Use `data_only=False` when editing formulas or structure.

## Formula-First Rule

When a calculated result belongs in the workbook, use Excel formulas rather than hardcoded Python-calculated values.

Correct examples:

- Use `=SUM(B2:B9)`, not a Python-computed total.
- Use `=(C4-C2)/C2`, not a hardcoded growth rate.
- Use `=AVERAGE(D2:D19)`, not a Python-computed average.
- Use `=IFERROR(numerator/denominator,0)` or an equivalent guard when division by zero is plausible.

Python may be used to generate formulas, populate raw data, clean source tables, validate outputs, or build the workbook, but formulas should remain formulas where the user would reasonably expect the workbook to update dynamically.

## Formula Recalculation and Validation Workflow

For any workbook containing formulas:

1. Save the workbook.
2. Recalculate formulas with LibreOffice/headless spreadsheet recalculation when available.
3. Reopen the workbook and scan all worksheets for formula errors.
4. Fix any errors.
5. Recalculate again.
6. Deliver only after the scan finds zero blocking formula errors.

Blocking formula errors:

- `#REF!`
- `#DIV/0!`
- `#VALUE!`
- `#N/A`
- `#NAME?`
- `#NUM!`
- `#NULL!`

If the helper script is available, run one of the following patterns:

```bash
python /mnt/data/xlsx_tools.py recalc output.xlsx
python /mnt/data/xlsx_tools.py validate output.xlsx
python /mnt/data/xlsx_tools.py recalc-and-validate output.xlsx
```

If the helper script is not available, generate a minimal validation script in Code Interpreter using `openpyxl` and, when available, call LibreOffice directly.

## Verification Checklist

Before delivering a workbook:

- Confirm sheet names and expected workbook structure.
- Confirm column mappings before writing formulas broadly.
- Remember Excel rows and columns are 1-indexed.
- Test 2-3 sample formulas manually before filling large ranges.
- Check formulas in far-right columns and lower rows, not just top-left cells.
- Search for all relevant matches, not only the first match.
- Handle blank, null, `NaN`, zero, negative, text, and large-value edge cases.
- Prevent division by zero.
- Verify cross-sheet references.
- Verify formulas still point to intended sheets after renames or copies.
- Scan for formula errors after recalculation.
- Preserve user-entered values unless the task requires changing them.
- Keep raw data separate from calculations and outputs when possible.

## Hardcoded Value Documentation

When adding hardcoded values, document the source in one of these ways:

1. Adjacent source note cell
2. Cell comment/note
3. Dedicated `Sources` worksheet
4. Dedicated source table near the relevant assumptions

Preferred format:

```text
Source: [System/Document], [Date], [Specific Reference], [URL or file path if applicable]
```

Examples:

```text
Source: Finance Export, 2026-06-24, Revenue by Month tab, uploaded workbook
Source: User-provided assumption, 2026-06-24, Growth rate supplied in prompt
Source: FY26 Budget Workbook, 2026-06-24, Sheet: Assumptions, Cell: C12
Source: Unknown — user confirmation required
```

If the hardcoded source documentation companion file is available, follow it for expanded standards. If it is not available, the rules in this section are authoritative.

## Financial and Operating Model Conventions

Use these conventions for financial, budget, forecast, operating model, or executive analytics workbooks unless the user's template says otherwise.

### Cell Color Conventions

| Meaning | Style |
|---|---|
| Hardcoded inputs and user-changeable assumptions | Blue font |
| Formulas and calculations | Black font |
| Same-workbook links to other worksheets | Green font |
| External workbook or external data links | Red font |
| Key assumptions requiring attention or review | Yellow fill |

### Number Formats

| Value type | Format |
|---|---|
| Years | Text strings such as `"2024"`, not numeric values intended for calculation |
| Currency | Units in headers, e.g. `Revenue ($mm)` |
| Zero values | Display as `-` where appropriate |
| Percentages | `0.0%` |
| Multiples | `0.0x` |
| Negative values | Parentheses, e.g. `(1.2)` |

## Workbook Design Patterns

Prefer a clear workbook structure:

1. `README` or `Instructions` sheet when the workbook is complex.
2. `Sources` sheet for hardcoded source documentation.
3. `Raw Data` or source-specific raw data sheets.
4. `Assumptions` sheet for user-changeable inputs.
5. `Calculations` sheet for intermediate logic.
6. `Summary` or `Dashboard` sheet for final outputs.

Do not overcomplicate small workbooks. Use only the sheets needed for the task.

## Editing Existing Workbooks

When editing an existing workbook:

1. Inspect workbook structure first.
2. Preserve hidden sheets unless there is a clear reason to change them.
3. Preserve formulas unless changing them is required.
4. Preserve workbook formatting and conventions.
5. Avoid deleting sheets, named ranges, tables, charts, validations, or comments unless explicitly requested.
6. If a workbook appears to be a template, follow the template style instead of applying generic formatting.
7. Save as a new version rather than overwriting the original when the environment supports file versioning.

## CSV and TSV Handling

When the input is CSV or TSV:

1. Detect delimiter and encoding where possible.
2. Preserve leading zeros in IDs, ZIP codes, account codes, and course codes by treating them as text.
3. Normalize dates cautiously and document any assumptions.
4. When delivering Excel, keep imported raw data separate from cleaned or calculated outputs.
5. Do not silently drop rows or columns. Document removals or transformations.

## Failure Handling

If formula recalculation is not possible because LibreOffice is unavailable, set workbook calculation mode to automatic, scan formulas for obvious reference problems, and state the limitation. If formulas may be stale, tell the user that Excel should recalculate on open.

If a user asks for a workbook using regulated, private, or sensitive data, default to synthetic or de-identified examples unless the user confirms their governance configuration permits the use of real data.
