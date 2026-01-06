---
name: pdf
description: Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs using reportlab and platypus, merging/splitting documents, and handling forms. When the agent needs to generate or analyze PDF documents at scale.
license: Proprietary.
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations using Python libraries and command-line tools. Always use the libraries pypdf and reportlab with platypus first before any other agents are to be used.
## General PDF Rules
- When creating PDFs, do not use page breaks for small sections.  Only use page breaks for sections that extend over multiple pages.
- When generating PDFs from output, ensure that the entirety of the previous output is included in the output file.  Do not summarize the output further to create a document.  
- Create styles and use elements available in reportlab to ensure high quality visually appealing documents are created.
- All previous outputs can be found from previous assistants threads.  

## Quick Start

```python
from pypdf2 import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Task Python Libraries

### pypdf - Basic Operations

#### Merge PDFs
Use PdfMerger from the PyPDF2 library

#### Split PDF
Use PdfReader, PdfWriter from the PyPDF2 library

#### Extract Metadata
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

#### Rotate Pages
Use PdfReader, PdfWriter from the PyPDF2 library

### pdfplumber - Text and Table Extraction

#### Extract Text with Layout
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### Advanced Table Extraction
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Check if table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab - Create, generate, and convert PDFs using Platypus

#### Color palette and formatting
- Always use the following color palette for all newly created documents:
["#00346d","#2d6db4","#4b87ce","#003a76","#2868af"]
- Always use the font type Helvetica

#### Basic PDF Creation with Platypus
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

# Define color palette
COLORS = {
    'primary': HexColor('#00346d'),
    'secondary': HexColor('#2d6db4'),
    'accent': HexColor('#4b87ce'),
    'dark': HexColor('#003a76'),
    'light': HexColor('#2868af')
}

# Create document
doc = SimpleDocTemplate("output.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Custom styles with color palette
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Title'],
    textColor=COLORS['primary'],
    fontName='Helvetica-Bold',
    fontSize=24
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading1'],
    textColor=COLORS['dark'],
    fontName='Helvetica-Bold',
    fontSize=16
)

# Add content
title = Paragraph("Document Title", title_style)
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body text using Helvetica font.", styles['Normal'])
story.append(body)

# Build PDF
doc.build(story)
```

#### Create PDF with Tables using Platypus
```python
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

doc = SimpleDocTemplate("table_report.pdf", pagesize=letter)
story = []
styles = getSampleStyleSheet()

# Add title
story.append(Paragraph("Sales Report", styles['Title']))
story.append(Spacer(1, 0.5*inch))

# Create table data
data = [
    ['Product', 'Q1', 'Q2', 'Q3', 'Q4'],
    ['Product A', '$10,000', '$12,000', '$14,000', '$16,000'],
    ['Product B', '$8,000', '$9,000', '$10,000', '$11,000'],
    ['Product C', '$15,000', '$17,000', '$19,000', '$21,000'],
]

# Create table
table = Table(data)

# Apply table style with color palette
table.setStyle(TableStyle([
    # Header row
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#00346d')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    
    # Data rows
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
    ('GRID', (0, 0), (-1, -1), 1, HexColor('#2d6db4')),
    
    # Alternating row colors
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor('#e8f2ff')]),
]))

story.append(table)
doc.build(story)
```

