---
name: docx
description: Comprehensive DOCX manipulation toolkit for extracting text and tables, creating new documents, merging/splitting content, and handling formatting. When the agent needs to generate or analyze Word documents at scale.
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX Processing Guide

## Overview

This guide covers essential DOCX processing operations using Python libraries and command-line tools. Always use the libraries python-docx, docxtpl, and docx2pdf first before any other agents are to be used.

## Quick Start

<!-- python -->
    from docx import Document

    # Read a DOCX
    doc = Document("document.docx")
    print(f"Paragraphs: {len(doc.paragraphs)}")

    # Extract text
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

## Professional Document Formatting Standards

### Color Palette
Always use the following professional color palette for all newly created documents:
- Primary Blue: #003d7a (RGB: 0, 61, 122)
- Secondary Blue: #0066cc (RGB: 0, 102, 204)
- Accent Blue: #4d94ff (RGB: 77, 148, 255)
- Dark Gray: #333333 (RGB: 51, 51, 51)
- Light Gray: #666666 (RGB: 102, 102, 102)

### Typography Standards
- **Headings**: Calibri Light, sizes 28pt (Title), 18pt (Heading 1), 14pt (Heading 2), 12pt (Heading 3)
- **Body Text**: Calibri, 11pt, 1.15 line spacing
- **Captions**: Calibri, 9pt, italic, color #666666
- **Tables**: Calibri, 10pt, with alternating row colors (#f5f5f5)

### Document Layout
- **Margins**: 1 inch all sides (Normal template)
- **Paragraph Spacing**: 6pt before, 6pt after for body text
- **Heading Spacing**: 12pt before, 6pt after
- **First Line Indent**: 0.5 inches for body paragraphs

## Task Python Libraries

### python-docx - Core Operations

#### Create Professional Document

<!-- python -->
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.style import WD_STYLE_TYPE

    def create_professional_document():
        doc = Document()
        
        # Define custom styles
        styles = doc.styles
        
        # Custom Title Style
        title_style = styles.add_style('CustomTitle', WD_STYLE_TYPE.PARAGRAPH)
        title_style.font.name = 'Calibri Light'
        title_style.font.size = Pt(28)
        title_style.font.color.rgb = RGBColor(0, 61, 122)
        title_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title_style.paragraph_format.space_after = Pt(12)
        
        # Add title
        title = doc.add_paragraph('Annual Report 2024', style='CustomTitle')
        
        # Add subtitle
        subtitle = doc.add_paragraph()
        subtitle_run = subtitle.add_run('Excellence in Innovation')
        subtitle_run.font.name = 'Calibri Light'
        subtitle_run.font.size = Pt(16)
        subtitle_run.font.color.rgb = RGBColor(102, 102, 102)
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Add executive summary with proper formatting
        doc.add_heading('Executive Summary', level=1)
        summary = doc.add_paragraph()
        summary.paragraph_format.first_line_indent = Inches(0.5)
        summary.paragraph_format.space_after = Pt(6)
        summary.add_run('This report presents our achievements and strategic initiatives for the fiscal year 2024.')
        
        return doc

    doc = create_professional_document()
    doc.save('professional_report.docx')

#### Extract All Content with Formatting Info

<!-- python -->
    from docx import Document
    import json

    def extract_formatted_content(filename):
        doc = Document(filename)
        content = []
        
        # Extract paragraphs with formatting
        for para in doc.paragraphs:
            para_info = {
                'text': para.text,
                'style': para.style.name,
                'alignment': str(para.alignment),
                'runs': []
            }
            
            for run in para.runs:
                run_info = {
                    'text': run.text,
                    'bold': run.bold,
                    'italic': run.italic,
                    'underline': run.underline,
                    'font_name': run.font.name,
                    'font_size': run.font.size.pt if run.font.size else None,
                    'color': run.font.color.rgb if run.font.color.rgb else None
                }
                para_info['runs'].append(run_info)
            
            content.append(para_info)
        
        # Extract tables
        tables = []
        for table in doc.tables:
            table_data = []
            for row in table.rows:
                row_data = [cell.text for cell in row.cells]
                table_data.append(row_data)
            tables.append(table_data)
        
        return {'paragraphs': content, 'tables': tables}

#### Advanced Table Creation

<!-- python -->
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import parse_xml
    from docx.oxml.ns import nsdecls

    def create_professional_table(doc, data, headers):
        # Create table with custom style
        rows = len(data) + 1  # +1 for header
        cols = len(headers)
        table = doc.add_table(rows=rows, cols=cols)
        
        # Apply custom table style
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = True
        
        # Style header row
        header_cells = table.rows[0].cells
        for i, header in enumerate(headers):
            cell = header_cells[i]
            cell.text = header
            
            # Format header cell
            shading_elm = parse_xml(r'<w:shd {} w:fill="003d7a"/>'.format(nsdecls('w')))
            cell._element.get_or_add_tcPr().append(shading_elm)
            
            # Format header text
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)
                    run.font.size = Pt(11)
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Add data with alternating row colors
        for row_idx, row_data in enumerate(data):
            row_cells = table.rows[row_idx + 1].cells
            
            # Apply alternating row color
            if row_idx % 2 == 1:
                for cell in row_cells:
                    shading_elm = parse_xml(r'<w:shd {} w:fill="f5f5f5"/>'.format(nsdecls('w')))
                    cell._element.get_or_add_tcPr().append(shading_elm)
            
            # Add data
            for col_idx, value in enumerate(row_data):
                cell = row_cells[col_idx]
                cell.text = str(value)
                
                # Center align numbers
                if isinstance(value, (int, float)):
                    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        return table

