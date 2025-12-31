#!/usr/bin/env python3
"""
Convert Student Notes HTML to Presentation Slides HTML
Extracts key content from detailed student notes and creates presentation-ready slides
"""

from bs4 import BeautifulSoup
import re
import os
from pathlib import Path


def extract_title_from_notes(soup):
    """Extract the main title from student notes"""
    h1 = soup.find('h1')
    if h1:
        return h1.get_text().strip()
    return "Course Content"


def extract_learning_objectives(soup):
    """Extract learning objectives if present"""
    objectives = []
    # Look for sections that might contain objectives
    for header in soup.find_all(['h2', 'h3']):
        text = header.get_text().lower()
        if 'objective' in text or 'learning outcome' in text or 'goals' in text:
            # Get the next sibling content
            next_elem = header.find_next_sibling()
            if next_elem and next_elem.name == 'ul':
                for li in next_elem.find_all('li', recursive=False):
                    objectives.append(li.get_text().strip())
            elif next_elem and next_elem.name == 'p':
                objectives.append(next_elem.get_text().strip())
    return objectives


def extract_sections(soup):
    """Extract main sections and their content"""
    sections = []
    
    # Find all h2 headers (main sections)
    h2_headers = soup.find_all('h2')
    
    for h2 in h2_headers:
        section_title = h2.get_text().strip()
        section_content = {
            'title': section_title,
            'subsections': []
        }
        
        # Get all content until the next h2
        current = h2.find_next_sibling()
        current_subsection = None
        
        while current and current.name != 'h2':
            if current.name == 'h3':
                # New subsection
                if current_subsection:
                    section_content['subsections'].append(current_subsection)
                current_subsection = {
                    'title': current.get_text().strip(),
                    'content': []
                }
            elif current_subsection is not None:
                # Add content to current subsection
                if current.name == 'p':
                    text = current.get_text().strip()
                    if text:
                        current_subsection['content'].append({
                            'type': 'text',
                            'value': text
                        })
                elif current.name == 'ul':
                    items = [li.get_text().strip() for li in current.find_all('li', recursive=False)]
                    if items:
                        current_subsection['content'].append({
                            'type': 'list',
                            'items': items
                        })
                elif current.name == 'pre' or (current.name == 'div' and 'code-block' in current.get('class', [])):
                    code = current.get_text().strip()
                    if code:
                        current_subsection['content'].append({
                            'type': 'code',
                            'value': code
                        })
                elif current.name == 'table':
                    current_subsection['content'].append({
                        'type': 'table',
                        'html': str(current)
                    })
                elif current.name == 'img':
                    current_subsection['content'].append({
                        'type': 'image',
                        'src': current.get('src', ''),
                        'alt': current.get('alt', '')
                    })
                elif current.name == 'blockquote':
                    text = current.get_text().strip()
                    if text:
                        current_subsection['content'].append({
                            'type': 'quote',
                            'value': text
                        })
            
            current = current.find_next_sibling()
        
        # Add the last subsection
        if current_subsection:
            section_content['subsections'].append(current_subsection)
        
        sections.append(section_content)
    
    return sections


