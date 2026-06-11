---
name: pptx
description: Build and edit PowerPoint presentations programmatically — title/agenda/content/table/chart/image slides, speaker notes, templates, and brand styling. Trigger when a user asks to create, generate, build, design, or update a .pptx / slide deck / presentation.
license: Proprietary. LICENSE.txt has complete terms
---

# Creating PowerPoint Presentations with the Code Interpreter

## Overview
This guide covers creating PowerPoint presentations programmatically in the nebulaONE Python code interpreter. It is model-agnostic. **Plan the deck before generating it** — outline the slides, then build. All decks default to the **nebulaONE brand palette** and **Segoe UI** (see [README.md](README.md)).

## Prerequisites
- Required libraries: `python-pptx`, `Pillow`, `matplotlib`, `seaborn`

## nebulaONE Brand Constants
Reuse these in every deck so output matches the platform look:

```python
from pptx.dml.color import RGBColor
from pptx.util import Pt

NEBULA = {
    'primary':   RGBColor(0x0F, 0x25, 0x57),  # Deep Navy  #0f2557
    'secondary': RGBColor(0x1A, 0x3A, 0x6B),  # Navy Blue  #1a3a6b
    'accent':    RGBColor(0x00, 0x99, 0xCC),  # Deep Cyan  #0099cc (text-safe)
    'bright':    RGBColor(0x00, 0xD4, 0xFF),  # Bright Cyan #00d4ff (fills/accents only)
    'support':   RGBColor(0x93, 0x81, 0xFF),  # Indigo     #9381ff
    'fill':      RGBColor(0xBE, 0xF0, 0xFF),  # Light Cyan #bef0ff (subtle fills)
    'text':      RGBColor(0x33, 0x33, 0x33),  # Dark Gray  #333333
    'muted':     RGBColor(0x66, 0x66, 0x66),  # Light Gray #666666
    'white':     RGBColor(0xFF, 0xFF, 0xFF),
}
BRAND_FONT = 'Segoe UI'
```

## Basic PowerPoint Creation

### 1. Creating a Blank Presentation
```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# Create a new presentation
prs = Presentation()

# Set slide size (16:9 widescreen)
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Add a title slide
title_slide_layout = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide_layout)

# Add title and subtitle
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = "Your Presentation Title"
subtitle.text = "Created with nebulaONE"

# Save the presentation
prs.save('my_presentation.pptx')
```

### 2. Understanding Slide Layouts
PowerPoint templates come with predefined layouts. Common layouts include:
- Layout 0: Title Slide
- Layout 1: Title and Content
- Layout 2: Section Header
- Layout 3: Two Content
- Layout 4: Comparison
- Layout 5: Title Only
- Layout 6: Blank
- Layout 7: Content with Caption
- Layout 8: Picture with Caption

### 3. Analyzing Template Layouts
```python
def analyze_template(template_path):
    """Analyze a PowerPoint template to understand its layouts"""
    prs = Presentation(template_path)

    for idx, layout in enumerate(prs.slide_layouts):
        print(f"Layout {idx}: {layout.name}")
        for placeholder in layout.placeholders:
            print(f"  - Placeholder {placeholder.placeholder_format.idx}: {placeholder.name}")
```

## Designing Slide Content

### 1. Adding Text with Formatting
```python
def add_formatted_text_slide(prs, title_text, content_items):
    """Add a slide with formatted text content"""
    slide_layout = prs.slide_layouts[1]  # Title and Content layout
    slide = prs.slides.add_slide(slide_layout)

    # Set title
    title = slide.shapes.title
    title.text = title_text
    title.text_frame.paragraphs[0].font.name = BRAND_FONT
    title.text_frame.paragraphs[0].font.color.rgb = NEBULA['primary']

    # Add content
    content = slide.placeholders[1]
    text_frame = content.text_frame
    text_frame.clear()  # Clear existing content

    for i, item in enumerate(content_items):
        p = text_frame.paragraphs[0] if i == 0 else text_frame.add_paragraph()
        p.text = item['text']
        p.level = item.get('level', 0)

        # Apply formatting
        font = p.font
        font.name = item.get('font', BRAND_FONT)
        font.size = Pt(item.get('size', 18))
        font.bold = item.get('bold', False)
        font.italic = item.get('italic', False)
        font.color.rgb = item.get('color', NEBULA['text'])
```