### docxtpl - Template-Based Generation

#### Create Dynamic Documents from Templates

<!-- python -->
    from docxtpl import DocxTemplate, RichText
    from datetime import datetime

    def generate_from_template(template_path, output_path):
        doc = DocxTemplate(template_path)
        
        # Create rich text with formatting
        company_name = RichText()
        company_name.add('TechCorp Industries', 
                        color='003d7a', 
                        bold=True, 
                        size=14)
        
        # Prepare context with various data types
        context = {
            'company': company_name,
            'date': datetime.now().strftime('%B %d, %Y'),
            'quarter': 'Q4 2024',
            'revenue': 1500000,
            'growth_rate': 15.5,
            'departments': [
                {'name': 'Engineering', 'headcount': 150, 'budget': 500000},
                {'name': 'Sales', 'headcount': 75, 'budget': 300000},
                {'name': 'Marketing', 'headcount': 50, 'budget': 200000}
            ],
            'achievements': [
                'Launched new product line',
                'Expanded to 3 new markets',
                'Achieved ISO certification'
            ]
        }
        
        # Render the template
        doc.render(context)
        doc.save(output_path)

#### Advanced Template Features

<!-- python -->
    from docxtpl import DocxTemplate, RichText, InlineImage
    from docx.shared import Mm
    import matplotlib.pyplot as plt
    import io

    def create_report_with_charts(template_path, output_path):
        doc = DocxTemplate(template_path)
        
        # Create a chart
        fig, ax = plt.subplots(figsize=(6, 4))
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
        sales = [100, 120, 140, 110, 160]
        
        ax.bar(months, sales, color='#003d7a')
        ax.set_title('Monthly Sales Performance', fontsize=14, fontweight='bold')
        ax.set_ylabel('Sales (in thousands)', fontsize=12)
        ax.grid(axis='y', alpha=0.3)
        
        # Save chart to bytes buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        # Create inline image
        chart_image = InlineImage(doc, img_buffer, width=Mm(120))
        
        # Create formatted text elements
        highlight = RichText()
        highlight.add('Key Achievement: ', bold=True, color='003d7a')
        highlight.add('Record sales in May with ')
        highlight.add('$160,000', bold=True, color='0066cc')
        highlight.add(' in revenue')
        
        context = {
            'chart': chart_image,
            'highlight': highlight,
            'performance_summary': 'Q2 showed strong growth momentum'
        }
        
        doc.render(context)
        doc.save(output_path)

### Working with Styles and Themes

#### Create Custom Document Theme

