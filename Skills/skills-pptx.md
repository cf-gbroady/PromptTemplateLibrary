# Creating PowerPoint Presentations with Code Interpreter

## Overview
This guide provides comprehensive instructions for creating PowerPoint presentations programmatically using Python's code interpreter capabilities. It covers slide design, content creation, image generation, and template usage.  It's important to plan any presentation before diving in to create and generate the presentation.

## Prerequisites
- Python environment with code interpreter
- Required libraries: `python-pptx`, `Pillow`, `matplotlib`, `seaborn`

## Basic PowerPoint Creation

### 1. Creating a Blank Presentation
\`\`\`python
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
subtitle.text = "Created with Python"

# Save the presentation
prs.save('my_presentation.pptx')
\`\`\`

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
\`\`\`python
def analyze_template(template_path):
    """Analyze a PowerPoint template to understand its layouts"""
    prs = Presentation(template_path)
    
    for idx, layout in enumerate(prs.slide_layouts):
        print(f"Layout {idx}: {layout.name}")
        for placeholder in layout.placeholders:
            print(f"  - Placeholder {placeholder.placeholder_format.idx}: {placeholder.name}")
\`\`\`

## Designing Slide Content

### 1. Adding Text with Formatting
\`\`\`python
def add_formatted_text_slide(prs, title_text, content_items):
    """Add a slide with formatted text content"""
    slide_layout = prs.slide_layouts[1]  # Title and Content layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Set title
    title = slide.shapes.title
    title.text = title_text
    
    # Add content
    content = slide.placeholders[1]
    text_frame = content.text_frame
    text_frame.clear()  # Clear existing content
    
    for item in content_items:
        p = text_frame.add_paragraph()
        p.text = item['text']
        p.level = item.get('level', 0)
        
        # Apply formatting
        font = p.font
        font.name = item.get('font', 'Arial')
        font.size = Pt(item.get('size', 18))
        font.bold = item.get('bold', False)
        font.italic = item.get('italic', False)
        
        if 'color' in item:
            font.color.rgb = RGBColor(*item['color'])
\`\`\`

### 2. Creating Tables
\`\`\`python
def add_table_slide(prs, title_text, data, headers):
    """Add a slide with a table"""
    slide_layout = prs.slide_layouts[5]  # Title Only layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Set title
    title = slide.shapes.title
    title.text = title_text
    
    # Define table dimensions
    rows = len(data) + 1  # +1 for header
    cols = len(headers)
    left = Inches(1)
    top = Inches(2)
    width = Inches(8)
    height = Inches(0.8 * rows)
    
    # Add table
    table = slide.shapes.add_table(rows, cols, left, top, width, height).table
    
    # Set column widths
    for i in range(cols):
        table.columns[i].width = Inches(width.inches / cols)
    
    # Add headers
    for i, header in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = header
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(68, 114, 196)
        
        # Format header text
        paragraph = cell.text_frame.paragraphs[0]
        paragraph.font.bold = True
        paragraph.font.color.rgb = RGBColor(255, 255, 255)
        paragraph.alignment = PP_ALIGN.CENTER
    
    # Add data
    for row_idx, row_data in enumerate(data):
        for col_idx, value in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = str(value)
            
            # Alternate row colors
            if row_idx % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(240, 240, 240)
\`\`\`

### 3. Adding Shapes and Graphics
\`\`\`python
from pptx.enum.shapes import MSO_SHAPE

def add_shapes_slide(prs, title_text):
    """Add a slide with various shapes"""
    slide_layout = prs.slide_layouts[5]  # Title Only layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Set title
    title = slide.shapes.title
    title.text = title_text
    
    # Add rectangle
    left = Inches(1)
    top = Inches(2)
    width = Inches(2)
    height = Inches(1)
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(255, 0, 0)
    
    # Add circle
    left = Inches(4)
    diameter = Inches(1.5)
    shape = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, left, top, diameter, diameter
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0, 255, 0)
    
    # Add arrow
    left = Inches(7)
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RIGHT_ARROW, left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0, 0, 255)
\`\`\`

## Image Generation and Integration

### 1. Generating Charts with Matplotlib
\`\`\`python
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

def generate_chart_image():
    """Generate a chart and return as image bytes"""
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Sample data
    categories = ['Q1', 'Q2', 'Q3', 'Q4']
    values1 = [20, 35, 30, 35]
    values2 = [25, 30, 35, 30]
    
    # Create bar chart
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, values1, width, label='Product A')
    bars2 = ax.bar(x + width/2, values2, width, label='Product B')
    
    # Customize chart
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Sales (in millions)')
    ax.set_title('Quarterly Sales Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom')
    
    # Save to bytes
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer
\`\`\`

### 2. Creating Custom Graphics
\`\`\`python
from PIL import Image, ImageDraw, ImageFont
import io

def create_custom_graphic(width=800, height=600):
    """Create a custom graphic using PIL"""
    # Create new image with gradient background
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for y in range(height):
        color_value = int(255 * (1 - y / height))
        color = (color_value, color_value, 255)
        draw.line([(0, y), (width, y)], fill=color)
    
    # Add shapes
    # Circle
    draw.ellipse([50, 50, 250, 250], fill=(255, 255, 0), outline=(0, 0, 0), width=3)
    
    # Rectangle
    draw.rectangle([300, 100, 500, 200], fill=(0, 255, 0), outline=(0, 0, 0), width=3)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    text = "Custom Graphic"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = height - 100
    
    draw.text((x, y), text, fill=(255, 255, 255), font=font)
    
    # Save to bytes
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    return img_buffer
\`\`\`

### 3. Adding Images to Slides
\`\`\`python
def add_image_slide(prs, title_text, image_path=None, image_bytes=None):
    """Add a slide with an image"""
    slide_layout = prs.slide_layouts[8]  # Picture with Caption layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Set title
    title = slide.shapes.title
    title.text = title_text
    
    # Add image
    left = Inches(1)
    top = Inches(2)
    
    if image_path:
        pic = slide.shapes.add_picture(image_path, left, top)
    elif image_bytes:
        pic = slide.shapes.add_picture(image_bytes, left, top)
    
    # Scale image to fit slide
    max_width = Inches(8)
    max_height = Inches(5)
    
    # Calculate scaling factor
    scale_width = max_width / pic.width
    scale_height = max_height / pic.height
    scale = min(scale_width, scale_height)
    
    # Apply scaling
    pic.width = int(pic.width * scale)
    pic.height = int(pic.height * scale)
    
    # Center the image
    pic.left = int((prs.slide_width - pic.width) / 2)
    
    return slide
\`\`\`

## Working with Templates

### 1. Using Existing Templates
\`\`\`python
from datetime import datetime

def create_from_template(template_path, output_path):
    """Create a presentation from an existing template"""
    # Load template
    prs = Presentation(template_path)
    
    # Modify first slide (usually title slide)
    slide = prs.slides[0]
    title = slide.shapes.title
    title.text = "Updated Presentation"
    
    # Find and update subtitle
    for shape in slide.placeholders:
        if shape.placeholder_format.idx == 1:  # Subtitle placeholder
            shape.text = f"Generated on {datetime.now().strftime('%Y-%m-%d')}"
    
    # Add new slide with content
    content_layout = prs.slide_layouts[1]  # Title and Content
    new_slide = prs.slides.add_slide(content_layout)
    
    title = new_slide.shapes.title
    title.text = "Key Points"
    
    content = new_slide.placeholders[1]
    tf = content.text_frame
    tf.text = "First point"
    
    p = tf.add_paragraph()
    p.text = "Second point"
    p.level = 0
    
    p = tf.add_paragraph()
    p.text = "Sub-point"
    p.level = 1
    
    # Save modified presentation
    prs.save(output_path)
\`\`\`

### 2. Creating Custom Templates
\`\`\`python
def create_custom_template():
    """Create a custom template with predefined styles"""
    prs = Presentation()
    
    # Define custom color scheme
    title_color = RGBColor(0, 51, 102)  # Dark blue
    subtitle_color = RGBColor(102, 102, 102)  # Gray
    accent_color = RGBColor(255, 192, 0)  # Orange
    
    # Customize slide master
    slide_master = prs.slide_master
    
    # Create title slide layout
    title_slide = prs.slides.add_slide(prs.slide_layouts[0])
    
    # Style title
    title = title_slide.shapes.title
    title.text = "Template Title"
    title.text_frame.paragraphs[0].font.color.rgb = title_color
    title.text_frame.paragraphs[0].font.size = Pt(44)
    title.text_frame.paragraphs[0].font.bold = True
    
    # Style subtitle
    subtitle = title_slide.placeholders[1]
    subtitle.text = "Template Subtitle"
    subtitle.text_frame.paragraphs[0].font.color.rgb = subtitle_color
    subtitle.text_frame.paragraphs[0].font.size = Pt(24)
    
    # Add footer to all slides
    for slide in prs.slides:
        footer_left = Inches(0.5)
        footer_top = Inches(6.9)
        footer_width = Inches(12.33)
        footer_height = Inches(0.5)
        
        footer = slide.shapes.add_textbox(
            footer_left, footer_top, footer_width, footer_height
        )
        footer.text = "© 2024 Your Company"
        footer.text_frame.paragraphs[0].font.size = Pt(10)
        footer.text_frame.paragraphs[0].font.color.rgb = subtitle_color
    
    return prs
\`\`\`

### 3. Template Best Practices
\`\`\`python
class PresentationTemplate:
    """Class for managing presentation templates"""
    
    def __init__(self, template_path=None):
        if template_path:
            self.prs = Presentation(template_path)
        else:
            self.prs = Presentation()
        
        # Define style constants
        self.colors = {
            'primary': RGBColor(0, 51, 102),
            'secondary': RGBColor(102, 102, 102),
            'accent': RGBColor(255, 192, 0),
            'success': RGBColor(0, 176, 80),
            'warning': RGBColor(255, 192, 0),
            'danger': RGBColor(255, 0, 0)
        }
        
        self.fonts = {
            'title': {'name': 'Arial', 'size': 44, 'bold': True},
            'subtitle': {'name': 'Arial', 'size': 24, 'bold': False},
            'body': {'name': 'Arial', 'size': 18, 'bold': False},
            'caption': {'name': 'Arial', 'size': 14, 'bold': False}
        }
    
    def add_title_slide(self, title, subtitle=None):
        """Add a styled title slide"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[0])
        
        # Apply title styling
        title_shape = slide.shapes.title
        title_shape.text = title
        self._apply_text_style(title_shape.text_frame.paragraphs[0], 'title', 'primary')
        
        # Apply subtitle styling if provided
        if subtitle and len(slide.placeholders) > 1:
            subtitle_shape = slide.placeholders[1]
            subtitle_shape.text = subtitle
            self._apply_text_style(subtitle_shape.text_frame.paragraphs[0], 'subtitle', 'secondary')
        
        return slide
    
    def _apply_text_style(self, paragraph, font_style, color_name):
        """Apply consistent text styling"""
        font_config = self.fonts[font_style]
        paragraph.font.name = font_config['name']
        paragraph.font.size = Pt(font_config['size'])
        paragraph.font.bold = font_config['bold']
        paragraph.font.color.rgb = self.colors[color_name]
\`\`\`

## Complete Example: Creating a Professional Presentation

\`\`\`python
from pptx.enum.shapes import MSO_SHAPE_TYPE

def create_professional_presentation():
    """Create a complete professional presentation with multiple slide types"""
    
    # Initialize presentation
    prs = Presentation()
    template = PresentationTemplate()
    
    # 1. Title Slide
    template.add_title_slide(
        "Quarterly Business Review",
        "Q4 2024 Performance Analysis"
    )
    
    # 2. Agenda Slide
    agenda_items = [
        {'text': 'Executive Summary', 'level': 0},
        {'text': 'Sales Performance', 'level': 0},
        {'text': 'Regional Analysis', 'level': 1},
        {'text': 'Product Categories', 'level': 1},
        {'text': 'Market Trends', 'level': 0},
        {'text': 'Future Outlook', 'level': 0}
    ]
    add_formatted_text_slide(prs, "Agenda", agenda_items)
    
    # 3. Chart Slide
    chart_image = generate_chart_image()
    add_image_slide(prs, "Sales Performance", image_bytes=chart_image)
    
    # 4. Table Slide
    headers = ['Region', 'Q3 Sales', 'Q4 Sales', 'Growth %']
    data = [
        ['North', '$1.2M', '$1.5M', '+25%'],
        ['South', '$0.9M', '$1.1M', '+22%'],
        ['East', '$1.5M', '$1.7M', '+13%'],
        ['West', '$0.8M', '$0.9M', '+12%']
    ]
    add_table_slide(prs, "Regional Performance", data, headers)
    
    # 5. Custom Graphic Slide
    custom_graphic = create_custom_graphic()
    add_image_slide(prs, "Market Position", image_bytes=custom_graphic)
    
    # 6. Conclusion Slide
    conclusion_items = [
        {'text': 'Strong growth across all regions', 'level': 0, 'bold': True},
        {'text': 'Product A leading in market share', 'level': 0},
        {'text': 'Positive outlook for Q1 2025', 'level': 0},
        {'text': 'Recommend continued investment in R&D', 'level': 0, 'color': (0, 176, 80)}
    ]
    add_formatted_text_slide(prs, "Key Takeaways", conclusion_items)
    
    # Save presentation
    prs.save('professional_presentation.pptx')
    print("Presentation created successfully!")

# Run the example
create_professional_presentation()
\`\`\`

## Tips for Visual Appeal

### 1. Color Schemes
- Use consistent color palettes throughout the presentation
- Limit to 3-4 main colors
- Use color to highlight important information
- Ensure sufficient contrast for readability

### 2. Typography
- Use no more than 2-3 font families
- Maintain consistent font sizes for similar elements
- Use bold and italic sparingly for emphasis
- Ensure text is large enough to read from a distance

### 3. Layout Principles
- Follow the rule of thirds for positioning elements
- Maintain consistent margins and spacing
- Use white space effectively
- Align elements properly

### 4. Image Best Practices
- Use high-resolution images (300 DPI for printing)
- Maintain aspect ratios when scaling
- Compress images to reduce file size
- Use consistent image styles (e.g., all photos or all illustrations)

## Error Handling and Validation

\`\`\`python
def validate_presentation(prs):
    """Validate presentation for common issues"""
    issues = []
    
    for slide_idx, slide in enumerate(prs.slides):
        # Check for empty titles
        if hasattr(slide.shapes, 'title') and slide.shapes.title:
            if not slide.shapes.title.text or slide.shapes.title.text.strip() == "":
                issues.append(f"Slide {slide_idx + 1}: Empty title")
        
        # Check for placeholder text
        for shape in slide.shapes:
            if hasattr(shape, 'text') and shape.text:
                if "placeholder" in shape.text.lower() or "lorem ipsum" in shape.text.lower():
                    issues.append(f"Slide {slide_idx + 1}: Contains placeholder text")
        
        # Check image resolution
        for shape in slide.shapes:
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                if shape.width < Inches(1) or shape.height < Inches(1):
                    issues.append(f"Slide {slide_idx + 1}: Image may be too small")
    
    return issues

def save_with_validation(prs, filename):
    """Save presentation with validation check"""
    issues = validate_presentation(prs)
    
    if issues:
        print("Warning: The following issues were found:")
        for issue in issues:
            print(f"  - {issue}")
        
        response = input("Do you want to save anyway? (y/n): ")
        if response.lower() != 'y':
            print("Save cancelled.")
            return False
    
    prs.save(filename)
    print(f"Presentation saved as {filename}")
    return True
\`\`\`

## Advanced Features

### 1. Slide Transitions
\`\`\`python
def add_transitions(prs):
    """Add transitions between slides"""
    from pptx.enum.slide import PP_TRANSITION
    
    for slide in prs.slides:
        # Add fade transition
        slide.slide_layout.slide_master.transition.type = PP_TRANSITION.FADE
        slide.slide_layout.slide_master.transition.duration = 1.0
\`\`\`

### 2. Speaker Notes
\`\`\`python
def add_speaker_notes(slide, notes_text):
    """Add speaker notes to a slide"""
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text
\`\`\`

### 3. Hyperlinks
\`\`\`python
def add_hyperlink(shape, url):
    """Add hyperlink to a shape"""
    shape.click_action.hyperlink.address = url
\`\`\`

## Image Generation with AI

### 1. Preparing Image Generation Prompts
\`\`\`python
def prepare_image_prompt(slide_content, style="professional"):
    """Prepare prompt for AI image generation"""
    base_prompt = f"Create a {style} image for a presentation slide about {slide_content}"
    
    style_modifiers = {
        "professional": "clean, modern, business-appropriate",
        "creative": "artistic, colorful, innovative",
        "technical": "detailed, diagram-style, technical illustration",
        "minimal": "simple, minimalist, clean lines"
    }
    
    if style in style_modifiers:
        base_prompt += f", {style_modifiers[style]}"
    
    return base_prompt
\`\`\`

### 2. Integrating Generated Images
\`\`\`python
def add_ai_generated_image(prs, title, image_prompt, position="center"):
    """Add slide with AI-generated image"""
    # Note: This assumes the AI agent has generated and saved an image
    slide = prs.slides.add_slide(prs.slide_layouts[8])
    
    # Set title
    title_shape = slide.shapes.title
    title_shape.text = title
    
    # Placeholder for image integration
    # The actual image would be generated by the AI agent
    # and then added using the add_picture method
    
    print(f"Image prompt: {image_prompt}")
    print("Generate image using AI capabilities, then add to slide")
    
    return slide
\`\`\`

## Best Practices Summary

1. **Planning**
   - Define presentation structure before coding
   - Create a content outline
   - Identify required visual elements

2. **Consistency**
   - Use templates for uniform styling
   - Maintain consistent color schemes
   - Apply standard fonts throughout

3. **Performance**
   - Optimize image sizes
   - Limit animations and transitions
   - Test on target display devices

4. **Accessibility**
   - Use high contrast colors
   - Include alt text for images
   - Ensure readable font sizes

5. **Version Control**
   - Save incremental versions
   - Document changes
   - Maintain template library

## Conclusion

This comprehensive guide provides all the necessary tools and techniques for creating professional PowerPoint presentations programmatically. By combining these methods with the agent's image generation capabilities, you can create visually appealing and data-rich presentations efficiently.

Remember to:
- Plan your presentation structure before coding
- Use templates for consistency
- Generate high-quality images and charts
- Validate your output before finalizing
- Keep accessibility in mind (proper contrast, readable fonts)
- Test presentations on different devices and screens