### 2. Creating Tables
```python
def add_table_slide(prs, title_text, data, headers):
    """Add a slide with a brand-styled table"""
    slide_layout = prs.slide_layouts[5]  # Title Only layout
    slide = prs.slides.add_slide(slide_layout)

    # Set title
    title = slide.shapes.title
    title.text = title_text

    # Define table dimensions
    rows = len(data) + 1  # +1 for header
    cols = len(headers)
    left, top = Inches(1), Inches(2)
    width, height = Inches(8), Inches(0.8 * rows)

    # Add table
    table = slide.shapes.add_table(rows, cols, left, top, width, height).table

    # Set column widths
    for i in range(cols):
        table.columns[i].width = Inches(width.inches / cols)

    # Add headers (brand navy with white text)
    for i, header in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = header
        cell.fill.solid()
        cell.fill.fore_color.rgb = NEBULA['primary']

        paragraph = cell.text_frame.paragraphs[0]
        paragraph.font.name = BRAND_FONT
        paragraph.font.bold = True
        paragraph.font.color.rgb = NEBULA['white']
        paragraph.alignment = PP_ALIGN.CENTER

    # Add data with alternating light-cyan rows
    for row_idx, row_data in enumerate(data):
        for col_idx, value in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = str(value)
            cell.text_frame.paragraphs[0].font.name = BRAND_FONT
            if row_idx % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = NEBULA['fill']
```

### 3. Adding Shapes and Graphics
```python
from pptx.enum.shapes import MSO_SHAPE

def add_shapes_slide(prs, title_text):
    """Add a slide with brand-colored shapes"""
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title Only
    slide.shapes.title.text = title_text

    left, top = Inches(1), Inches(2)
    width, height = Inches(2), Inches(1)

    # Rounded rectangle (primary)
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid(); shape.fill.fore_color.rgb = NEBULA['primary']

    # Oval (accent)
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(4), top, Inches(1.5), Inches(1.5))
    shape.fill.solid(); shape.fill.fore_color.rgb = NEBULA['accent']

    # Arrow (indigo)
    shape = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(7), top, width, height)
    shape.fill.solid(); shape.fill.fore_color.rgb = NEBULA['support']
```

## Image Generation and Integration

### 1. Generating Charts with Matplotlib (brand palette)
```python
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

NEBULA_HEX = ['#0f2557', '#1a3a6b', '#0099cc', '#00d4ff', '#9381ff']

def generate_chart_image():
    """Generate a brand-colored chart and return it as image bytes"""
    fig, ax = plt.subplots(figsize=(8, 6))

    categories = ['Q1', 'Q2', 'Q3', 'Q4']
    values1 = [20, 35, 30, 35]
    values2 = [25, 30, 35, 30]

    x = np.arange(len(categories))
    width = 0.35
    bars1 = ax.bar(x - width/2, values1, width, label='Product A', color=NEBULA_HEX[0])
    bars2 = ax.bar(x + width/2, values2, width, label='Product B', color=NEBULA_HEX[2])

    ax.set_xlabel('Quarter')
    ax.set_ylabel('Sales (in millions)')
    ax.set_title('Quarterly Sales Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()

    for bars in (bars1, bars2):
        for bar in bars:
            h = bar.get_height()
            ax.annotate(f'{h}', xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom')

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    img_buffer.seek(0)
    plt.close()
    return img_buffer
```

### 2. Adding Images to Slides
```python
def add_image_slide(prs, title_text, image_path=None, image_bytes=None):
    """Add a slide with an image, scaled to fit and centered"""
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title Only
    slide.shapes.title.text = title_text

    left, top = Inches(1), Inches(2)
    source = image_path if image_path else image_bytes
    pic = slide.shapes.add_picture(source, left, top)

    # Scale to fit while preserving aspect ratio
    max_width, max_height = Inches(8), Inches(5)
    scale = min(max_width / pic.width, max_height / pic.height)
    pic.width = int(pic.width * scale)
    pic.height = int(pic.height * scale)

    # Center horizontally
    pic.left = int((prs.slide_width - pic.width) / 2)
    return slide
```

## Working with Templates

### 1. Reusable Brand Template Class
```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

class PresentationTemplate:
    """Manage a brand-consistent presentation"""

    def __init__(self, template_path=None):
        self.prs = Presentation(template_path) if template_path else Presentation()
        self.prs.slide_width = Inches(13.333)
        self.prs.slide_height = Inches(7.5)
        self.colors = NEBULA
        self.fonts = {
            'title':    {'name': BRAND_FONT, 'size': 40, 'bold': True},
            'subtitle': {'name': BRAND_FONT, 'size': 22, 'bold': False},
            'body':     {'name': BRAND_FONT, 'size': 18, 'bold': False},
            'caption':  {'name': BRAND_FONT, 'size': 12, 'bold': False},
        }

    def add_title_slide(self, title, subtitle=None):
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[0])
        ts = slide.shapes.title
        ts.text = title
        self._style(ts.text_frame.paragraphs[0], 'title', 'primary')
        if subtitle and len(slide.placeholders) > 1:
            sub = slide.placeholders[1]
            sub.text = subtitle
            self._style(sub.text_frame.paragraphs[0], 'subtitle', 'muted')
        return slide

    def _style(self, paragraph, font_style, color_name):
        cfg = self.fonts[font_style]
        paragraph.font.name = cfg['name']
        paragraph.font.size = Pt(cfg['size'])
        paragraph.font.bold = cfg['bold']
        paragraph.font.color.rgb = self.colors[color_name]
```

