---
name: xlsx
summary: Create, inspect, clean, edit, validate, and deliver spreadsheet files.
description: Use when the user's primary input or output is a spreadsheet file or spreadsheet-like tabular file, including .xlsx, .xlsm, .csv, or .tsv. Trigger for requests to open, read, analyze, clean, normalize, transform, create, edit, format, chart, repair, validate, or convert spreadsheet files.
---

# xlsx Skill

## Purpose

Use this skill to produce reliable, editable, and auditable spreadsheet deliverables. Apply it when a spreadsheet is the primary input, primary output, or required artifact.

## Runtime model

This skill is self-contained: its required operating instructions and minimal Python patterns are in this file. Do not depend on downloading, importing, or locating a companion `.py` file. A runtime may have no network access and may not mount repository files into Code Interpreter.

The companion reference at `Skills/xlsx/docs/code_snippets.md` is for repository readers and public browsing only. It is not a required runtime dependency.

## When to use

Use for `.xlsx`, `.xlsm`, `.csv`, and `.tsv` work such as inspection, cleaning, normalization, transformation, formatting, formula repair, validation, charting, or workbook creation.

## Do not use when

Use another workflow when the primary deliverable is a Word document, standalone web dashboard, database pipeline, Google Sheets API integration, or general analysis with no spreadsheet artifact.

## Required output standard

1. Deliver an actual spreadsheet when a file is requested.
2. Preserve existing worksheet names, styles, formulas, tables, charts, validations, named ranges, hidden sheets, and template conventions unless the requested change requires otherwise.
3. Save edits as a new version rather than overwriting the source file.
4. Keep raw data, assumptions, calculations, and final outputs separate when the workbook is complex enough to need them.
5. Use formulas for workbook calculations users would expect to update dynamically. Use Python for data preparation, workbook construction, and validation.
6. Document every introduced hardcoded value in a nearby source note, comment, or `Sources` worksheet so the workbook remains auditable.

## Tool selection

- Use `pandas` for ingestion, cleaning, reshaping, joining, deduplication, and aggregation.
- Use `openpyxl` for formulas, styles, comments, sheets, tables, validations, and edits to an existing `.xlsx` workbook.
- Use LibreOffice headless recalculation when it is available, then inspect cached results for formula errors.

Open editable workbooks with `data_only=False`. Do not save a workbook opened with `data_only=True`, because that mode reads cached values rather than preserving formula logic.

## Workflow

1. Inspect the input workbook before editing: sheet names, dimensions, formulas, tables, named ranges, validations, hidden sheets, and relevant existing conventions.
2. Confirm column mappings and test representative rows before applying formulas or transformations across a full range.
3. Make only changes directly requested or clearly necessary to deliver the requested result.
4. Use explicit source notes for hardcoded values. Preferred format: `Source: [system or document], [date], [specific reference], [URL or uploaded-file location]`.
5. Save to a new versioned output path.
6. For workbooks containing formulas, recalculate when possible and scan every worksheet for blocking Excel error values before delivery.
7. Report the output path, sheets changed, validation performed, and any limitation.

## Inline Python patterns

### Inspect a workbook safely

~~~python
from pathlib import Path
from openpyxl import load_workbook

input_path = Path("/mnt/data/input.xlsx")
wb = load_workbook(input_path, data_only=False, read_only=False)
for ws in wb.worksheets:
    print({"sheet": ws.title, "rows": ws.max_row, "columns": ws.max_column, "state": ws.sheet_state})
~~~

### Recalculate with LibreOffice when available

~~~python
from pathlib import Path
import shutil
import subprocess

workbook = Path("/mnt/data/output.xlsx")
soffice = shutil.which("soffice") or shutil.which("libreoffice")
if soffice:
    subprocess.run(
        [soffice, "--headless", "--convert-to", "xlsx", "--outdir", str(workbook.parent), str(workbook)],
        check=True,
        capture_output=True,
        text=True,
    )
else:
    print("LibreOffice is unavailable; set calculation mode to automatic and disclose that Excel should recalculate on open.")
~~~

If the conversion command cannot replace the desired workbook cleanly in the current environment, use a separate temporary output directory, then move the recalculated file into the intended versioned output path after confirming it exists.

### Scan cached values for blocking formula errors

~~~python
from openpyxl import load_workbook

ERRORS = {"#REF!", "#DIV/0!", "#VALUE!", "#N/A", "#NAME?", "#NUM!", "#NULL!"}

def find_formula_errors(path):
    wb = load_workbook(path, data_only=True, read_only=True)
    hits = []
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                if cell.value in ERRORS:
                    hits.append(f"{ws.title}!{cell.coordinate}: {cell.value}")
    return hits

errors = find_formula_errors("/mnt/data/output.xlsx")
if errors:
    raise ValueError("Blocking formula errors found:\n" + "\n".join(errors))
print("Validation passed: no blocking cached formula errors found.")
~~~

If recalculation is unavailable, scan formulas for obvious broken references, set calculation mode to automatic, and clearly tell the user that cached formula results may refresh when opened in Excel. Do not claim a full calculation validation in that case.

## Formula and formatting rules

- Use Excel formulas such as `=SUM(B2:B9)`, `=AVERAGE(D2:D19)`, and `=IFERROR(numerator/denominator,0)` rather than static Python-calculated values where a workbook needs dynamic behavior.
- Handle blanks, nulls, `NaN`, zero, negative, text, and large-value edge cases deliberately.
- Preserve the template's formatting conventions. If none exist for a financial or operating model, use blue font for user-changeable hardcodes, black for formulas, green for same-workbook links, red for external links, and yellow fill for assumptions needing attention.
- Preserve leading zero identifiers, account codes, ZIP codes, and course codes as text during CSV or TSV imports.
- Do not silently drop rows or columns; describe removals, exclusions, or transformations.

## Quality checklist

Before delivery, confirm that:

- The source file was preserved and the output path is versioned.
- Expected sheets and workbook structure are present.
- Formula ranges and cross-sheet references were checked beyond only the first few rows.
- Blocking formula errors are absent after recalculation, or the recalculation limitation is stated.
- Source documentation exists for introduced hardcodes.
- The workbook opens successfully and retains the requested edits.

## Failure handling and privacy

Ask a focused clarifying question when an ambiguous request could change formulas, source data, or the intended output layout. If a dependency is unavailable, use the best available fallback and name the limitation. For private, regulated, or sensitive data, use only data the user is authorized to provide and avoid external uploads or services unless explicitly approved.
