# Hardcoded Source Documentation Standard for xlsx Workbooks

## Purpose

This document defines how to document hardcoded values added to spreadsheet workbooks so outputs are auditable, maintainable, and safe for business use.

Use this standard whenever a workbook contains manually entered assumptions, copied values, scenario inputs, benchmark data, or values derived from a source outside the workbook.

## What Counts as a Hardcoded Value?

A hardcoded value is any value entered directly into a cell rather than calculated by an Excel formula or loaded transparently from a documented source table.

Examples:

- A growth rate typed into an assumptions cell
- A budget amount copied from a PDF, email, or user prompt
- A headcount assumption supplied by a stakeholder
- A benchmark percentage copied from a report
- A manually entered date or threshold
- A scenario input such as `Base`, `Upside`, or `Downside`

Hardcoded values are not automatically bad. They are often necessary. The risk is undocumented hardcoding.

## Required Source Note Format

Every material hardcoded value should have a source note in this format:

```text
Source: [System/Document], [Date], [Specific Reference], [URL or file path if applicable]
```

Examples:

```text
Source: User-provided assumption, 2026-06-24, Prompt states 8% annual growth
Source: FY26 Budget Workbook, 2026-06-24, Sheet: Assumptions, Cell: C12
Source: Finance Export, 2026-06-24, Sheet: Revenue by Month, uploaded workbook
Source: Board Deck, 2026-06-24, Slide 14, Revenue forecast table
Source: Unknown — user confirmation required
```

## Acceptable Documentation Methods

Use one or more of the following methods.

### 1. Adjacent Source Note Cell

Best for small models or visible assumption tables.

| Assumption | Value | Source |
|---|---:|---|
| Annual growth rate | 8.0% | Source: User-provided assumption, 2026-06-24, Prompt states 8% annual growth |

### 2. Cell Comment or Note

Best when the sheet is already tightly formatted and adding a source column would disrupt layout.

The comment should use the required source-note format.

### 3. Dedicated `Sources` Worksheet

Best for larger workbooks, recurring reporting, or executive/finance models.

Recommended columns:

| Field | Description |
|---|---|
| Source ID | Unique short ID such as `SRC-001` |
| Workbook Location | Sheet and cell/range where the value is used |
| Value / Assumption | Description of the hardcoded value |
| Source Type | User prompt, uploaded file, system export, external report, manual estimate |
| Source Name | Name of the file, system, or stakeholder |
| Source Date | Date the source was accessed or provided |
| Specific Reference | Sheet/cell, page, slide, section, email subject, or prompt excerpt |
| URL / Path | Link or file path when available |
| Notes | Any caveats or confidence notes |

### 4. Assumptions Table with Source Column

Best for financial models and operating plans.

| Assumption | Value | Unit | Source | Last Updated | Owner |
|---|---:|---|---|---|---|
| Annual growth | 8.0% | % | Source: User-provided assumption, 2026-06-24, Prompt states 8% annual growth | 2026-06-24 | User |

## Color and Formatting Guidance

For financial, budget, forecast, or operating model workbooks:

| Meaning | Recommended style |
|---|---|
| Hardcoded assumptions and user-changeable inputs | Blue font |
| Formulas and calculations | Black font |
| Same-workbook links to another worksheet | Green font |
| External workbook or external data links | Red font |
| Key assumptions requiring review | Yellow fill |

If the workbook already has a customer template or style guide, follow the existing template instead.

## Materiality Guidance

Document all hardcoded values that are material to the workbook's conclusions.

Always document:

- Assumptions used in formulas
- Inputs that drive dashboards, forecasts, budgets, or recommendations
- Values copied from external files
- Values provided verbally or in a prompt
- Benchmarks, rates, fees, percentages, and thresholds
- Values likely to be updated later

Optional to document:

- Decorative labels
- Static section headers
- Helper labels
- Non-material sample data clearly marked as sample/synthetic

## Unknown or Unverified Sources

If a source cannot be verified, do not hide that uncertainty.

Use:

```text
Source: Unknown — user confirmation required
```

or:

```text
Source: Unverified user-provided value, 2026-06-24, confirmation required before production use
```

## Recommended Workflow

1. Identify all direct cell values that materially affect outputs.
2. Determine whether each value is user-provided, copied from a file, imported from a system, or estimated.
3. Add a source note using the required format.
4. Use a `Sources` sheet for larger workbooks.
5. Add comments or adjacent source cells for small workbooks.
6. Review source notes before delivery.
7. If any source is unknown, flag it clearly for user confirmation.

## Delivery Checklist

Before delivering the workbook, confirm:

- Material hardcoded values are documented.
- User-changeable assumptions are visually distinct where appropriate.
- Unknown sources are marked as requiring confirmation.
- Source notes include a date.
- Source notes are specific enough for another person to trace the value.
- Source documentation does not expose sensitive data unnecessarily.

## Security and Privacy Note

Do not paste sensitive data into source notes unless it is necessary for auditability and appropriate under the user's data-governance policy. Prefer references such as file name, sheet name, section, or cell address over copying confidential source content into comments.
