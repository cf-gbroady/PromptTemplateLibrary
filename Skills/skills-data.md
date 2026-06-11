---
name: data-visualization
description: >
  Generates, customizes, and recommends data visualizations from user-uploaded documents. Trigger when a user uploads a spreadsheet, CSV, PDF, or dataset and asks for charts, graphs, dashboards, trends, comparisons, or summary insights — or when tabular/time-series data would clearly benefit from visual exploration. Default palette is the nebulaONE brand (navy/cyan/indigo); users can request other schemes.
license: See LICENSE.txt
---

# Data Visualization Skill

This skill guides the creation and recommendation of data visualizations when users upload documents containing structured or semi-structured data. It is model-agnostic and runs in the nebulaONE Python code interpreter.

> 🔒 **Privacy first (ed/healthcare default):** Before charting, scan for PII/PHI (names, MRNs, student IDs, emails, DOBs). Do not render identifiable individuals in a public-looking chart — aggregate, bin, or pseudonymize first, and never label more than is needed. If the data appears regulated (FERPA/HIPAA), keep all processing in-session and flag it to the user. See [skills-compliance-privacy.md](skills-compliance-privacy.md).

## nebulaONE Brand Palette (default)

Use these brand colors by default instead of a generic purple/blue ramp:

```python
# nebulaONE sequential/categorical palette (navy → cyan → indigo)
NEBULA_PALETTE = ['#0f2557', '#1a3a6b', '#0099cc', '#00d4ff', '#9381ff', '#beb6cf']
# Single-hue sequential ramp (light → dark) for heatmaps/choropleths
NEBULA_SEQUENTIAL = ['#bef0ff', '#7fd9f2', '#00d4ff', '#0099cc', '#1a3a6b', '#0f2557']
```

If a user requests another scheme, honor it. Otherwise apply `NEBULA_PALETTE`.

## When to Use This Skill

- When a user uploads a file (spreadsheet, CSV, PDF, DOCX, etc.) and:
  - Requests charts, graphs, or dashboards.
  - Mentions analysis, trends, comparisons, or summary insights.
  - The content contains tables, metrics, or time series data that would benefit from visual exploration.
- When data patterns, outliers, or relationships may be better understood visually.
- When the user is unsure what visualizations are possible, suggest the most relevant and insightful options.

## Default Visualization Guidance

- **Chart Types:** Recommend visualizations based on data context:
  - **Time series:** Line or area charts
  - **Category comparisons:** Bar or column charts
  - **Distributions:** Histograms, boxplots, violin plots
  - **Part-to-whole:** Pie, donut, or stacked bar charts
  - **Relationships:** Scatterplots, heatmaps
  - **Hierarchies:** Treemaps, sunbursts
- **Complexity:** When multiple dimensions or metrics are present, suggest grouped, stacked, or multi-panel charts for richer insights.
- **Download:** Whenever a data visualization is created, always be sure to a downloadable png of the same image and present it below the image of the data viz.  


## Workflow for Visualization

1. **Detect Data Structure**
   - Parse uploaded file(s) to identify tables, columns, and key variables.
   - Extract relevant data points and summarize available fields.

2. **Perform Pre Visualizations**
   - Suggest 3–8 chart types tailored to the data (see above).
   - Briefly explain why each chart is useful for the user's goals.
   - Always apply the nebulaONE brand palette (`NEBULA_PALETTE`) unless the user requests otherwise.

3. **Generate Visualizations**
   - Use Matplotlib/pyplot as the primary choice, with Seaborn as the secondary option (default: nebulaONE navy/cyan/indigo brand palette).
   - Annotate key values, trends, or outliers where appropriate.
   - Render charts in the chat when possible; offer downloadable pngs with each output by default.


4. **Customization**
   - Allow users to request alternative color schemes, chart types, or highlight specific data points.
   - Support both concise dashboard-style summaries and detailed, publication-quality charts.

5. **Documentation and Export**
   - Provide code snippets for reproducibility (Python/Matplotlib/Seaborn/Plotly).
   - Enable export to PNG, SVG, or interactive HTML.

## Accessibility and Standards

### 1. **Color Accessibility:**
   # Use colorblind-friendly palettes
   cb_palette = ['#0173B2', '#DE8F05', '#029E73', '#CC78BC', 
                 '#CA9161', '#FBAFE4', '#949494', '#ECE133', '#56B4E9']
   
   # Ensure sufficient contrast ratios (WCAG AA: 4.5:1)
   # Add patterns for critical distinctions

### 2. **Alternative Representations:**
   - Generate descriptive alt text programmatically
   - Provide data tables for screen readers
   - Include sonification options for trends
   - Support keyboard navigation for interactive plots

### 3. **Annotation Standards:**
   - Use clear, descriptive titles
   - Include units in axis labels
   - Provide context in subtitles
   - Add data source citations
   - Include confidence intervals where appropriate

## Example Usage

- **User uploads an Excel file with sales data.**
  - Automatically extract key metrics (e.g., sales by region, time, product).
  - Suggest and generate bar charts, line charts, and heatmaps using the nebulaONE brand palette.
  - Display charts in chat and offer code/downloads.

- **User uploads a PDF with financial tables.**
  - Parse tables, summarize trends (e.g., revenue, expenses, profit).
  - Recommend grouped bar charts and line charts for year-over-year comparison.
  - Use default color palette unless user specifies otherwise.

## Best Practices

- Keep visualizations clear, interpretable, and visually consistent.
- Use annotations, titles, and axis labels for context.
- When in doubt, start with summary charts and invite the user to request deeper or alternative views.
- Never put more than ~10 category labels on a single axis or legend; group the long tail into an "Other" bucket for readability.

---