#### Advanced PDF Creation with Platypus
```python
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.platypus import Table, TableStyle, KeepTogether
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

# Create custom page template
def create_letterhead(canvas, doc):
    """Add letterhead to each page"""
    canvas.saveState()
    
    # Add header with color
    canvas.setFillColor(HexColor('#00346d'))
    canvas.rect(0, letter[1] - inch, letter[0], inch, fill=1)
    
    # Add company name
    canvas.setFillColor(colors.white)
    canvas.setFont('Helvetica-Bold', 16)
    canvas.drawCentredString(letter[0]/2, letter[1] - 0.5*inch, "Company Name")
    
    # Add footer
    canvas.setFillColor(HexColor('#2d6db4'))
    canvas.setFont('Helvetica', 9)
    canvas.drawString(inch, 0.5*inch, f"Page {doc.page}")
    
    canvas.restoreState()

# Create document with custom template
doc = SimpleDocTemplate(
    "advanced_report.pdf",
    pagesize=letter,
    topMargin=1.5*inch,
    bottomMargin=inch
)

# Custom styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name='CustomBody',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=11,
    leading=14,
    alignment=TA_JUSTIFY,
    spaceAfter=12
))

styles.add(ParagraphStyle(
    name='ColoredHeading',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=14,
    textColor=HexColor('#003a76'),
    spaceAfter=6
))

# Build story
story = []

# Add content
story.append(Paragraph("Executive Summary", styles['ColoredHeading']))
story.append(Paragraph(
    "This report demonstrates advanced PDF creation using ReportLab's Platypus layout engine. "
    "The document includes custom styling, tables, and professional formatting.",
    styles['CustomBody']
))

story.append(Spacer(1, 0.3*inch))

# Add a complex table
data = [
    ['Department', 'Budget', 'Actual', 'Variance', 'Status'],
    ['Sales', '$100,000', '$110,000', '+$10,000', 'On Track'],
    ['Marketing', '$50,000', '$48,000', '-$2,000', 'Under Budget'],
    ['Operations', '$200,000', '$205,000', '+$5,000', 'Over Budget'],
    ['IT', '$75,000', '$75,000', '$0', 'On Budget'],
]

table = Table(data, colWidths=[2*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
table.setStyle(TableStyle([
    # Header styling
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#00346d')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    
    # Data styling
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#4b87ce')),
    
    # Conditional formatting for status
    ('BACKGROUND', (4, 1), (4, 1), colors.lightgreen),
    ('BACKGROUND', (4, 2), (4, 2), colors.lightgreen),
    ('BACKGROUND', (4, 3), (4, 3), colors.lightyellow),
    ('BACKGROUND', (4, 4), (4, 4), colors.lightblue),
]))

story.append(KeepTogether([
    Paragraph("Financial Summary", styles['ColoredHeading']),
    table
]))

# Build PDF with custom page template
doc.build(story, onFirstPage=create_letterhead, onLaterPages=create_letterhead)
```

#### Create Forms and Interactive Elements
```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfform
from reportlab.lib.colors import HexColor
from reportlab.lib import colors

# Note: For forms, we need to use canvas initially, then can convert to platypus
c = canvas.Canvas("form.pdf", pagesize=letter)

# Set font
c.setFont("Helvetica", 12)

# Add form title with color
c.setFillColor(HexColor('#00346d'))
c.setFont("Helvetica-Bold", 16)
c.drawString(100, 750, "Application Form")

# Reset to normal text
c.setFillColor(colors.black)
c.setFont("Helvetica", 12)

# Add text fields
c.drawString(100, 700, "Name:")
c.acroForm.textfield(
    name='name',
    tooltip='Enter your full name',
    x=200, y=695,
    borderStyle='inset',
    width=200,
    textColor=colors.black,
    fillColor=colors.white,
    borderColor=HexColor('#2d6db4')
)

# Add checkbox
c.drawString(100, 650, "I agree to the terms:")
c.acroForm.checkbox(
    name='agree',
    tooltip='Check to agree',
    x=250, y=645,
    buttonStyle='check',
    borderColor=HexColor('#2d6db4'),
    fillColor=colors.white,
    textColor=colors.black,
    forceBorder=True
)

# Save the form
c.save()
```