## Complete Example: A Professional Presentation
```python
def create_professional_presentation():
    """Create a complete brand-consistent deck"""
    template = PresentationTemplate()
    prs = template.prs

    # 1. Title slide
    template.add_title_slide("Quarterly Business Review", "Q4 2024 Performance Analysis")

    # 2. Agenda
    agenda_items = [
        {'text': 'Executive Summary', 'level': 0},
        {'text': 'Sales Performance', 'level': 0},
        {'text': 'Regional Analysis', 'level': 1},
        {'text': 'Product Categories', 'level': 1},
        {'text': 'Market Trends', 'level': 0},
        {'text': 'Future Outlook', 'level': 0},
    ]
    add_formatted_text_slide(prs, "Agenda", agenda_items)

    # 3. Chart slide
    add_image_slide(prs, "Sales Performance", image_bytes=generate_chart_image())

    # 4. Table slide
    headers = ['Region', 'Q3 Sales', 'Q4 Sales', 'Growth %']
    data = [
        ['North', '$1.2M', '$1.5M', '+25%'],
        ['South', '$0.9M', '$1.1M', '+22%'],
        ['East',  '$1.5M', '$1.7M', '+13%'],
        ['West',  '$0.8M', '$0.9M', '+12%'],
    ]
    add_table_slide(prs, "Regional Performance", data, headers)

    # 5. Key takeaways
    takeaways = [
        {'text': 'Strong growth across all regions', 'level': 0, 'bold': True},
        {'text': 'Product A leading in market share', 'level': 0},
        {'text': 'Positive outlook for Q1 2025', 'level': 0},
        {'text': 'Recommend continued investment in R&D', 'level': 0, 'color': NEBULA['accent']},
    ]
    add_formatted_text_slide(prs, "Key Takeaways", takeaways)

    prs.save('professional_presentation.pptx')
    print("Presentation created successfully!")
```

## Speaker Notes
```python
def add_speaker_notes(slide, notes_text):
    """Add speaker notes to a slide"""
    slide.notes_slide.notes_text_frame.text = notes_text
```

## Hyperlinks
```python
def add_hyperlink(shape, url):
    """Add a hyperlink to a shape"""
    shape.click_action.hyperlink.address = url
```

> ⚠️ **Slide transitions:** `python-pptx` does **not** expose a supported API for slide transitions or animations — there is no `PP_TRANSITION`. If transitions are essential, either (a) build the deck from a template that already defines them, or (b) inject the `<p:transition>` element into each slide's XML manually via `slide._element`. Do not invent a transition API; it will raise `ImportError`/`AttributeError`.

## Validation
```python
from pptx.util import Inches
from pptx.enum.shapes import MSO_SHAPE_TYPE

def validate_presentation(prs):
    """Validate a deck for common issues"""
    issues = []
    for idx, slide in enumerate(prs.slides, start=1):
        if slide.shapes.title and not (slide.shapes.title.text or '').strip():
            issues.append(f"Slide {idx}: empty title")
        for shape in slide.shapes:
            if getattr(shape, 'has_text_frame', False) and shape.text:
                low = shape.text.lower()
                if 'placeholder' in low or 'lorem ipsum' in low:
                    issues.append(f"Slide {idx}: placeholder text remains")
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                if shape.width < Inches(1) or shape.height < Inches(1):
                    issues.append(f"Slide {idx}: image may be too small")
    return issues
```

## Tips for Visual Appeal
- **Color:** stick to the brand palette; 3–4 colors max per slide. Bright cyan `#00d4ff` is for fills/accents, not small text.
- **Typography:** use `Segoe UI` throughout; keep sizes consistent (title 40pt, body 18pt). Bold/italic for emphasis only.
- **Layout:** generous white space, consistent margins, aligned elements, one idea per slide.
- **Images:** high-resolution (300 DPI), preserved aspect ratios, consistent style.
- **Accessibility:** high contrast, readable sizes, alt text on images (see [skills-accessibility.md](skills-accessibility.md)).

## Best Practices Summary
1. **Plan** the slide structure before coding.
2. **Be consistent** — reuse `PresentationTemplate` and the brand constants.
3. **Optimize** image sizes; limit heavy graphics.
4. **Validate** with `validate_presentation()` before delivering.
5. **Cite** any external data on the slide or in the notes (see [skills-citations-grounding.md](skills-citations-grounding.md)).