def generate_slides_html(title, week_num, objectives, sections, output_path):
    """Generate the presentation slides HTML"""
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Presentation Slides</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #ffffff;
            line-height: 1.6;
        }}
        
        .slide {{
            min-height: 100vh;
            padding: 60px 80px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            page-break-after: always;
            border-bottom: 3px solid #0f3460;
        }}
        
        .slide:nth-child(even) {{
            background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
        }}
        
        .title-slide {{
            justify-content: center;
            align-items: center;
            text-align: center;
            background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
        }}
        
        .title-slide h1 {{
            font-size: 3.5em;
            margin-bottom: 20px;
            color: #e94560;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .title-slide .week-number {{
            font-size: 1.5em;
            color: #ffd700;
            margin-bottom: 40px;
            letter-spacing: 2px;
        }}
        
        .title-slide .course-code {{
            font-size: 1.2em;
            color: #a8dadc;
            margin-top: 30px;
        }}
        
        h2 {{
            font-size: 2.5em;
            color: #e94560;
            margin-bottom: 30px;
            border-bottom: 3px solid #ffd700;
            padding-bottom: 15px;
        }}
        
        h3 {{
            font-size: 2em;
            color: #ffd700;
            margin-bottom: 25px;
        }}
        
        ul {{
            font-size: 1.4em;
            margin-left: 40px;
            margin-bottom: 20px;
        }}
        
        ul li {{
            margin-bottom: 15px;
            line-height: 1.8;
        }}
        
        p {{
            font-size: 1.3em;
            margin-bottom: 20px;
            line-height: 1.8;
        }}
        
        .code-block {{
            background: #0f0f0f;
            border-left: 4px solid #e94560;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            overflow-x: auto;
        }}
        
        pre {{
            background: #0f0f0f;
            border-left: 4px solid #e94560;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 1.1em;
            line-height: 1.5;
        }}
        
        code {{
            font-family: 'Courier New', monospace;
            color: #a8dadc;
        }}
        
        .quote {{
            background: rgba(233, 69, 96, 0.1);
            border-left: 5px solid #e94560;
            padding: 20px;
            margin: 20px 0;
            font-style: italic;
            font-size: 1.2em;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 1.2em;
        }}
        
        th {{
            background: #0f3460;
            color: #ffd700;
            padding: 15px;
            text-align: left;
            border: 1px solid #16213e;
        }}
        
        td {{
            padding: 12px;
            border: 1px solid #16213e;
            background: rgba(255, 255, 255, 0.05);
        }}
        
        tr:hover {{
            background: rgba(233, 69, 96, 0.1);
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            margin: 20px 0;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }}
        
        .key-points {{
            background: rgba(255, 215, 0, 0.1);
            border: 2px solid #ffd700;
            padding: 30px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        
        .slide-number {{
            position: fixed;
            bottom: 20px;
            right: 30px;
            font-size: 1em;
            color: #a8dadc;
            opacity: 0.7;
        }}
        
        @media print {{
            .slide {{
                page-break-after: always;
            }}
        }}
    </style>
</head>
<body>
"""
    
    slide_num = 1
    
    # Title slide
    html_template += f"""
    <div class="slide title-slide">
        <div class="week-number">Week {week_num}</div>
        <h1>{title}</h1>
        <div class="course-code">OPS3 - Virtualization and Cloud Infrastructure</div>
        <div class="slide-number">Slide {slide_num}</div>
    </div>
"""
    slide_num += 1
    
    # Learning objectives slide
    if objectives:
        html_template += f"""
    <div class="slide">
        <h2>Learning Objectives</h2>
        <ul>
"""
        for obj in objectives:
            html_template += f"            <li>{obj}</li>\n"
        html_template += f"""        </ul>
        <div class="slide-number">Slide {slide_num}</div>
    </div>
"""
        slide_num += 1
    
    # Content slides
    for section in sections:
        # Section title slide
        html_template += f"""
    <div class="slide">
        <h2>{section['title']}</h2>
        <div class="slide-number">Slide {slide_num}</div>
    </div>
"""
        slide_num += 1
        
        # Subsection slides
        for subsection in section['subsections']:
            html_template += f"""
    <div class="slide">
        <h3>{subsection['title']}</h3>
"""
            
            for content_item in subsection['content']:
                if content_item['type'] == 'text':
                    # Split long paragraphs into bullet points
                    text = content_item['value']
                    if len(text) > 300:
                        # For long text, create bullet points from sentences
                        sentences = re.split(r'(?<=[.!?])\s+', text)
                        html_template += "        <ul>\n"
                        for sentence in sentences[:5]:  # Limit to 5 points
                            if sentence.strip():
                                html_template += f"            <li>{sentence.strip()}</li>\n"
                        html_template += "        </ul>\n"
                    else:
                        html_template += f"        <p>{text}</p>\n"
                
                elif content_item['type'] == 'list':
                    html_template += "        <ul>\n"
                    for item in content_item['items'][:8]:  # Limit to 8 items per slide
                        html_template += f"            <li>{item}</li>\n"
                    html_template += "        </ul>\n"
                
                elif content_item['type'] == 'code':
                    html_template += f"""        <pre><code>{content_item['value']}</code></pre>\n"""
                
                elif content_item['type'] == 'table':
                    html_template += f"        {content_item['html']}\n"
                
                elif content_item['type'] == 'image':
                    alt_text = content_item['alt'] or 'Diagram'
                    html_template += f"""        <img src="{content_item['src']}" alt="{alt_text}">\n"""
                
                elif content_item['type'] == 'quote':
                    html_template += f"""        <div class="quote">{content_item['value']}</div>\n"""
            
            html_template += f"""        <div class="slide-number">Slide {slide_num}</div>
    </div>
"""
            slide_num += 1
    
    # Summary slide
    html_template += f"""
    <div class="slide title-slide">
        <h2>Summary</h2>
        <p style="font-size: 1.5em; margin-top: 30px;">Review the key concepts covered in this week's material</p>
        <p style="font-size: 1.2em; margin-top: 20px; color: #ffd700;">Questions?</p>
        <div class="slide-number">Slide {slide_num}</div>
    </div>
"""
    
    html_template += """
</body>
</html>"""
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    return slide_num


def process_week(week_dir, week_num):
    """Process a single week's student notes and generate slides"""
    student_notes_path = week_dir / f"Week_{week_num}_Student_Notes.html"
    slides_output_path = week_dir / f"Week_{week_num}_Slides.html"
    
    if not student_notes_path.exists():
        print(f"⚠️  Week {week_num}: Student notes not found at {student_notes_path}")
        return False
    
    # Read and parse the student notes HTML
    with open(student_notes_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract content
    title = extract_title_from_notes(soup)
    objectives = extract_learning_objectives(soup)
    sections = extract_sections(soup)
    
    # Generate slides HTML
    num_slides = generate_slides_html(title, week_num, objectives, sections, slides_output_path)
    
    print(f"✅ Week {week_num}: Generated {num_slides} slides -> {slides_output_path.name}")
    return True


def main():
    """Main function to process all weeks"""
    base_dir = Path(__file__).parent.parent
    
    print("=" * 70)
    print("Converting Student Notes to Presentation Slides")
    print("=" * 70)
    print()
    
    weeks = [
        ("Week 1 - Introduction to Virtualization", 1),
        ("Week 2 - Virtual Machines", 2),
        ("Week 3 - Virtual Networking and Linux Networking Fundamentals", 3),
        ("Week 4 - Storage and Backup", 4),
        ("Week 5 - Containers and Resource Management", 5),
        ("Week 6 - Proxmox Cluster and High Availability", 6),
        ("Week 7 - Transition to Cloud Computing Concepts", 7),
        ("Week 8 - Cloud Foundation", 8),
        ("Week 9 - Compute Operations", 9),
        ("Week 10 - Storage and Persistence", 10),
        ("Week 11 - Automation and Cloud API", 11),
        ("Week 12 - Final Project and Review", 12),
    ]
    
    success_count = 0
    for week_name, week_num in weeks:
        week_dir = base_dir / week_name
        if week_dir.exists():
            if process_week(week_dir, week_num):
                success_count += 1
        else:
            print(f"⚠️  Week {week_num}: Directory not found: {week_name}")
    
    print()
    print("=" * 70)
    print(f"✅ Successfully processed {success_count}/{len(weeks)} weeks")
    print("=" * 70)


if __name__ == "__main__":
    main()