#### Create Charts and Graphics with Platypus
```python
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import letter
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

doc = SimpleDocTemplate("charts.pdf", pagesize=letter)
story = []

# Create a bar chart
drawing = Drawing(400, 200)
bc = VerticalBarChart()
bc.x = 50
bc.y = 50
bc.height = 125
bc.width = 300
bc.data = [[10, 20, 30, 40], [15, 25, 35, 45]]
bc.categoryAxis.categoryNames = ['Q1', 'Q2', 'Q3', 'Q4']
bc.valueAxis.valueMin = 0
bc.valueAxis.valueMax = 50
bc.bars[0].fillColor = HexColor('#00346d')
bc.bars[1].fillColor = HexColor('#4b87ce')
drawing.add(bc)
story.append(drawing)

# Create a pie chart
drawing2 = Drawing(400, 200)
pie = Pie()
pie.x = 150
pie.y = 50
pie.width = 100
pie.height = 100
pie.data = [30, 25, 20, 15, 10]
pie.labels = ['Product A', 'Product B', 'Product C', 'Product D', 'Other']
pie.slices.strokeWidth = 0.5
# Apply color palette to slices
for i, color in enumerate([HexColor(c) for c in ["#00346d","#2d6db4","#4b87ce","#003a76","#2868af"]]):
    pie.slices[i].fillColor = color
drawing2.add(pie)
story.append(drawing2)

doc.build(story)
```

#### Create Multi-Column Layout with Platypus
```python
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, FrameBreak
from reportlab.platypus import Frame, PageTemplate, BaseDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

class TwoColumnDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        BaseDocTemplate.__init__(self, filename, **kwargs)
        
        # Define frames for two columns
        frame1 = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width/2 - 6,
            self.height,
            id='col1'
        )
        frame2 = Frame(
            self.leftMargin + self.width/2 + 6,
            self.bottomMargin,
            self.width/2 - 6,
            self.height,
            id='col2'
        )
        
        # Add page template
        self.addPageTemplates([
            PageTemplate(id='TwoCol', frames=[frame1, frame2])
        ])

# Create document
doc = TwoColumnDocTemplate("two_column.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add content
for i in range(10):
    story.append(Paragraph(f"Section {i+1}", styles['Heading2']))
    story.append(Paragraph("Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 10, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Force column break after every 3 sections
    if i % 3 == 2:
        story.append(FrameBreak())

doc.build(story)
```

## Common Tasks

### Extract Text from Scanned PDFs
```python
# Requires: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### Extract text and output to PDFs using Platypus
- Do not use page breaks for small sections.  Only use page breaks for sections that extend over multiple pages.

```python
import fitz  # PyMuPDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch

# Extract text from source PDF
pdf_path = "source.pdf"
doc = fitz.open(pdf_path)
all_text = ""
for page in doc:
    all_text += page.get_text() + "\n"

# Create new PDF with extracted text using Platypus
output_doc = SimpleDocTemplate("extracted_text.pdf", pagesize=letter)
styles = getSampleStyleSheet()

# Custom style with color palette
custom_style = ParagraphStyle(
    'CustomStyle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=11,
    textColor=HexColor('#00346d')
)

story = []
# Add title
title_style = ParagraphStyle(
    'Title',
    parent=styles['Title'],
    fontName='Helvetica-Bold',
    fontSize=18,
    textColor=HexColor('#003a76')
)
story.append(Paragraph("Extracted Text Output", title_style))
story.append(Spacer(1, 0.5*inch))

# Add extracted text
paragraphs = all_text.split('\n\n')
for para in paragraphs:
    if para.strip():
        story.append(Paragraph(para, custom_style))
        story.append(Spacer(1, 0.2*inch))

output_doc.build(story)
```

### Add Watermark using Platypus
```python
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from pypdf2 import PdfReader, PdfWriter
import io

# First create a watermark PDF using Platypus
def create_watermark():
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    
    # Set watermark properties
    c.setFont("Helvetica-Bold", 50)
    c.setFillColor(HexColor('#2d6db4'))
    c.setFillAlpha(0.3)  # Semi-transparent
    
    # Rotate and center the watermark
    c.saveState()
    c.translate(letter[0]/2, letter[1]/2)
    c.rotate(45)
    c.drawCentredString(0, 0, "CONFIDENTIAL")
    c.restoreState()
    
    c.save()
    packet.seek(0)
    return PdfReader(packet)