<!-- python -->
    from docx import Document
    from docx.shared import Pt, RGBColor, Inches
    from docx.enum.style import WD_STYLE_TYPE
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    def setup_document_theme(doc):
        styles = doc.styles
        
        # Define color scheme
        colors = {
            'primary': RGBColor(0, 61, 122),
            'secondary': RGBColor(0, 102, 204),
            'accent': RGBColor(77, 148, 255),
            'text': RGBColor(51, 51, 51),
            'muted': RGBColor(102, 102, 102)
        }
        
        # Heading 1 Style
        h1 = styles['Heading 1']
        h1.font.name = 'Calibri Light'
        h1.font.size = Pt(18)
        h1.font.color.rgb = colors['primary']
        h1.paragraph_format.space_before = Pt(12)
        h1.paragraph_format.space_after = Pt(6)
        
        # Heading 2 Style
        h2 = styles['Heading 2']
        h2.font.name = 'Calibri Light'
        h2.font.size = Pt(14)
        h2.font.color.rgb = colors['secondary']
        h2.paragraph_format.space_before = Pt(12)
        h2.paragraph_format.space_after = Pt(6)
        
        # Normal Style
        normal = styles['Normal']
        normal.font.name = 'Calibri'
        normal.font.size = Pt(11)
        normal.font.color.rgb = colors['text']
        normal.paragraph_format.line_spacing = 1.15
        normal.paragraph_format.space_after = Pt(6)
        
        # Create custom styles
        # Callout Box Style
        callout = styles.add_style('CalloutBox', WD_STYLE_TYPE.PARAGRAPH)
        callout.base_style = styles['Normal']
        callout.font.size = Pt(10)
        callout.font.color.rgb = colors['primary']
        callout.paragraph_format.left_indent = Inches(0.5)
        callout.paragraph_format.right_indent = Inches(0.5)
        callout.paragraph_format.space_before = Pt(6)
        callout.paragraph_format.space_after = Pt(6)
        
        # Quote Style
        quote = styles.add_style('StyledQuote', WD_STYLE_TYPE.PARAGRAPH)
        quote.base_style = styles['Normal']
        quote.font.italic = True
        quote.font.size = Pt(12)
        quote.font.color.rgb = colors['muted']
        quote.paragraph_format.left_indent = Inches(1)
        quote.paragraph_format.right_indent = Inches(1)
        quote.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        return doc

### Advanced Operations

#### Add Watermark with Transparency

<!-- python -->
    from docx import Document
    from docx.shared import Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    def add_diagonal_watermark(doc, text):
        # Create watermark in header
        section = doc.sections[0]
        header = section.header
        
        # Create paragraph for watermark
        paragraph = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
        
        # Create the watermark run
        run = paragraph.add_run()
        
        # Create watermark element
        watermark = OxmlElement('w:pict')
        shape = OxmlElement('v:shape')
        shape.set(qn('w:style'), 'position:absolute;margin-left:0;margin-top:0;width:600pt;height:800pt;rotation:315;z-index:-1')
        
        textpath = OxmlElement('v:textpath')
        textpath.set(qn('v:string'), text)
        textpath.set(qn('w:style'), 'font-family:"Calibri Light";font-size:120pt')
        
        fill = OxmlElement('v:fill')
        fill.set(qn('w:opacity'), '0.15')
        fill.set(qn('w:color'), '#cccccc')
        
        shape.append(textpath)
        shape.append(fill)
        watermark.append(shape)
        
        run._element.append(watermark)
        
        return doc

#### Convert DOCX to PDF with Formatting Preservation

<!-- python -->
    from docx2pdf import convert
    import os
    import sys

    def convert_to_pdf_with_options(docx_path, pdf_path=None):
        """
        Convert DOCX to PDF preserving all formatting
        """
        if pdf_path is None:
            pdf_path = os.path.splitext(docx_path)[0] + '.pdf'
        
        try:
            # For Windows
            if sys.platform == 'win32':
                import win32com.client
                word = win32com.client.Dispatch("Word.Application")
                word.Visible = False
                
                doc = word.Documents.Open(os.path.abspath(docx_path))
                doc.SaveAs2(os.path.abspath(pdf_path), FileFormat=17)  # 17 = PDF format
                doc.Close()
                word.Quit()
            else:
                # For other platforms, use docx2pdf
                convert(docx_path, pdf_path)
                
            return pdf_path
            
        except Exception as e:
            print(f"Error converting to PDF: {e}")
            # Fallback to basic conversion
            convert(docx_path, pdf_path)
            return pdf_path

#### Extract and Analyze Document Structure

<!-- python -->
    from docx import Document
    import json

    def analyze_document_structure(filename):
        doc = Document(filename)
        
        structure = {
            'metadata': {
                'author': doc.core_properties.author,
                'created': str(doc.core_properties.created),
                'modified': str(doc.core_properties.modified),
                'title': doc.core_properties.title,
                'subject': doc.core_properties.subject
            },
            'statistics': {
                'paragraphs': len(doc.paragraphs),
                'tables': len(doc.tables),
                'sections': len(doc.sections),
                'styles_used': set()
            },
            'content_outline': []
        }
        
        # Analyze content structure
        for para in doc.paragraphs:
            if para.style.name.startswith('Heading'):
                level = para.style.name.split()[-1]
                structure['content_outline'].append({
                    'level': level,
                    'text': para.text,
                    'style': para.style.name
                })
            
            if para.style.name:
                structure['statistics']['styles_used'].add(para.style.name)
        
        # Convert set to list for JSON serialization
        structure['statistics']['styles_used'] = list(structure['statistics']['styles_used'])
        
        return structure