# Apply watermark to existing PDF
watermark = create_watermark().pages[0]
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Extract Images
```python
import fitz  # PyMuPDF
import zipfile
import os

def extract_images_from_pdf(pdf_path, output_folder="extracted_images"):
    # Create output folder
    os.makedirs(output_folder, exist_ok=True)
    
    # Open PDF
    pdf = fitz.open(pdf_path)
    
    # Extract images
    image_count = 0
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            # Get image data
            xref = img[0]
            pix = fitz.Pixmap(pdf, xref)
            
            # Save image
            if pix.n - pix.alpha < 4:  # GRAY or RGB
                image_count += 1
                img_path = f"{output_folder}/page{page_num+1}_img{img_index+1}.png"
                pix.save(img_path)
            else:  # CMYK
                image_count += 1
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                img_path = f"{output_folder}/page{page_num+1}_img{img_index+1}.png"
                pix1.save(img_path)
                pix1 = None
            
            pix = None
    
    # Create zip file
    with zipfile.ZipFile(f"{output_folder}.zip", 'w') as zipf:
        for root, dirs, files in os.walk(output_folder):
            for file in files:
                zipf.write(os.path.join(root, file), file)
    
    return f"Extracted {image_count} images to {output_folder}.zip"
```

### Password Protection
```python
from pypdf2 import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Add password
writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

### Create Invoice with Platypus
```python
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from datetime import datetime

# Create document
doc = SimpleDocTemplate("invoice.pdf", pagesize=letter)
story = []
styles = getSampleStyleSheet()

# Custom styles
invoice_title = ParagraphStyle(
    'InvoiceTitle',
    parent=styles['Title'],
    fontSize=24,
    textColor=HexColor('#00346d'),
    spaceAfter=30
)

# Add invoice header
story.append(Paragraph("INVOICE", invoice_title))
story.append(Spacer(1, 0.3*inch))

# Company info
company_info = [
    ['Your Company Name', 'Invoice #: INV-001'],
    ['123 Business Street', f'Date: {datetime.now().strftime("%B %d, %Y")}'],
    ['City, State 12345', 'Due Date: Net 30'],
]

info_table = Table(company_info, colWidths=[3.5*inch, 3*inch])
info_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
]))
story.append(info_table)
story.append(Spacer(1, 0.5*inch))

# Invoice items
items = [
    ['Description', 'Quantity', 'Unit Price', 'Total'],
    ['Professional Services', '10', '$100.00', '$1,000.00'],
    ['Consulting Hours', '5', '$150.00', '$750.00'],
    ['Project Management', '1', '$500.00', '$500.00'],
    ['', '', 'Subtotal:', '$2,250.00'],
    ['', '', 'Tax (10%):', '$225.00'],
    ['', '', 'Total:', '$2,475.00'],
]

items_table = Table(items, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
items_table.setStyle(TableStyle([
    # Header
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#00346d')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    
    # Data
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
    ('GRID', (0, 0), (-1, 3), 1, HexColor('#2d6db4')),
    
    # Total rows
    ('FONTNAME', (2, 4), (-1, -1), 'Helvetica-Bold'),
    ('LINEABOVE', (2, 4), (-1, 4), 1, colors.black),
]))

story.append(items_table)

# Build PDF
doc.build(story)
```

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab + platypus | SimpleDocTemplate + Story |
| Command line merge | qpdf | `qpdf --empty --pages...` |
| OCR scanned PDFs | pytesseract | Convert to image first |
| Professional layouts | platypus | Frames, PageTemplates |
| Forms | reportlab canvas | `acroForm.textfield()` |
| Charts | reportlab graphics | Drawing + Charts |
| Watermarks | platypus + pypdf | Create watermark, merge PDFs |
| Multi-column | platypus | Custom DocTemplate with Frames |