### Working with Forms and Fields

#### Create Fillable Document Forms

<!-- python -->
    from docx import Document
    from docx.shared import Pt, RGBColor, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    def create_form_document():
        doc = Document()
        
        # Add form title
        title = doc.add_heading('Employee Information Form', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Helper function to add form field
        def add_form_field(label, field_length='_' * 50):
            p = doc.add_paragraph()
            p.add_run(f'{label}: ').bold = True
            field_run = p.add_run(field_length)
            field_run.font.color.rgb = RGBColor(200, 200, 200)
            return p
        
        # Add form fields
        add_form_field('Full Name')
        add_form_field('Employee ID', '_' * 20)
        add_form_field('Department')
        add_form_field('Start Date', '__/__/____')
        
        # Add a checkbox section
        doc.add_paragraph()
        doc.add_paragraph('Benefits Enrollment:').bold = True
        
        benefits = ['Health Insurance', 'Dental Insurance', '401(k)', 'Life Insurance']
        for benefit in benefits:
            p = doc.add_paragraph()
            p.add_run('☐  ' + benefit)
            p.paragraph_format.left_indent = Inches(0.5)
        
        # Add signature section
        doc.add_paragraph()
        doc.add_paragraph()
        
        sig_table = doc.add_table(rows=2, cols=2)
        sig_table.autofit = False
        
        # Signature fields
        sig_table.cell(0, 0).text = 'Employee Signature: _______________________'
        sig_table.cell(0, 1).text = 'Date: ______________'
        sig_table.cell(1, 0).text = 'HR Representative: _______________________'
        sig_table.cell(1, 1).text = 'Date: ______________'
        
        return doc

### Document Comparison and Merging

#### Compare Two Documents

<!-- python -->
    from docx import Document
    import difflib

    def compare_documents(doc1_path, doc2_path):
        doc1 = Document(doc1_path)
        doc2 = Document(doc2_path)
        
        # Extract text from both documents
        text1 = '\n'.join([p.text for p in doc1.paragraphs])
        text2 = '\n'.join([p.text for p in doc2.paragraphs])
        
        # Create a new document for the comparison
        result_doc = Document()
        result_doc.add_heading('Document Comparison Report', 0)
        
        # Add metadata
        result_doc.add_paragraph(f'Document 1: {doc1_path}')
        result_doc.add_paragraph(f'Document 2: {doc2_path}')
        result_doc.add_paragraph()
        
        # Perform comparison
        differ = difflib.unified_diff(
            text1.splitlines(),
            text2.splitlines(),
            lineterm='',
            fromfile='Document 1',
            tofile='Document 2'
        )
        
        # Add differences to document
        result_doc.add_heading('Differences Found:', level=1)
        
        for line in differ:
            p = result_doc.add_paragraph()
            if line.startswith('+'):
                run = p.add_run(line)
                run.font.color.rgb = RGBColor(0, 128, 0)  # Green for additions
            elif line.startswith('-'):
                run = p.add_run(line)
                run.font.color.rgb = RGBColor(255, 0, 0)  # Red for deletions
            else:
                p.add_run(line)
        
        return result_doc

### Performance Optimization

#### Batch Processing Documents

<!-- python -->
    import os
    from docx import Document
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import time

    def process_single_document(file_path, output_dir):
        """Process a single document"""
        try:
            doc = Document(file_path)
            
            # Add watermark
            add_watermark(doc, "PROCESSED")
            
            # Add processing timestamp
            doc.add_paragraph(f"Processed on: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Save to output directory
            filename = os.path.basename(file_path)
            output_path = os.path.join(output_dir, f"processed_{filename}")
            doc.save(output_path)
            
            return f"Success: {filename}"
        except Exception as e:
            return f"Error processing {file_path}: {str(e)}"

    def batch_process_documents(input_dir, output_dir, max_workers=4):
        """Process multiple documents in parallel"""
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Get all.docx files
        docx_files = [
            os.path.join(input_dir, f) 
            for f in os.listdir(input_dir) 
            if f.endswith('.docx')
        ]
        
        results = []
        
        # Process files in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(process_single_document, file_path, output_dir): file_path
                for file_path in docx_files
            }
            
            for future in as_completed(future_to_file):
                result = future.result()
                results.append(result)
                print(result)
        
        return results

## Common Tasks

### Generate Reports with Charts

<!-- python -->
    from docx import Document
    from docx.shared import Inches
    import matplotlib.pyplot as plt
    import io

    def create_report_with_charts():
        doc = Document()
        
        # Setup document theme
        doc = setup_document_theme(doc)
        
        # Add title
        doc.add_heading('Quarterly Business Report', 0)
        
        # Create and add chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Revenue chart
        quarters = ['Q1', 'Q2', 'Q3', 'Q4']
        revenue = [250, 300, 280, 350]
        ax1.bar(quarters, revenue, color='#003d7a')
        ax1.set_title('Quarterly Revenue (in thousands)', fontweight='bold')
        ax1.set_ylabel('Revenue ($k)')
        ax1.grid(axis='y', alpha=0.3)
        
        # Pie chart for market share
        segments = ['Product A', 'Product B', 'Product C', 'Other']
        sizes = [35, 30, 25, 10]
        colors = ['#003d7a', '#0066cc', '#4d94ff', '#cccccc']
        ax2.pie(sizes, labels=segments, colors=colors, autopct='%1.1f%%')
        ax2.set_title('Market Share by Product', fontweight='bold')
        
        # Save chart to bytes
        img_buffer = io.BytesIO()
        plt.tight_layout()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        # Add chart to document
        doc.add_picture(img_buffer, width=Inches(6))
        
        # Add analysis text
        doc.add_heading('Key Insights', level=1)
        insights = doc.add_paragraph()
        insights.add_run('Revenue Growth: ').bold = True
        insights.add_run('Q4 showed a ')
        insights.add_run('40% increase').font.color.rgb = RGBColor(0, 128, 0)
        insights.add_run(' compared to Q1.')
        
        return doc

### Create Multi-Column Layouts

<!-- python -->
    from docx import Document
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    def create_two_column_section(doc):
        # Add a section break
        section = doc.add_section()
        
        # Create columns element
        sectPr = section._element
        cols = OxmlElement('w:cols')
        cols.set(qn('w:num'), '2')  # Number of columns
        cols.set(qn('w:space'), '720')  # Space between columns (720 = 0.5 inch)
        
        sectPr.insert_element_before(cols, 'w:docGrid')
        
        # Add content to columns
        doc.add_heading('Two-Column Layout', level=1)
        
        for i in range(4):
            para = doc.add_paragraph(
                f'This is paragraph {i+1} in the two-column section. '
                'The text will automatically flow from the first column '
                'to the second column as needed. This creates a '
                'newspaper-style layout.'
            )
            para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        return section

### Extract Images with Metadata

<!-- python -->
    from docx import Document
    import os
    from PIL import Image
    import json

    def extract_images_with_metadata(docx_path, output_dir):
        doc = Document(docx_path)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        image_info = []
        
        for i, rel in enumerate(doc.part.rels.values()):
            if "image" in rel.target_ref:
                img_data = rel.target_part.blob
                
                # Determine image format
                if img_data.startswith(b'\xff\xd8'):
                    ext = '.jpg'
                elif img_data.startswith(b'\x89PNG'):
                    ext = '.png'
                else:
                    ext = '.img'
                
                img_name = f"image_{i+1}{ext}"
                img_path = os.path.join(output_dir, img_name)
                
                # Save image
                with open(img_path, "wb") as f:
                    f.write(img_data)
                
                # Get image metadata
                with Image.open(img_path) as img:
                    info = {
                        'filename': img_name,
                        'format': img.format,
                        'mode': img.mode,
                        'size': img.size,
                        'width': img.width,
                        'height': img.height
                    }
                    image_info.append(info)
        
        # Save metadata
        with open(os.path.join(output_dir, 'image_metadata.json'), 'w') as f:
            json.dump(image_info, f, indent=2)
        
        return image_info

### Mail Merge Operations

''' python 
    from docx import Document
    from docxtpl import DocxTemplate
    import csv

    def mail_merge_from_csv(template_path, csv_path, output_dir):
        """
        Perform mail merge using CSV data
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Read CSV data
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            records = list(reader)
        
        # Generate document for each record
        for i, record in enumerate(records):
            doc = DocxTemplate(template_path)
            
            # Add formatted fields
            if 'name' in record:
                record['formatted_name'] = RichText(record['name'], bold=True, size=14)
            
            # Render document
            doc.render(record)
            
            # Save with unique filename
            output_name = f"merged_{i+1}_{record.get('name', 'document').replace(' ', '_')}.docx"
            output_path = os.path.join(output_dir, output_name)
            doc.save(output_path)
        
        return len(records)

## Error Handling and Validation

<!-- python -->
    from docx import Document
    import os
    import logging

    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    def safe_document_operation(func):
        """Decorator for safe document operations"""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except FileNotFoundError as e:
                logger.error(f"File not found: {e}")
                return None
            except PermissionError as e:
                logger.error(f"Permission denied: {e}")
                return None
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return None
        return wrapper

    @safe_document_operation
    def validate_and_repair_document(file_path):
        """Validate document structure and attempt repairs"""
        doc = Document(file_path)
        
        issues = []
        repairs = []
        
        # Check for empty paragraphs
        empty_paras = [i for i, p in enumerate(doc.paragraphs) if not p.text.strip()]
        if empty_paras:
            issues.append(f"Found {len(empty_paras)} empty paragraphs")
            
        # Check for broken tables
        for i, table in enumerate(doc.tables):
            try:
                rows = len(table.rows)
                if rows == 0:
                    issues.append(f"Table {i} has no rows")
            except:
                issues.append(f"Table {i} is corrupted")
                
        # Check styles
        used_styles = set()
        for para in doc.paragraphs:
            if para.style:
                used_styles.add(para.style.name)
                
        # Create validation report
        report = {
            'file': file_path,
            'valid': len(issues) == 0,
            'issues': issues,
            'statistics': {
                'paragraphs': len(doc.paragraphs),
                'tables': len(doc.tables),
                'styles_used': list(used_styles)
            }
        }
        
        return report

## Advanced PDF Conversion

<!-- python -->
    from docx import Document
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    import os

    def advanced_docx_to_pdf(docx_path, pdf_path):
        """Convert DOCX to PDF with advanced formatting preservation"""
        
        # Read DOCX
        doc = Document(docx_path)
        
        # Create PDF
        pdf = SimpleDocTemplate(pdf_path, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Create custom styles matching DOCX formatting
        custom_styles = {
            'CustomTitle': ParagraphStyle(
                'CustomTitle',
                parent=styles['Title'],
                fontSize=28,
                textColor=colors.HexColor('#003d7a'),
                alignment=1  # Center
            ),
            'CustomHeading1': ParagraphStyle(
                'CustomHeading1',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#003d7a'),
                spaceBefore=12,
                spaceAfter=6
            ),
            'CustomBody': ParagraphStyle(
                'CustomBody',
                parent=styles['Normal'],
                fontSize=11,
                leading=13,
                spaceBefore=6,
                spaceAfter=6
            )
        }
        
        # Convert content
        for element in doc.element.body:
            if element.tag.endswith('p'):  # Paragraph
                para = element
                text = ''.join(node.text for node in para.iter() if node.text)
                
                # Determine style
                style = custom_styles.get('CustomBody')
                if any(run.bold for run in para.runs):
                    style = custom_styles.get('CustomHeading1')
                    
                if text.strip():
                    story.append(Paragraph(text, style))
                    
            elif element.tag.endswith('tbl'):  # Table
                # Extract table data
                table_data = []
                for row in element.findall('.//w:tr', namespaces=element.nsmap):
                    row_data = []
                    for cell in row.findall('.//w:tc', namespaces=element.nsmap):
                        cell_text = ''.join(
                            node.text for node in cell.iter() if node.text
                        )
                        row_data.append(cell_text)
                    table_data.append(row_data)
                
                if table_data:
                    # Create PDF table
                    t = Table(table_data)
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003d7a')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(t)
                    story.append(Spacer(1, 12))
        
        # Build PDF
        pdf.build(story)
        return pdf_path

## Document Security and Protection

<!-- python -->
    from docx import Document
    from cryptography.fernet import Fernet
    import base64
    import json
    import hashlib

    class SecureDocument:
        def __init__(self):
            self.key = Fernet.generate_key()
            self.cipher = Fernet(self.key)
        
        def encrypt_document_content(self, doc_path):
            """Encrypt sensitive content in document"""
            doc = Document(doc_path)
            encrypted_data = []
            
            # Extract and encrypt sensitive paragraphs
            for para in doc.paragraphs:
                if '[CONFIDENTIAL]' in para.text:
                    # Remove marker and encrypt
                    clean_text = para.text.replace('[CONFIDENTIAL]', '').strip()
                    encrypted = self.cipher.encrypt(clean_text.encode())
                    
                    # Store encrypted version
                    encrypted_data.append({
                        'original_index': doc.paragraphs.index(para),
                        'encrypted': base64.b64encode(encrypted).decode()
                    })
                    
                    # Replace with placeholder
                    para.text = '[ENCRYPTED CONTENT - ID: {}]'.format(
                        hashlib.md5(encrypted).hexdigest()[:8]
                    )
            
            # Save encrypted document
            encrypted_path = doc_path.replace('.docx', '_encrypted.docx')
            doc.save(encrypted_path)
            
            # Save encryption metadata
            metadata = {
                'key': base64.b64encode(self.key).decode(),
                'encrypted_sections': encrypted_data
            }
            
            with open(encrypted_path.replace('.docx', '_key.json'), 'w') as f:
                json.dump(metadata, f)
            
            return encrypted_path
        
        def add_document_protection(self, doc_path, password):
            """Add various protection mechanisms"""
            if os.name == 'nt':  # Windows only
                import win32com.client
                
                word = win32com.client.Dispatch("Word.Application")
                doc = word.Documents.Open(os.path.abspath(doc_path))
                
                # Protection types:
                # 0 - No protection
                # 1 - Allow only revisions
                # 2 - Allow only comments
                # 3 - Allow only form fields
                # 4 - Read only
                
                doc.Protect(Type=3, NoReset=False, Password=password)
                
                protected_path = doc_path.replace('.docx', '_protected.docx')
                doc.SaveAs2(os.path.abspath(protected_path))
                doc.Close()
                word.Quit()
                
                return protected_path

## Document Accessibility

<!-- python -->
    from docx import Document
    from docx.shared import Pt, RGBColor

    def create_accessible_document(content, title):
        """Create document following accessibility guidelines"""
        doc = Document()
        
        # Set document properties for accessibility
        doc.core_properties.title = title
        doc.core_properties.subject = "Accessible Document"
        doc.core_properties.keywords = "accessibility, WCAG"
        
        # Use proper heading hierarchy
        doc.add_heading(title, 0)  # Title (Heading 1)
        
        # Ensure sufficient color contrast
        for section in content:
            if section['type'] == 'heading':
                heading = doc.add_heading(section['text'], section['level'])
                # Ensure heading has good contrast
                for run in heading.runs:
                    run.font.color.rgb = RGBColor(0, 0, 0)  # Black on white
                    
            elif section['type'] == 'paragraph':
                para = doc.add_paragraph(section['text'])
                # Ensure minimum font size for readability
                for run in para.runs:
                    run.font.size = Pt(12)  # Minimum 12pt for body text
                    
            elif section['type'] == 'list':
                for item in section['items']:
                    doc.add_paragraph(item, style='List Bullet')
                    
            elif section['type'] == 'image':
                # Add image with alt text
                doc.add_picture(section['path'], width=Inches(4))
                # Add caption as alt text
                caption = doc.add_paragraph(f"Figure: {section['alt_text']}")
                caption.style = 'Caption'
        
        # Add table of contents for navigation
        doc.add_page_break()
        doc.add_heading('Table of Contents', 1)
        
        # Extract headings for TOC
        for para in doc.paragraphs:
            if para.style.name.startswith('Heading') and para.text != 'Table of Contents':
                level = int(para.style.name[-1])
                indent = '  ' * (level - 1)
                doc.add_paragraph(f"{indent}• {para.text}")
        
        return doc

## Performance Monitoring

<!-- python -->
    import time
    import psutil
    import functools
    from docx import Document

    def monitor_performance(func):
        """Decorator to monitor document operation performance"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Start monitoring
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            # Execute function
            result = func(*args, **kwargs)
            
            # End monitoring
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            # Log performance metrics
            metrics = {
                'function': func.__name__,
                'execution_time': f"{end_time - start_time:.2f} seconds",
                'memory_used': f"{end_memory - start_memory:.2f} MB",
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"Performance Metrics: {metrics}")
            
            return result
        return wrapper

    @monitor_performance
    def process_large_document(file_path):
        """Process large documents efficiently"""
        doc = Document(file_path)
        
        # Process in chunks to manage memory
        chunk_size = 100
        total_paragraphs = len(doc.paragraphs)
        
        for i in range(0, total_paragraphs, chunk_size):
            chunk = doc.paragraphs[i:i + chunk_size]
            
            # Process chunk
            for para in chunk:
                # Perform operations
                if para.text:
                    para.text = para.text.strip()
        
        return doc

## Integration with Other Formats

<!-- python -->
    from docx import Document
    import pandas as pd
    import markdown
    from bs4 import BeautifulSoup

    def excel_to_docx(excel_path, docx_path):
        """Convert Excel file to formatted DOCX"""
        doc = Document()
        
        # Read Excel file
        xls = pd.ExcelFile(excel_path)
        
        for sheet_name in xls.sheet_names:
            # Add sheet as section
            doc.add_heading(f'Sheet: {sheet_name}', 1)
            
            # Read sheet data
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            
            # Create table
            table = doc.add_table(rows=len(df) + 1, cols=len(df.columns))
            table.style = 'Light Grid Accent 1'
            
            # Add headers
            for i, column in enumerate(df.columns):
                table.cell(0, i).text = str(column)
            
            # Add data
            for row_idx, row in df.iterrows():
                for col_idx, value in enumerate(row):
                    table.cell(row_idx + 1, col_idx).text = str(value)
            
            doc.add_paragraph()  # Add spacing
        
        doc.save(docx_path)
        return doc

    def markdown_to_docx(md_path, docx_path):
        """Convert Markdown to DOCX with formatting"""
        doc = Document()
        
        # Read markdown
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert to HTML
        html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
        soup = BeautifulSoup(html, 'html.parser')
        
        # Process HTML elements
        for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol', 'table', 'pre']):
            if element.name == 'h1':
                doc.add_heading(element.text, 1)
            elif element.name == 'h2':
                doc.add_heading(element.text, 2)
            elif element.name == 'h3':
                doc.add_heading(element.text, 3)
            elif element.name == 'p':
                para = doc.add_paragraph()
                # Process inline formatting
                for child in element.children:
                    if child.name == 'strong':
                        para.add_run(child.text).bold = True
                    elif child.name == 'em':
                        para.add_run(child.text).italic = True
                    elif child.name == 'code':
                        run = para.add_run(child.text)
                        run.font.name = 'Consolas'
                        run.font.color.rgb = RGBColor(100, 100, 100)
                    else:
                        para.add_run(str(child))
            elif element.name in ['ul', 'ol']:
                for li in element.find_all('li'):
                    style = 'List Bullet' if element.name == 'ul' else 'List Number'
                    doc.add_paragraph(li.text, style=style)
            elif element.name == 'pre':
                # Code block
                para = doc.add_paragraph()
                run = para.add_run(element.text)
                run.font.name = 'Consolas'
                run.font.size = Pt(10)
                para.paragraph_format.left_indent = Inches(0.5)
        
        doc.save(docx_path)
        return doc

## Quick Reference

| Task | Best Tool/Method | Command/Code |
|------|-----------------|--------------|
| Create DOCX | python-docx | `Document()` |
| Extract text | python-docx | `paragraph.text` |
| Extract tables | python-docx | `doc.tables` |
| Merge documents | python-docx | Copy elements |
| Add images | python-docx | `add_picture()` |
| Convert to PDF | docx2pdf/win32com | `convert()` |
| Templates | docxtpl | `DocxTemplate()` |
| Batch processing | ThreadPoolExecutor | Parallel processing |
| Add watermark | Custom XML | Shape elements |
| Protect document | win32com (Windows) | `doc.Protect()` |
| Extract images | rels | `doc.part.rels` |
| Mail merge | docxtpl + CSV | `render()` |
| Charts/graphs | matplotlib + io | `add_picture()` |
| Accessibility | Proper structure | Heading hierarchy |
| Performance | Chunking | Process in batches |
| Security | Encryption | Fernet cipher |

## Best Practices

1. **Always validate input files** before processing
2. **Use proper heading hierarchy** for document structure
3. **Implement error handling** for all file operations
4. **Process large documents in chunks** to manage memory
5. **Follow accessibility guidelines** (WCAG) for public documents
6. **Use templates** for consistent formatting across documents
7. **Test PDF conversion** on target platform (Windows/Linux/Mac)
8. **Backup original files** before modifications
9. **Use descriptive variable names** and comments in code
10. **Monitor performance** for batch operations
